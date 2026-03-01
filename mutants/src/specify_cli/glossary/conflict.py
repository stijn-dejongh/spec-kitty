"""Conflict detection logic (WP04).

This module implements conflict classification and severity scoring for
semantic conflicts detected during term resolution.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from .extraction import ExtractedTerm
from .models import ConflictType, Severity, TermSense, TermSurface, SenseRef, SenseStatus

if TYPE_CHECKING:
    from . import models
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


def classify_conflict(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    args = [term, resolution_results, is_critical_step, llm_output_text]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_classify_conflict__mutmut_orig, x_classify_conflict__mutmut_mutants, args, kwargs, None)


def x_classify_conflict__mutmut_orig(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_1(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = True,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_2(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_3(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step or term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_4(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence <= 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_5(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 1.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_6(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = None
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_7(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status != SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_8(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) >= 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_9(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 2:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_10(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None or len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_11(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_12(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) != 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_13(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 2:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_14(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = None
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_15(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[1]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_16(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(None, sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_17(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, None, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_18(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, None):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_19(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(sense.definition, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_20(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, llm_output_text):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None


def x_classify_conflict__mutmut_21(
    term: ExtractedTerm,
    resolution_results: List[TermSense],
    is_critical_step: bool = False,
    llm_output_text: Optional[str] = None,
) -> Optional[ConflictType]:
    """Classify conflict type based on resolution results.

    Args:
        term: Extracted term with confidence score
        resolution_results: List of TermSense from scope resolution
        is_critical_step: Whether the step is marked as critical (for UNRESOLVED_CRITICAL)
        llm_output_text: LLM output text to check for contradictions (for INCONSISTENT)

    Returns:
        ConflictType if a conflict exists, None otherwise

    Conflict types:
        - UNKNOWN: No match in any scope
        - AMBIGUOUS: 2+ active senses, unqualified usage
        - INCONSISTENT: LLM output contradicts active glossary
        - UNRESOLVED_CRITICAL: Critical term, low confidence, unresolved

    Note:
        INCONSISTENT detection requires llm_output_text parameter.
        UNRESOLVED_CRITICAL requires is_critical_step=True.
    """
    # UNKNOWN: No match in any scope
    if not resolution_results:
        # Check if this is a critical step with low confidence (UNRESOLVED_CRITICAL)
        if is_critical_step and term.confidence < 0.5:
            return ConflictType.UNRESOLVED_CRITICAL
        return ConflictType.UNKNOWN

    # AMBIGUOUS: 2+ active senses (filter out deprecated/draft)
    active_senses = [s for s in resolution_results if s.status == SenseStatus.ACTIVE]
    if len(active_senses) > 1:
        return ConflictType.AMBIGUOUS

    # Single match - check for INCONSISTENT
    if llm_output_text is not None and len(resolution_results) == 1:
        sense = resolution_results[0]
        # Simple contradiction check: if LLM output uses the term but with
        # a different meaning than the glossary definition (heuristic)
        # This is a basic implementation - WP06 may enhance with semantic analysis
        if _detect_inconsistent_usage(term.surface, sense.definition, ):
            return ConflictType.INCONSISTENT

    # Single match - no conflict
    return None

x_classify_conflict__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_classify_conflict__mutmut_1': x_classify_conflict__mutmut_1, 
    'x_classify_conflict__mutmut_2': x_classify_conflict__mutmut_2, 
    'x_classify_conflict__mutmut_3': x_classify_conflict__mutmut_3, 
    'x_classify_conflict__mutmut_4': x_classify_conflict__mutmut_4, 
    'x_classify_conflict__mutmut_5': x_classify_conflict__mutmut_5, 
    'x_classify_conflict__mutmut_6': x_classify_conflict__mutmut_6, 
    'x_classify_conflict__mutmut_7': x_classify_conflict__mutmut_7, 
    'x_classify_conflict__mutmut_8': x_classify_conflict__mutmut_8, 
    'x_classify_conflict__mutmut_9': x_classify_conflict__mutmut_9, 
    'x_classify_conflict__mutmut_10': x_classify_conflict__mutmut_10, 
    'x_classify_conflict__mutmut_11': x_classify_conflict__mutmut_11, 
    'x_classify_conflict__mutmut_12': x_classify_conflict__mutmut_12, 
    'x_classify_conflict__mutmut_13': x_classify_conflict__mutmut_13, 
    'x_classify_conflict__mutmut_14': x_classify_conflict__mutmut_14, 
    'x_classify_conflict__mutmut_15': x_classify_conflict__mutmut_15, 
    'x_classify_conflict__mutmut_16': x_classify_conflict__mutmut_16, 
    'x_classify_conflict__mutmut_17': x_classify_conflict__mutmut_17, 
    'x_classify_conflict__mutmut_18': x_classify_conflict__mutmut_18, 
    'x_classify_conflict__mutmut_19': x_classify_conflict__mutmut_19, 
    'x_classify_conflict__mutmut_20': x_classify_conflict__mutmut_20, 
    'x_classify_conflict__mutmut_21': x_classify_conflict__mutmut_21
}
x_classify_conflict__mutmut_orig.__name__ = 'x_classify_conflict'


def _detect_inconsistent_usage(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    args = [term_surface, glossary_definition, llm_output]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__detect_inconsistent_usage__mutmut_orig, x__detect_inconsistent_usage__mutmut_mutants, args, kwargs, None)


def x__detect_inconsistent_usage__mutmut_orig(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_1(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = None
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_2(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.upper()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_3(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = None
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_4(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.upper()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_5(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = None

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_6(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.upper()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_7(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_8(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return True

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_9(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = None
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_10(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "XXaXX", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_11(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "A", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_12(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "XXanXX", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_13(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "AN", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_14(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "XXtheXX", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_15(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "THE", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_16(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "XXisXX", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_17(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "IS", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_18(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "XXareXX", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_19(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "ARE", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_20(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "XXofXX", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_21(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "OF", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_22(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "XXforXX", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_23(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "FOR", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_24(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "XXtoXX", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_25(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "TO", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_26(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "XXinXX", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_27(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "IN", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_28(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "XXonXX",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_29(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "ON",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_30(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "XXatXX", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_31(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "AT", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_32(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "XXbyXX", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_33(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "BY", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_34(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "XXwithXX", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_35(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "WITH", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_36(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "XXfromXX", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_37(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "FROM", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_38(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "XXasXX", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_39(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "AS", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_40(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "XXandXX", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_41(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "AND", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_42(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "XXorXX", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_43(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "OR", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_44(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "XXbutXX",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_45(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "BUT",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_46(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = None

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_47(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        None
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_48(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(None)
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_49(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip("XX.,;:!?XX")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_50(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 or word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_51(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) >= 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_52(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 4 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_53(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_54(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = None
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_55(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(None)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_56(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = None

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_57(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(None)

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_58(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(None, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_59(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, None))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_60(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_61(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, ))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_62(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = None
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_63(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(None)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_64(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(2)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_65(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = None
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_66(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(None)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_67(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(3)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_68(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = None

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_69(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " - after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_70(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower - " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_71(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " - term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_72(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context - " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_73(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + "XX XX" + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_74(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + "XX XX" + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_75(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = None
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_76(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(None, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_77(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, None):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_78(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_79(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, ):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_80(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return False  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_81(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = None

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_82(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(None)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_83(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(None)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_84(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(None)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_85(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(None)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_86(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(None)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_87(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(None, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_88(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, None):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_89(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_90(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, ):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_91(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return False  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_92(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = None

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_93(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(None)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_94(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(None, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_95(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, None):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_96(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_97(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, ):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_98(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = None

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_99(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    None
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_100(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(None)
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_101(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip("XX.,;:!?XX")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_102(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 or word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_103(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) >= 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_104(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 4 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_105(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_106(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = None
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_107(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = None
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_108(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap * len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_109(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio <= 0.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_110(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 1.3:
                        return True  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_111(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return False  # Low overlap = likely contradiction

    return False


def x__detect_inconsistent_usage__mutmut_112(
    term_surface: str,
    glossary_definition: str,
    llm_output: str,
) -> bool:
    """Detect if LLM output uses term inconsistently with glossary.

    This is a heuristic-based implementation. Uses simple keyword matching
    to detect if the term appears in output with contradictory context.

    Args:
        term_surface: The term being checked
        glossary_definition: The authoritative definition from glossary
        llm_output: The LLM-generated text to analyze

    Returns:
        True if inconsistent usage detected

    Implementation:
        Uses keyword-based contradiction detection:
        1. Extract key concepts from glossary definition (nouns)
        2. Search for term usage context in LLM output
        3. Check if context contradicts key concepts

        Contradiction indicators:
        - Negation words near term ("not a", "isn't a", "unlike")
        - Alternative definitions ("refers to", "means", "is a")
        - Context missing key concepts from definition

    Note:
        This is a basic heuristic implementation. WP06 may enhance with:
        - Semantic similarity models
        - Context window analysis
        - LLM-based contradiction detection
    """
    # Normalize inputs
    term_lower = term_surface.lower()
    definition_lower = glossary_definition.lower()
    output_lower = llm_output.lower()

    # Quick exit: term not in output
    if term_lower not in output_lower:
        return False

    # Extract key concepts from definition (simple noun extraction)
    # Split definition into words, filter stop words
    stop_words = {
        "a", "an", "the", "is", "are", "of", "for", "to", "in", "on",
        "at", "by", "with", "from", "as", "and", "or", "but",
    }
    definition_words = set(
        word.strip(".,;:!?")
        for word in definition_lower.split()
        if len(word) > 3 and word not in stop_words
    )

    # Find term occurrences in output with context window
    import re

    # Pattern: capture 50 chars before and after term
    pattern = rf"(.{{0,50}})\b{re.escape(term_lower)}\b(.{{0,50}})"
    matches = list(re.finditer(pattern, output_lower))

    for match in matches:
        before_context = match.group(1)
        after_context = match.group(2)
        context = before_context + " " + term_lower + " " + after_context

        # Check for direct negation of definition key concepts
        # Example: definition has "unit of work", output says "not a unit of work"
        for def_word in definition_words:
            # Pattern: "is not a {def_word}", "isn't a {def_word}", "{term} not a {def_word}"
            negation_of_concept = (
                rf"\b(is\s+not|isn['']t|not\s+a|not\s+an)\s+({def_word}|[a-z]+\s+{def_word})"
            )
            if re.search(negation_of_concept, context):
                return True  # Negation of key concept = contradiction

        # Check for broader negation patterns
        negation_patterns = [
            rf"\b{re.escape(term_lower)}\s+is\s+not\s+a?\b",
            rf"\b{re.escape(term_lower)}\s+isn['']t\s+a?\b",
            rf"\bnot\s+a\s+{re.escape(term_lower)}\b",
            rf"\bunlike\s+{re.escape(term_lower)}\b",
            rf"\bcontrary\s+to\s+{re.escape(term_lower)}\b",
        ]

        for neg_pattern in negation_patterns:
            if re.search(neg_pattern, context):
                return True  # Negation found = contradiction

        # Check for alternative definitions
        alternative_patterns = [
            rf"\b{re.escape(term_lower)}\s+(refers\s+to|means|is\s+a|is\s+an)\b",
        ]

        for alt_pattern in alternative_patterns:
            if re.search(alt_pattern, context):
                # Check if the alternative definition contradicts key concepts
                context_words = set(
                    word.strip(".,;:!?")
                    for word in context.split()
                    if len(word) > 3 and word not in stop_words
                )

                # If less than 30% overlap with definition key concepts, flag inconsistency
                if definition_words:
                    overlap = len(definition_words & context_words)
                    overlap_ratio = overlap / len(definition_words)
                    if overlap_ratio < 0.3:
                        return True  # Low overlap = likely contradiction

    return True

x__detect_inconsistent_usage__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__detect_inconsistent_usage__mutmut_1': x__detect_inconsistent_usage__mutmut_1, 
    'x__detect_inconsistent_usage__mutmut_2': x__detect_inconsistent_usage__mutmut_2, 
    'x__detect_inconsistent_usage__mutmut_3': x__detect_inconsistent_usage__mutmut_3, 
    'x__detect_inconsistent_usage__mutmut_4': x__detect_inconsistent_usage__mutmut_4, 
    'x__detect_inconsistent_usage__mutmut_5': x__detect_inconsistent_usage__mutmut_5, 
    'x__detect_inconsistent_usage__mutmut_6': x__detect_inconsistent_usage__mutmut_6, 
    'x__detect_inconsistent_usage__mutmut_7': x__detect_inconsistent_usage__mutmut_7, 
    'x__detect_inconsistent_usage__mutmut_8': x__detect_inconsistent_usage__mutmut_8, 
    'x__detect_inconsistent_usage__mutmut_9': x__detect_inconsistent_usage__mutmut_9, 
    'x__detect_inconsistent_usage__mutmut_10': x__detect_inconsistent_usage__mutmut_10, 
    'x__detect_inconsistent_usage__mutmut_11': x__detect_inconsistent_usage__mutmut_11, 
    'x__detect_inconsistent_usage__mutmut_12': x__detect_inconsistent_usage__mutmut_12, 
    'x__detect_inconsistent_usage__mutmut_13': x__detect_inconsistent_usage__mutmut_13, 
    'x__detect_inconsistent_usage__mutmut_14': x__detect_inconsistent_usage__mutmut_14, 
    'x__detect_inconsistent_usage__mutmut_15': x__detect_inconsistent_usage__mutmut_15, 
    'x__detect_inconsistent_usage__mutmut_16': x__detect_inconsistent_usage__mutmut_16, 
    'x__detect_inconsistent_usage__mutmut_17': x__detect_inconsistent_usage__mutmut_17, 
    'x__detect_inconsistent_usage__mutmut_18': x__detect_inconsistent_usage__mutmut_18, 
    'x__detect_inconsistent_usage__mutmut_19': x__detect_inconsistent_usage__mutmut_19, 
    'x__detect_inconsistent_usage__mutmut_20': x__detect_inconsistent_usage__mutmut_20, 
    'x__detect_inconsistent_usage__mutmut_21': x__detect_inconsistent_usage__mutmut_21, 
    'x__detect_inconsistent_usage__mutmut_22': x__detect_inconsistent_usage__mutmut_22, 
    'x__detect_inconsistent_usage__mutmut_23': x__detect_inconsistent_usage__mutmut_23, 
    'x__detect_inconsistent_usage__mutmut_24': x__detect_inconsistent_usage__mutmut_24, 
    'x__detect_inconsistent_usage__mutmut_25': x__detect_inconsistent_usage__mutmut_25, 
    'x__detect_inconsistent_usage__mutmut_26': x__detect_inconsistent_usage__mutmut_26, 
    'x__detect_inconsistent_usage__mutmut_27': x__detect_inconsistent_usage__mutmut_27, 
    'x__detect_inconsistent_usage__mutmut_28': x__detect_inconsistent_usage__mutmut_28, 
    'x__detect_inconsistent_usage__mutmut_29': x__detect_inconsistent_usage__mutmut_29, 
    'x__detect_inconsistent_usage__mutmut_30': x__detect_inconsistent_usage__mutmut_30, 
    'x__detect_inconsistent_usage__mutmut_31': x__detect_inconsistent_usage__mutmut_31, 
    'x__detect_inconsistent_usage__mutmut_32': x__detect_inconsistent_usage__mutmut_32, 
    'x__detect_inconsistent_usage__mutmut_33': x__detect_inconsistent_usage__mutmut_33, 
    'x__detect_inconsistent_usage__mutmut_34': x__detect_inconsistent_usage__mutmut_34, 
    'x__detect_inconsistent_usage__mutmut_35': x__detect_inconsistent_usage__mutmut_35, 
    'x__detect_inconsistent_usage__mutmut_36': x__detect_inconsistent_usage__mutmut_36, 
    'x__detect_inconsistent_usage__mutmut_37': x__detect_inconsistent_usage__mutmut_37, 
    'x__detect_inconsistent_usage__mutmut_38': x__detect_inconsistent_usage__mutmut_38, 
    'x__detect_inconsistent_usage__mutmut_39': x__detect_inconsistent_usage__mutmut_39, 
    'x__detect_inconsistent_usage__mutmut_40': x__detect_inconsistent_usage__mutmut_40, 
    'x__detect_inconsistent_usage__mutmut_41': x__detect_inconsistent_usage__mutmut_41, 
    'x__detect_inconsistent_usage__mutmut_42': x__detect_inconsistent_usage__mutmut_42, 
    'x__detect_inconsistent_usage__mutmut_43': x__detect_inconsistent_usage__mutmut_43, 
    'x__detect_inconsistent_usage__mutmut_44': x__detect_inconsistent_usage__mutmut_44, 
    'x__detect_inconsistent_usage__mutmut_45': x__detect_inconsistent_usage__mutmut_45, 
    'x__detect_inconsistent_usage__mutmut_46': x__detect_inconsistent_usage__mutmut_46, 
    'x__detect_inconsistent_usage__mutmut_47': x__detect_inconsistent_usage__mutmut_47, 
    'x__detect_inconsistent_usage__mutmut_48': x__detect_inconsistent_usage__mutmut_48, 
    'x__detect_inconsistent_usage__mutmut_49': x__detect_inconsistent_usage__mutmut_49, 
    'x__detect_inconsistent_usage__mutmut_50': x__detect_inconsistent_usage__mutmut_50, 
    'x__detect_inconsistent_usage__mutmut_51': x__detect_inconsistent_usage__mutmut_51, 
    'x__detect_inconsistent_usage__mutmut_52': x__detect_inconsistent_usage__mutmut_52, 
    'x__detect_inconsistent_usage__mutmut_53': x__detect_inconsistent_usage__mutmut_53, 
    'x__detect_inconsistent_usage__mutmut_54': x__detect_inconsistent_usage__mutmut_54, 
    'x__detect_inconsistent_usage__mutmut_55': x__detect_inconsistent_usage__mutmut_55, 
    'x__detect_inconsistent_usage__mutmut_56': x__detect_inconsistent_usage__mutmut_56, 
    'x__detect_inconsistent_usage__mutmut_57': x__detect_inconsistent_usage__mutmut_57, 
    'x__detect_inconsistent_usage__mutmut_58': x__detect_inconsistent_usage__mutmut_58, 
    'x__detect_inconsistent_usage__mutmut_59': x__detect_inconsistent_usage__mutmut_59, 
    'x__detect_inconsistent_usage__mutmut_60': x__detect_inconsistent_usage__mutmut_60, 
    'x__detect_inconsistent_usage__mutmut_61': x__detect_inconsistent_usage__mutmut_61, 
    'x__detect_inconsistent_usage__mutmut_62': x__detect_inconsistent_usage__mutmut_62, 
    'x__detect_inconsistent_usage__mutmut_63': x__detect_inconsistent_usage__mutmut_63, 
    'x__detect_inconsistent_usage__mutmut_64': x__detect_inconsistent_usage__mutmut_64, 
    'x__detect_inconsistent_usage__mutmut_65': x__detect_inconsistent_usage__mutmut_65, 
    'x__detect_inconsistent_usage__mutmut_66': x__detect_inconsistent_usage__mutmut_66, 
    'x__detect_inconsistent_usage__mutmut_67': x__detect_inconsistent_usage__mutmut_67, 
    'x__detect_inconsistent_usage__mutmut_68': x__detect_inconsistent_usage__mutmut_68, 
    'x__detect_inconsistent_usage__mutmut_69': x__detect_inconsistent_usage__mutmut_69, 
    'x__detect_inconsistent_usage__mutmut_70': x__detect_inconsistent_usage__mutmut_70, 
    'x__detect_inconsistent_usage__mutmut_71': x__detect_inconsistent_usage__mutmut_71, 
    'x__detect_inconsistent_usage__mutmut_72': x__detect_inconsistent_usage__mutmut_72, 
    'x__detect_inconsistent_usage__mutmut_73': x__detect_inconsistent_usage__mutmut_73, 
    'x__detect_inconsistent_usage__mutmut_74': x__detect_inconsistent_usage__mutmut_74, 
    'x__detect_inconsistent_usage__mutmut_75': x__detect_inconsistent_usage__mutmut_75, 
    'x__detect_inconsistent_usage__mutmut_76': x__detect_inconsistent_usage__mutmut_76, 
    'x__detect_inconsistent_usage__mutmut_77': x__detect_inconsistent_usage__mutmut_77, 
    'x__detect_inconsistent_usage__mutmut_78': x__detect_inconsistent_usage__mutmut_78, 
    'x__detect_inconsistent_usage__mutmut_79': x__detect_inconsistent_usage__mutmut_79, 
    'x__detect_inconsistent_usage__mutmut_80': x__detect_inconsistent_usage__mutmut_80, 
    'x__detect_inconsistent_usage__mutmut_81': x__detect_inconsistent_usage__mutmut_81, 
    'x__detect_inconsistent_usage__mutmut_82': x__detect_inconsistent_usage__mutmut_82, 
    'x__detect_inconsistent_usage__mutmut_83': x__detect_inconsistent_usage__mutmut_83, 
    'x__detect_inconsistent_usage__mutmut_84': x__detect_inconsistent_usage__mutmut_84, 
    'x__detect_inconsistent_usage__mutmut_85': x__detect_inconsistent_usage__mutmut_85, 
    'x__detect_inconsistent_usage__mutmut_86': x__detect_inconsistent_usage__mutmut_86, 
    'x__detect_inconsistent_usage__mutmut_87': x__detect_inconsistent_usage__mutmut_87, 
    'x__detect_inconsistent_usage__mutmut_88': x__detect_inconsistent_usage__mutmut_88, 
    'x__detect_inconsistent_usage__mutmut_89': x__detect_inconsistent_usage__mutmut_89, 
    'x__detect_inconsistent_usage__mutmut_90': x__detect_inconsistent_usage__mutmut_90, 
    'x__detect_inconsistent_usage__mutmut_91': x__detect_inconsistent_usage__mutmut_91, 
    'x__detect_inconsistent_usage__mutmut_92': x__detect_inconsistent_usage__mutmut_92, 
    'x__detect_inconsistent_usage__mutmut_93': x__detect_inconsistent_usage__mutmut_93, 
    'x__detect_inconsistent_usage__mutmut_94': x__detect_inconsistent_usage__mutmut_94, 
    'x__detect_inconsistent_usage__mutmut_95': x__detect_inconsistent_usage__mutmut_95, 
    'x__detect_inconsistent_usage__mutmut_96': x__detect_inconsistent_usage__mutmut_96, 
    'x__detect_inconsistent_usage__mutmut_97': x__detect_inconsistent_usage__mutmut_97, 
    'x__detect_inconsistent_usage__mutmut_98': x__detect_inconsistent_usage__mutmut_98, 
    'x__detect_inconsistent_usage__mutmut_99': x__detect_inconsistent_usage__mutmut_99, 
    'x__detect_inconsistent_usage__mutmut_100': x__detect_inconsistent_usage__mutmut_100, 
    'x__detect_inconsistent_usage__mutmut_101': x__detect_inconsistent_usage__mutmut_101, 
    'x__detect_inconsistent_usage__mutmut_102': x__detect_inconsistent_usage__mutmut_102, 
    'x__detect_inconsistent_usage__mutmut_103': x__detect_inconsistent_usage__mutmut_103, 
    'x__detect_inconsistent_usage__mutmut_104': x__detect_inconsistent_usage__mutmut_104, 
    'x__detect_inconsistent_usage__mutmut_105': x__detect_inconsistent_usage__mutmut_105, 
    'x__detect_inconsistent_usage__mutmut_106': x__detect_inconsistent_usage__mutmut_106, 
    'x__detect_inconsistent_usage__mutmut_107': x__detect_inconsistent_usage__mutmut_107, 
    'x__detect_inconsistent_usage__mutmut_108': x__detect_inconsistent_usage__mutmut_108, 
    'x__detect_inconsistent_usage__mutmut_109': x__detect_inconsistent_usage__mutmut_109, 
    'x__detect_inconsistent_usage__mutmut_110': x__detect_inconsistent_usage__mutmut_110, 
    'x__detect_inconsistent_usage__mutmut_111': x__detect_inconsistent_usage__mutmut_111, 
    'x__detect_inconsistent_usage__mutmut_112': x__detect_inconsistent_usage__mutmut_112
}
x__detect_inconsistent_usage__mutmut_orig.__name__ = 'x__detect_inconsistent_usage'


def score_severity(
    conflict_type: ConflictType,
    confidence: float,
    is_critical_step: bool = False,
) -> Severity:
    args = [conflict_type, confidence, is_critical_step]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_score_severity__mutmut_orig, x_score_severity__mutmut_mutants, args, kwargs, None)


def x_score_severity__mutmut_orig(
    conflict_type: ConflictType,
    confidence: float,
    is_critical_step: bool = False,
) -> Severity:
    """Score severity based on conflict type, confidence, and step criticality.

    Args:
        conflict_type: Type of conflict detected
        confidence: Extraction confidence (0.0-1.0)
        is_critical_step: Whether the step is marked critical

    Returns:
        Severity level (LOW, MEDIUM, HIGH)

    Scoring matrix:
        - HIGH: (critical step + low confidence) OR ambiguous conflict
        - MEDIUM: (non-critical + ambiguous) OR (unknown + medium confidence)
        - LOW: (inconsistent) OR (unknown + high confidence)

    Examples:
        >>> score_severity(ConflictType.AMBIGUOUS, 0.5, True)
        Severity.HIGH
        >>> score_severity(ConflictType.UNKNOWN, 0.9, False)
        Severity.LOW
        >>> score_severity(ConflictType.UNKNOWN, 0.5, False)
        Severity.MEDIUM
    """
    # Ambiguous conflicts are always high severity if critical step
    if conflict_type == ConflictType.AMBIGUOUS:
        if is_critical_step:
            return Severity.HIGH
        else:
            return Severity.MEDIUM

    # Unknown terms scored by confidence
    elif conflict_type == ConflictType.UNKNOWN:
        if confidence >= 0.8:
            return Severity.LOW  # High confidence unknown (likely safe)
        elif confidence >= 0.5:
            return Severity.MEDIUM  # Medium confidence unknown
        else:
            if is_critical_step:
                return Severity.HIGH  # Low confidence in critical step
            else:
                return Severity.MEDIUM

    # Inconsistent usage (WP06)
    elif conflict_type == ConflictType.INCONSISTENT:
        return Severity.LOW  # Non-blocking, informational

    # Unresolved critical (WP06)
    elif conflict_type == ConflictType.UNRESOLVED_CRITICAL:
        return Severity.HIGH  # Always high severity

    # Default fallback
    return Severity.MEDIUM


def x_score_severity__mutmut_1(
    conflict_type: ConflictType,
    confidence: float,
    is_critical_step: bool = True,
) -> Severity:
    """Score severity based on conflict type, confidence, and step criticality.

    Args:
        conflict_type: Type of conflict detected
        confidence: Extraction confidence (0.0-1.0)
        is_critical_step: Whether the step is marked critical

    Returns:
        Severity level (LOW, MEDIUM, HIGH)

    Scoring matrix:
        - HIGH: (critical step + low confidence) OR ambiguous conflict
        - MEDIUM: (non-critical + ambiguous) OR (unknown + medium confidence)
        - LOW: (inconsistent) OR (unknown + high confidence)

    Examples:
        >>> score_severity(ConflictType.AMBIGUOUS, 0.5, True)
        Severity.HIGH
        >>> score_severity(ConflictType.UNKNOWN, 0.9, False)
        Severity.LOW
        >>> score_severity(ConflictType.UNKNOWN, 0.5, False)
        Severity.MEDIUM
    """
    # Ambiguous conflicts are always high severity if critical step
    if conflict_type == ConflictType.AMBIGUOUS:
        if is_critical_step:
            return Severity.HIGH
        else:
            return Severity.MEDIUM

    # Unknown terms scored by confidence
    elif conflict_type == ConflictType.UNKNOWN:
        if confidence >= 0.8:
            return Severity.LOW  # High confidence unknown (likely safe)
        elif confidence >= 0.5:
            return Severity.MEDIUM  # Medium confidence unknown
        else:
            if is_critical_step:
                return Severity.HIGH  # Low confidence in critical step
            else:
                return Severity.MEDIUM

    # Inconsistent usage (WP06)
    elif conflict_type == ConflictType.INCONSISTENT:
        return Severity.LOW  # Non-blocking, informational

    # Unresolved critical (WP06)
    elif conflict_type == ConflictType.UNRESOLVED_CRITICAL:
        return Severity.HIGH  # Always high severity

    # Default fallback
    return Severity.MEDIUM


def x_score_severity__mutmut_2(
    conflict_type: ConflictType,
    confidence: float,
    is_critical_step: bool = False,
) -> Severity:
    """Score severity based on conflict type, confidence, and step criticality.

    Args:
        conflict_type: Type of conflict detected
        confidence: Extraction confidence (0.0-1.0)
        is_critical_step: Whether the step is marked critical

    Returns:
        Severity level (LOW, MEDIUM, HIGH)

    Scoring matrix:
        - HIGH: (critical step + low confidence) OR ambiguous conflict
        - MEDIUM: (non-critical + ambiguous) OR (unknown + medium confidence)
        - LOW: (inconsistent) OR (unknown + high confidence)

    Examples:
        >>> score_severity(ConflictType.AMBIGUOUS, 0.5, True)
        Severity.HIGH
        >>> score_severity(ConflictType.UNKNOWN, 0.9, False)
        Severity.LOW
        >>> score_severity(ConflictType.UNKNOWN, 0.5, False)
        Severity.MEDIUM
    """
    # Ambiguous conflicts are always high severity if critical step
    if conflict_type != ConflictType.AMBIGUOUS:
        if is_critical_step:
            return Severity.HIGH
        else:
            return Severity.MEDIUM

    # Unknown terms scored by confidence
    elif conflict_type == ConflictType.UNKNOWN:
        if confidence >= 0.8:
            return Severity.LOW  # High confidence unknown (likely safe)
        elif confidence >= 0.5:
            return Severity.MEDIUM  # Medium confidence unknown
        else:
            if is_critical_step:
                return Severity.HIGH  # Low confidence in critical step
            else:
                return Severity.MEDIUM

    # Inconsistent usage (WP06)
    elif conflict_type == ConflictType.INCONSISTENT:
        return Severity.LOW  # Non-blocking, informational

    # Unresolved critical (WP06)
    elif conflict_type == ConflictType.UNRESOLVED_CRITICAL:
        return Severity.HIGH  # Always high severity

    # Default fallback
    return Severity.MEDIUM


def x_score_severity__mutmut_3(
    conflict_type: ConflictType,
    confidence: float,
    is_critical_step: bool = False,
) -> Severity:
    """Score severity based on conflict type, confidence, and step criticality.

    Args:
        conflict_type: Type of conflict detected
        confidence: Extraction confidence (0.0-1.0)
        is_critical_step: Whether the step is marked critical

    Returns:
        Severity level (LOW, MEDIUM, HIGH)

    Scoring matrix:
        - HIGH: (critical step + low confidence) OR ambiguous conflict
        - MEDIUM: (non-critical + ambiguous) OR (unknown + medium confidence)
        - LOW: (inconsistent) OR (unknown + high confidence)

    Examples:
        >>> score_severity(ConflictType.AMBIGUOUS, 0.5, True)
        Severity.HIGH
        >>> score_severity(ConflictType.UNKNOWN, 0.9, False)
        Severity.LOW
        >>> score_severity(ConflictType.UNKNOWN, 0.5, False)
        Severity.MEDIUM
    """
    # Ambiguous conflicts are always high severity if critical step
    if conflict_type == ConflictType.AMBIGUOUS:
        if is_critical_step:
            return Severity.HIGH
        else:
            return Severity.MEDIUM

    # Unknown terms scored by confidence
    elif conflict_type != ConflictType.UNKNOWN:
        if confidence >= 0.8:
            return Severity.LOW  # High confidence unknown (likely safe)
        elif confidence >= 0.5:
            return Severity.MEDIUM  # Medium confidence unknown
        else:
            if is_critical_step:
                return Severity.HIGH  # Low confidence in critical step
            else:
                return Severity.MEDIUM

    # Inconsistent usage (WP06)
    elif conflict_type == ConflictType.INCONSISTENT:
        return Severity.LOW  # Non-blocking, informational

    # Unresolved critical (WP06)
    elif conflict_type == ConflictType.UNRESOLVED_CRITICAL:
        return Severity.HIGH  # Always high severity

    # Default fallback
    return Severity.MEDIUM


def x_score_severity__mutmut_4(
    conflict_type: ConflictType,
    confidence: float,
    is_critical_step: bool = False,
) -> Severity:
    """Score severity based on conflict type, confidence, and step criticality.

    Args:
        conflict_type: Type of conflict detected
        confidence: Extraction confidence (0.0-1.0)
        is_critical_step: Whether the step is marked critical

    Returns:
        Severity level (LOW, MEDIUM, HIGH)

    Scoring matrix:
        - HIGH: (critical step + low confidence) OR ambiguous conflict
        - MEDIUM: (non-critical + ambiguous) OR (unknown + medium confidence)
        - LOW: (inconsistent) OR (unknown + high confidence)

    Examples:
        >>> score_severity(ConflictType.AMBIGUOUS, 0.5, True)
        Severity.HIGH
        >>> score_severity(ConflictType.UNKNOWN, 0.9, False)
        Severity.LOW
        >>> score_severity(ConflictType.UNKNOWN, 0.5, False)
        Severity.MEDIUM
    """
    # Ambiguous conflicts are always high severity if critical step
    if conflict_type == ConflictType.AMBIGUOUS:
        if is_critical_step:
            return Severity.HIGH
        else:
            return Severity.MEDIUM

    # Unknown terms scored by confidence
    elif conflict_type == ConflictType.UNKNOWN:
        if confidence > 0.8:
            return Severity.LOW  # High confidence unknown (likely safe)
        elif confidence >= 0.5:
            return Severity.MEDIUM  # Medium confidence unknown
        else:
            if is_critical_step:
                return Severity.HIGH  # Low confidence in critical step
            else:
                return Severity.MEDIUM

    # Inconsistent usage (WP06)
    elif conflict_type == ConflictType.INCONSISTENT:
        return Severity.LOW  # Non-blocking, informational

    # Unresolved critical (WP06)
    elif conflict_type == ConflictType.UNRESOLVED_CRITICAL:
        return Severity.HIGH  # Always high severity

    # Default fallback
    return Severity.MEDIUM


def x_score_severity__mutmut_5(
    conflict_type: ConflictType,
    confidence: float,
    is_critical_step: bool = False,
) -> Severity:
    """Score severity based on conflict type, confidence, and step criticality.

    Args:
        conflict_type: Type of conflict detected
        confidence: Extraction confidence (0.0-1.0)
        is_critical_step: Whether the step is marked critical

    Returns:
        Severity level (LOW, MEDIUM, HIGH)

    Scoring matrix:
        - HIGH: (critical step + low confidence) OR ambiguous conflict
        - MEDIUM: (non-critical + ambiguous) OR (unknown + medium confidence)
        - LOW: (inconsistent) OR (unknown + high confidence)

    Examples:
        >>> score_severity(ConflictType.AMBIGUOUS, 0.5, True)
        Severity.HIGH
        >>> score_severity(ConflictType.UNKNOWN, 0.9, False)
        Severity.LOW
        >>> score_severity(ConflictType.UNKNOWN, 0.5, False)
        Severity.MEDIUM
    """
    # Ambiguous conflicts are always high severity if critical step
    if conflict_type == ConflictType.AMBIGUOUS:
        if is_critical_step:
            return Severity.HIGH
        else:
            return Severity.MEDIUM

    # Unknown terms scored by confidence
    elif conflict_type == ConflictType.UNKNOWN:
        if confidence >= 1.8:
            return Severity.LOW  # High confidence unknown (likely safe)
        elif confidence >= 0.5:
            return Severity.MEDIUM  # Medium confidence unknown
        else:
            if is_critical_step:
                return Severity.HIGH  # Low confidence in critical step
            else:
                return Severity.MEDIUM

    # Inconsistent usage (WP06)
    elif conflict_type == ConflictType.INCONSISTENT:
        return Severity.LOW  # Non-blocking, informational

    # Unresolved critical (WP06)
    elif conflict_type == ConflictType.UNRESOLVED_CRITICAL:
        return Severity.HIGH  # Always high severity

    # Default fallback
    return Severity.MEDIUM


def x_score_severity__mutmut_6(
    conflict_type: ConflictType,
    confidence: float,
    is_critical_step: bool = False,
) -> Severity:
    """Score severity based on conflict type, confidence, and step criticality.

    Args:
        conflict_type: Type of conflict detected
        confidence: Extraction confidence (0.0-1.0)
        is_critical_step: Whether the step is marked critical

    Returns:
        Severity level (LOW, MEDIUM, HIGH)

    Scoring matrix:
        - HIGH: (critical step + low confidence) OR ambiguous conflict
        - MEDIUM: (non-critical + ambiguous) OR (unknown + medium confidence)
        - LOW: (inconsistent) OR (unknown + high confidence)

    Examples:
        >>> score_severity(ConflictType.AMBIGUOUS, 0.5, True)
        Severity.HIGH
        >>> score_severity(ConflictType.UNKNOWN, 0.9, False)
        Severity.LOW
        >>> score_severity(ConflictType.UNKNOWN, 0.5, False)
        Severity.MEDIUM
    """
    # Ambiguous conflicts are always high severity if critical step
    if conflict_type == ConflictType.AMBIGUOUS:
        if is_critical_step:
            return Severity.HIGH
        else:
            return Severity.MEDIUM

    # Unknown terms scored by confidence
    elif conflict_type == ConflictType.UNKNOWN:
        if confidence >= 0.8:
            return Severity.LOW  # High confidence unknown (likely safe)
        elif confidence > 0.5:
            return Severity.MEDIUM  # Medium confidence unknown
        else:
            if is_critical_step:
                return Severity.HIGH  # Low confidence in critical step
            else:
                return Severity.MEDIUM

    # Inconsistent usage (WP06)
    elif conflict_type == ConflictType.INCONSISTENT:
        return Severity.LOW  # Non-blocking, informational

    # Unresolved critical (WP06)
    elif conflict_type == ConflictType.UNRESOLVED_CRITICAL:
        return Severity.HIGH  # Always high severity

    # Default fallback
    return Severity.MEDIUM


def x_score_severity__mutmut_7(
    conflict_type: ConflictType,
    confidence: float,
    is_critical_step: bool = False,
) -> Severity:
    """Score severity based on conflict type, confidence, and step criticality.

    Args:
        conflict_type: Type of conflict detected
        confidence: Extraction confidence (0.0-1.0)
        is_critical_step: Whether the step is marked critical

    Returns:
        Severity level (LOW, MEDIUM, HIGH)

    Scoring matrix:
        - HIGH: (critical step + low confidence) OR ambiguous conflict
        - MEDIUM: (non-critical + ambiguous) OR (unknown + medium confidence)
        - LOW: (inconsistent) OR (unknown + high confidence)

    Examples:
        >>> score_severity(ConflictType.AMBIGUOUS, 0.5, True)
        Severity.HIGH
        >>> score_severity(ConflictType.UNKNOWN, 0.9, False)
        Severity.LOW
        >>> score_severity(ConflictType.UNKNOWN, 0.5, False)
        Severity.MEDIUM
    """
    # Ambiguous conflicts are always high severity if critical step
    if conflict_type == ConflictType.AMBIGUOUS:
        if is_critical_step:
            return Severity.HIGH
        else:
            return Severity.MEDIUM

    # Unknown terms scored by confidence
    elif conflict_type == ConflictType.UNKNOWN:
        if confidence >= 0.8:
            return Severity.LOW  # High confidence unknown (likely safe)
        elif confidence >= 1.5:
            return Severity.MEDIUM  # Medium confidence unknown
        else:
            if is_critical_step:
                return Severity.HIGH  # Low confidence in critical step
            else:
                return Severity.MEDIUM

    # Inconsistent usage (WP06)
    elif conflict_type == ConflictType.INCONSISTENT:
        return Severity.LOW  # Non-blocking, informational

    # Unresolved critical (WP06)
    elif conflict_type == ConflictType.UNRESOLVED_CRITICAL:
        return Severity.HIGH  # Always high severity

    # Default fallback
    return Severity.MEDIUM


def x_score_severity__mutmut_8(
    conflict_type: ConflictType,
    confidence: float,
    is_critical_step: bool = False,
) -> Severity:
    """Score severity based on conflict type, confidence, and step criticality.

    Args:
        conflict_type: Type of conflict detected
        confidence: Extraction confidence (0.0-1.0)
        is_critical_step: Whether the step is marked critical

    Returns:
        Severity level (LOW, MEDIUM, HIGH)

    Scoring matrix:
        - HIGH: (critical step + low confidence) OR ambiguous conflict
        - MEDIUM: (non-critical + ambiguous) OR (unknown + medium confidence)
        - LOW: (inconsistent) OR (unknown + high confidence)

    Examples:
        >>> score_severity(ConflictType.AMBIGUOUS, 0.5, True)
        Severity.HIGH
        >>> score_severity(ConflictType.UNKNOWN, 0.9, False)
        Severity.LOW
        >>> score_severity(ConflictType.UNKNOWN, 0.5, False)
        Severity.MEDIUM
    """
    # Ambiguous conflicts are always high severity if critical step
    if conflict_type == ConflictType.AMBIGUOUS:
        if is_critical_step:
            return Severity.HIGH
        else:
            return Severity.MEDIUM

    # Unknown terms scored by confidence
    elif conflict_type == ConflictType.UNKNOWN:
        if confidence >= 0.8:
            return Severity.LOW  # High confidence unknown (likely safe)
        elif confidence >= 0.5:
            return Severity.MEDIUM  # Medium confidence unknown
        else:
            if is_critical_step:
                return Severity.HIGH  # Low confidence in critical step
            else:
                return Severity.MEDIUM

    # Inconsistent usage (WP06)
    elif conflict_type != ConflictType.INCONSISTENT:
        return Severity.LOW  # Non-blocking, informational

    # Unresolved critical (WP06)
    elif conflict_type == ConflictType.UNRESOLVED_CRITICAL:
        return Severity.HIGH  # Always high severity

    # Default fallback
    return Severity.MEDIUM


def x_score_severity__mutmut_9(
    conflict_type: ConflictType,
    confidence: float,
    is_critical_step: bool = False,
) -> Severity:
    """Score severity based on conflict type, confidence, and step criticality.

    Args:
        conflict_type: Type of conflict detected
        confidence: Extraction confidence (0.0-1.0)
        is_critical_step: Whether the step is marked critical

    Returns:
        Severity level (LOW, MEDIUM, HIGH)

    Scoring matrix:
        - HIGH: (critical step + low confidence) OR ambiguous conflict
        - MEDIUM: (non-critical + ambiguous) OR (unknown + medium confidence)
        - LOW: (inconsistent) OR (unknown + high confidence)

    Examples:
        >>> score_severity(ConflictType.AMBIGUOUS, 0.5, True)
        Severity.HIGH
        >>> score_severity(ConflictType.UNKNOWN, 0.9, False)
        Severity.LOW
        >>> score_severity(ConflictType.UNKNOWN, 0.5, False)
        Severity.MEDIUM
    """
    # Ambiguous conflicts are always high severity if critical step
    if conflict_type == ConflictType.AMBIGUOUS:
        if is_critical_step:
            return Severity.HIGH
        else:
            return Severity.MEDIUM

    # Unknown terms scored by confidence
    elif conflict_type == ConflictType.UNKNOWN:
        if confidence >= 0.8:
            return Severity.LOW  # High confidence unknown (likely safe)
        elif confidence >= 0.5:
            return Severity.MEDIUM  # Medium confidence unknown
        else:
            if is_critical_step:
                return Severity.HIGH  # Low confidence in critical step
            else:
                return Severity.MEDIUM

    # Inconsistent usage (WP06)
    elif conflict_type == ConflictType.INCONSISTENT:
        return Severity.LOW  # Non-blocking, informational

    # Unresolved critical (WP06)
    elif conflict_type != ConflictType.UNRESOLVED_CRITICAL:
        return Severity.HIGH  # Always high severity

    # Default fallback
    return Severity.MEDIUM

x_score_severity__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_score_severity__mutmut_1': x_score_severity__mutmut_1, 
    'x_score_severity__mutmut_2': x_score_severity__mutmut_2, 
    'x_score_severity__mutmut_3': x_score_severity__mutmut_3, 
    'x_score_severity__mutmut_4': x_score_severity__mutmut_4, 
    'x_score_severity__mutmut_5': x_score_severity__mutmut_5, 
    'x_score_severity__mutmut_6': x_score_severity__mutmut_6, 
    'x_score_severity__mutmut_7': x_score_severity__mutmut_7, 
    'x_score_severity__mutmut_8': x_score_severity__mutmut_8, 
    'x_score_severity__mutmut_9': x_score_severity__mutmut_9
}
x_score_severity__mutmut_orig.__name__ = 'x_score_severity'


def make_sense_ref(sense: TermSense) -> SenseRef:
    args = [sense]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_make_sense_ref__mutmut_orig, x_make_sense_ref__mutmut_mutants, args, kwargs, None)


def x_make_sense_ref__mutmut_orig(sense: TermSense) -> SenseRef:
    """Convert TermSense to SenseRef for conflict reporting.

    Args:
        sense: TermSense to convert

    Returns:
        SenseRef with essential fields (surface, scope, definition, confidence)
    """
    return SenseRef(
        surface=sense.surface.surface_text,
        scope=sense.scope,
        definition=sense.definition,
        confidence=sense.confidence,
    )


def x_make_sense_ref__mutmut_1(sense: TermSense) -> SenseRef:
    """Convert TermSense to SenseRef for conflict reporting.

    Args:
        sense: TermSense to convert

    Returns:
        SenseRef with essential fields (surface, scope, definition, confidence)
    """
    return SenseRef(
        surface=None,
        scope=sense.scope,
        definition=sense.definition,
        confidence=sense.confidence,
    )


def x_make_sense_ref__mutmut_2(sense: TermSense) -> SenseRef:
    """Convert TermSense to SenseRef for conflict reporting.

    Args:
        sense: TermSense to convert

    Returns:
        SenseRef with essential fields (surface, scope, definition, confidence)
    """
    return SenseRef(
        surface=sense.surface.surface_text,
        scope=None,
        definition=sense.definition,
        confidence=sense.confidence,
    )


def x_make_sense_ref__mutmut_3(sense: TermSense) -> SenseRef:
    """Convert TermSense to SenseRef for conflict reporting.

    Args:
        sense: TermSense to convert

    Returns:
        SenseRef with essential fields (surface, scope, definition, confidence)
    """
    return SenseRef(
        surface=sense.surface.surface_text,
        scope=sense.scope,
        definition=None,
        confidence=sense.confidence,
    )


def x_make_sense_ref__mutmut_4(sense: TermSense) -> SenseRef:
    """Convert TermSense to SenseRef for conflict reporting.

    Args:
        sense: TermSense to convert

    Returns:
        SenseRef with essential fields (surface, scope, definition, confidence)
    """
    return SenseRef(
        surface=sense.surface.surface_text,
        scope=sense.scope,
        definition=sense.definition,
        confidence=None,
    )


def x_make_sense_ref__mutmut_5(sense: TermSense) -> SenseRef:
    """Convert TermSense to SenseRef for conflict reporting.

    Args:
        sense: TermSense to convert

    Returns:
        SenseRef with essential fields (surface, scope, definition, confidence)
    """
    return SenseRef(
        scope=sense.scope,
        definition=sense.definition,
        confidence=sense.confidence,
    )


def x_make_sense_ref__mutmut_6(sense: TermSense) -> SenseRef:
    """Convert TermSense to SenseRef for conflict reporting.

    Args:
        sense: TermSense to convert

    Returns:
        SenseRef with essential fields (surface, scope, definition, confidence)
    """
    return SenseRef(
        surface=sense.surface.surface_text,
        definition=sense.definition,
        confidence=sense.confidence,
    )


def x_make_sense_ref__mutmut_7(sense: TermSense) -> SenseRef:
    """Convert TermSense to SenseRef for conflict reporting.

    Args:
        sense: TermSense to convert

    Returns:
        SenseRef with essential fields (surface, scope, definition, confidence)
    """
    return SenseRef(
        surface=sense.surface.surface_text,
        scope=sense.scope,
        confidence=sense.confidence,
    )


def x_make_sense_ref__mutmut_8(sense: TermSense) -> SenseRef:
    """Convert TermSense to SenseRef for conflict reporting.

    Args:
        sense: TermSense to convert

    Returns:
        SenseRef with essential fields (surface, scope, definition, confidence)
    """
    return SenseRef(
        surface=sense.surface.surface_text,
        scope=sense.scope,
        definition=sense.definition,
        )

x_make_sense_ref__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_make_sense_ref__mutmut_1': x_make_sense_ref__mutmut_1, 
    'x_make_sense_ref__mutmut_2': x_make_sense_ref__mutmut_2, 
    'x_make_sense_ref__mutmut_3': x_make_sense_ref__mutmut_3, 
    'x_make_sense_ref__mutmut_4': x_make_sense_ref__mutmut_4, 
    'x_make_sense_ref__mutmut_5': x_make_sense_ref__mutmut_5, 
    'x_make_sense_ref__mutmut_6': x_make_sense_ref__mutmut_6, 
    'x_make_sense_ref__mutmut_7': x_make_sense_ref__mutmut_7, 
    'x_make_sense_ref__mutmut_8': x_make_sense_ref__mutmut_8
}
x_make_sense_ref__mutmut_orig.__name__ = 'x_make_sense_ref'


def create_conflict(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    args = [term, conflict_type, severity, candidate_senses, context]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_create_conflict__mutmut_orig, x_create_conflict__mutmut_mutants, args, kwargs, None)


def x_create_conflict__mutmut_orig(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(term.surface),
        conflict_type=conflict_type,
        severity=severity,
        confidence=term.confidence,
        candidate_senses=[make_sense_ref(s) for s in candidate_senses],
        context=context,
    )


def x_create_conflict__mutmut_1(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "XXXX",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(term.surface),
        conflict_type=conflict_type,
        severity=severity,
        confidence=term.confidence,
        candidate_senses=[make_sense_ref(s) for s in candidate_senses],
        context=context,
    )


def x_create_conflict__mutmut_2(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=None,
        conflict_type=conflict_type,
        severity=severity,
        confidence=term.confidence,
        candidate_senses=[make_sense_ref(s) for s in candidate_senses],
        context=context,
    )


def x_create_conflict__mutmut_3(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(term.surface),
        conflict_type=None,
        severity=severity,
        confidence=term.confidence,
        candidate_senses=[make_sense_ref(s) for s in candidate_senses],
        context=context,
    )


def x_create_conflict__mutmut_4(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(term.surface),
        conflict_type=conflict_type,
        severity=None,
        confidence=term.confidence,
        candidate_senses=[make_sense_ref(s) for s in candidate_senses],
        context=context,
    )


def x_create_conflict__mutmut_5(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(term.surface),
        conflict_type=conflict_type,
        severity=severity,
        confidence=None,
        candidate_senses=[make_sense_ref(s) for s in candidate_senses],
        context=context,
    )


def x_create_conflict__mutmut_6(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(term.surface),
        conflict_type=conflict_type,
        severity=severity,
        confidence=term.confidence,
        candidate_senses=None,
        context=context,
    )


def x_create_conflict__mutmut_7(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(term.surface),
        conflict_type=conflict_type,
        severity=severity,
        confidence=term.confidence,
        candidate_senses=[make_sense_ref(s) for s in candidate_senses],
        context=None,
    )


def x_create_conflict__mutmut_8(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        conflict_type=conflict_type,
        severity=severity,
        confidence=term.confidence,
        candidate_senses=[make_sense_ref(s) for s in candidate_senses],
        context=context,
    )


def x_create_conflict__mutmut_9(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(term.surface),
        severity=severity,
        confidence=term.confidence,
        candidate_senses=[make_sense_ref(s) for s in candidate_senses],
        context=context,
    )


def x_create_conflict__mutmut_10(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(term.surface),
        conflict_type=conflict_type,
        confidence=term.confidence,
        candidate_senses=[make_sense_ref(s) for s in candidate_senses],
        context=context,
    )


def x_create_conflict__mutmut_11(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(term.surface),
        conflict_type=conflict_type,
        severity=severity,
        candidate_senses=[make_sense_ref(s) for s in candidate_senses],
        context=context,
    )


def x_create_conflict__mutmut_12(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(term.surface),
        conflict_type=conflict_type,
        severity=severity,
        confidence=term.confidence,
        context=context,
    )


def x_create_conflict__mutmut_13(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(term.surface),
        conflict_type=conflict_type,
        severity=severity,
        confidence=term.confidence,
        candidate_senses=[make_sense_ref(s) for s in candidate_senses],
        )


def x_create_conflict__mutmut_14(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(None),
        conflict_type=conflict_type,
        severity=severity,
        confidence=term.confidence,
        candidate_senses=[make_sense_ref(s) for s in candidate_senses],
        context=context,
    )


def x_create_conflict__mutmut_15(
    term: ExtractedTerm,
    conflict_type: ConflictType,
    severity: Severity,
    candidate_senses: List[TermSense],
    context: str = "",
) -> "models.SemanticConflict":
    """Create a SemanticConflict from classification results.

    Args:
        term: Extracted term that has a conflict
        conflict_type: Type of conflict detected
        severity: Severity score
        candidate_senses: List of matching TermSense objects
        context: Usage context (e.g., "step input: description field")

    Returns:
        SemanticConflict with all fields populated
    """
    from . import models

    return models.SemanticConflict(
        term=TermSurface(term.surface),
        conflict_type=conflict_type,
        severity=severity,
        confidence=term.confidence,
        candidate_senses=[make_sense_ref(None) for s in candidate_senses],
        context=context,
    )

x_create_conflict__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_create_conflict__mutmut_1': x_create_conflict__mutmut_1, 
    'x_create_conflict__mutmut_2': x_create_conflict__mutmut_2, 
    'x_create_conflict__mutmut_3': x_create_conflict__mutmut_3, 
    'x_create_conflict__mutmut_4': x_create_conflict__mutmut_4, 
    'x_create_conflict__mutmut_5': x_create_conflict__mutmut_5, 
    'x_create_conflict__mutmut_6': x_create_conflict__mutmut_6, 
    'x_create_conflict__mutmut_7': x_create_conflict__mutmut_7, 
    'x_create_conflict__mutmut_8': x_create_conflict__mutmut_8, 
    'x_create_conflict__mutmut_9': x_create_conflict__mutmut_9, 
    'x_create_conflict__mutmut_10': x_create_conflict__mutmut_10, 
    'x_create_conflict__mutmut_11': x_create_conflict__mutmut_11, 
    'x_create_conflict__mutmut_12': x_create_conflict__mutmut_12, 
    'x_create_conflict__mutmut_13': x_create_conflict__mutmut_13, 
    'x_create_conflict__mutmut_14': x_create_conflict__mutmut_14, 
    'x_create_conflict__mutmut_15': x_create_conflict__mutmut_15
}
x_create_conflict__mutmut_orig.__name__ = 'x_create_conflict'
