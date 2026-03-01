"""Conflict rendering with Rich (WP06/T025).

This module implements Rich-based rendering for semantic conflicts,
displaying ranked candidate senses with color-coded severity.
"""

import logging
from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .models import Severity, SemanticConflict, SenseRef

logger = logging.getLogger(__name__)

SEVERITY_COLORS: dict[Severity, str] = {
    Severity.HIGH: "red",
    Severity.MEDIUM: "yellow",
    Severity.LOW: "blue",
}

SEVERITY_ICONS: dict[Severity, str] = {
    Severity.HIGH: "\U0001f534",
    Severity.MEDIUM: "\U0001f7e1",
    Severity.LOW: "\U0001f535",
}

# Scope precedence map: lower number = higher precedence (shown first)
SCOPE_PRECEDENCE: dict[str, int] = {
    "mission_local": 0,
    "team_domain": 1,
    "audience_domain": 2,
    "spec_kitty_core": 3,
}
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


def sort_candidates(candidates: List[SenseRef]) -> List[SenseRef]:
    args = [candidates]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_sort_candidates__mutmut_orig, x_sort_candidates__mutmut_mutants, args, kwargs, None)


def x_sort_candidates__mutmut_orig(candidates: List[SenseRef]) -> List[SenseRef]:
    """Sort candidate senses by scope precedence then descending confidence.

    Candidates with scope precedence mission_local (0) appear first,
    then team_domain (1), audience_domain (2), spec_kitty_core (3).
    Within the same scope, higher confidence appears first.
    Unknown scopes are sorted after all known scopes.

    Args:
        candidates: List of SenseRef candidates to sort

    Returns:
        New sorted list (does not mutate input)
    """
    return sorted(
        candidates,
        key=lambda s: (SCOPE_PRECEDENCE.get(s.scope, 99), -s.confidence),
    )


def x_sort_candidates__mutmut_1(candidates: List[SenseRef]) -> List[SenseRef]:
    """Sort candidate senses by scope precedence then descending confidence.

    Candidates with scope precedence mission_local (0) appear first,
    then team_domain (1), audience_domain (2), spec_kitty_core (3).
    Within the same scope, higher confidence appears first.
    Unknown scopes are sorted after all known scopes.

    Args:
        candidates: List of SenseRef candidates to sort

    Returns:
        New sorted list (does not mutate input)
    """
    return sorted(
        None,
        key=lambda s: (SCOPE_PRECEDENCE.get(s.scope, 99), -s.confidence),
    )


def x_sort_candidates__mutmut_2(candidates: List[SenseRef]) -> List[SenseRef]:
    """Sort candidate senses by scope precedence then descending confidence.

    Candidates with scope precedence mission_local (0) appear first,
    then team_domain (1), audience_domain (2), spec_kitty_core (3).
    Within the same scope, higher confidence appears first.
    Unknown scopes are sorted after all known scopes.

    Args:
        candidates: List of SenseRef candidates to sort

    Returns:
        New sorted list (does not mutate input)
    """
    return sorted(
        candidates,
        key=None,
    )


def x_sort_candidates__mutmut_3(candidates: List[SenseRef]) -> List[SenseRef]:
    """Sort candidate senses by scope precedence then descending confidence.

    Candidates with scope precedence mission_local (0) appear first,
    then team_domain (1), audience_domain (2), spec_kitty_core (3).
    Within the same scope, higher confidence appears first.
    Unknown scopes are sorted after all known scopes.

    Args:
        candidates: List of SenseRef candidates to sort

    Returns:
        New sorted list (does not mutate input)
    """
    return sorted(
        key=lambda s: (SCOPE_PRECEDENCE.get(s.scope, 99), -s.confidence),
    )


def x_sort_candidates__mutmut_4(candidates: List[SenseRef]) -> List[SenseRef]:
    """Sort candidate senses by scope precedence then descending confidence.

    Candidates with scope precedence mission_local (0) appear first,
    then team_domain (1), audience_domain (2), spec_kitty_core (3).
    Within the same scope, higher confidence appears first.
    Unknown scopes are sorted after all known scopes.

    Args:
        candidates: List of SenseRef candidates to sort

    Returns:
        New sorted list (does not mutate input)
    """
    return sorted(
        candidates,
        )


def x_sort_candidates__mutmut_5(candidates: List[SenseRef]) -> List[SenseRef]:
    """Sort candidate senses by scope precedence then descending confidence.

    Candidates with scope precedence mission_local (0) appear first,
    then team_domain (1), audience_domain (2), spec_kitty_core (3).
    Within the same scope, higher confidence appears first.
    Unknown scopes are sorted after all known scopes.

    Args:
        candidates: List of SenseRef candidates to sort

    Returns:
        New sorted list (does not mutate input)
    """
    return sorted(
        candidates,
        key=lambda s: None,
    )


def x_sort_candidates__mutmut_6(candidates: List[SenseRef]) -> List[SenseRef]:
    """Sort candidate senses by scope precedence then descending confidence.

    Candidates with scope precedence mission_local (0) appear first,
    then team_domain (1), audience_domain (2), spec_kitty_core (3).
    Within the same scope, higher confidence appears first.
    Unknown scopes are sorted after all known scopes.

    Args:
        candidates: List of SenseRef candidates to sort

    Returns:
        New sorted list (does not mutate input)
    """
    return sorted(
        candidates,
        key=lambda s: (SCOPE_PRECEDENCE.get(None, 99), -s.confidence),
    )


def x_sort_candidates__mutmut_7(candidates: List[SenseRef]) -> List[SenseRef]:
    """Sort candidate senses by scope precedence then descending confidence.

    Candidates with scope precedence mission_local (0) appear first,
    then team_domain (1), audience_domain (2), spec_kitty_core (3).
    Within the same scope, higher confidence appears first.
    Unknown scopes are sorted after all known scopes.

    Args:
        candidates: List of SenseRef candidates to sort

    Returns:
        New sorted list (does not mutate input)
    """
    return sorted(
        candidates,
        key=lambda s: (SCOPE_PRECEDENCE.get(s.scope, None), -s.confidence),
    )


def x_sort_candidates__mutmut_8(candidates: List[SenseRef]) -> List[SenseRef]:
    """Sort candidate senses by scope precedence then descending confidence.

    Candidates with scope precedence mission_local (0) appear first,
    then team_domain (1), audience_domain (2), spec_kitty_core (3).
    Within the same scope, higher confidence appears first.
    Unknown scopes are sorted after all known scopes.

    Args:
        candidates: List of SenseRef candidates to sort

    Returns:
        New sorted list (does not mutate input)
    """
    return sorted(
        candidates,
        key=lambda s: (SCOPE_PRECEDENCE.get(99), -s.confidence),
    )


def x_sort_candidates__mutmut_9(candidates: List[SenseRef]) -> List[SenseRef]:
    """Sort candidate senses by scope precedence then descending confidence.

    Candidates with scope precedence mission_local (0) appear first,
    then team_domain (1), audience_domain (2), spec_kitty_core (3).
    Within the same scope, higher confidence appears first.
    Unknown scopes are sorted after all known scopes.

    Args:
        candidates: List of SenseRef candidates to sort

    Returns:
        New sorted list (does not mutate input)
    """
    return sorted(
        candidates,
        key=lambda s: (SCOPE_PRECEDENCE.get(s.scope, ), -s.confidence),
    )


def x_sort_candidates__mutmut_10(candidates: List[SenseRef]) -> List[SenseRef]:
    """Sort candidate senses by scope precedence then descending confidence.

    Candidates with scope precedence mission_local (0) appear first,
    then team_domain (1), audience_domain (2), spec_kitty_core (3).
    Within the same scope, higher confidence appears first.
    Unknown scopes are sorted after all known scopes.

    Args:
        candidates: List of SenseRef candidates to sort

    Returns:
        New sorted list (does not mutate input)
    """
    return sorted(
        candidates,
        key=lambda s: (SCOPE_PRECEDENCE.get(s.scope, 100), -s.confidence),
    )


def x_sort_candidates__mutmut_11(candidates: List[SenseRef]) -> List[SenseRef]:
    """Sort candidate senses by scope precedence then descending confidence.

    Candidates with scope precedence mission_local (0) appear first,
    then team_domain (1), audience_domain (2), spec_kitty_core (3).
    Within the same scope, higher confidence appears first.
    Unknown scopes are sorted after all known scopes.

    Args:
        candidates: List of SenseRef candidates to sort

    Returns:
        New sorted list (does not mutate input)
    """
    return sorted(
        candidates,
        key=lambda s: (SCOPE_PRECEDENCE.get(s.scope, 99), +s.confidence),
    )

x_sort_candidates__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_sort_candidates__mutmut_1': x_sort_candidates__mutmut_1, 
    'x_sort_candidates__mutmut_2': x_sort_candidates__mutmut_2, 
    'x_sort_candidates__mutmut_3': x_sort_candidates__mutmut_3, 
    'x_sort_candidates__mutmut_4': x_sort_candidates__mutmut_4, 
    'x_sort_candidates__mutmut_5': x_sort_candidates__mutmut_5, 
    'x_sort_candidates__mutmut_6': x_sort_candidates__mutmut_6, 
    'x_sort_candidates__mutmut_7': x_sort_candidates__mutmut_7, 
    'x_sort_candidates__mutmut_8': x_sort_candidates__mutmut_8, 
    'x_sort_candidates__mutmut_9': x_sort_candidates__mutmut_9, 
    'x_sort_candidates__mutmut_10': x_sort_candidates__mutmut_10, 
    'x_sort_candidates__mutmut_11': x_sort_candidates__mutmut_11
}
x_sort_candidates__mutmut_orig.__name__ = 'x_sort_candidates'


def _get_severity_color(severity: Severity) -> str:
    args = [severity]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__get_severity_color__mutmut_orig, x__get_severity_color__mutmut_mutants, args, kwargs, None)


def x__get_severity_color__mutmut_orig(severity: Severity) -> str:
    """Get color for severity, defaulting to white for unknown values."""
    color = SEVERITY_COLORS.get(severity)
    if color is None:
        logger.warning("Unknown severity level: %s, defaulting to white", severity)
        return "white"
    return color


def x__get_severity_color__mutmut_1(severity: Severity) -> str:
    """Get color for severity, defaulting to white for unknown values."""
    color = None
    if color is None:
        logger.warning("Unknown severity level: %s, defaulting to white", severity)
        return "white"
    return color


def x__get_severity_color__mutmut_2(severity: Severity) -> str:
    """Get color for severity, defaulting to white for unknown values."""
    color = SEVERITY_COLORS.get(None)
    if color is None:
        logger.warning("Unknown severity level: %s, defaulting to white", severity)
        return "white"
    return color


def x__get_severity_color__mutmut_3(severity: Severity) -> str:
    """Get color for severity, defaulting to white for unknown values."""
    color = SEVERITY_COLORS.get(severity)
    if color is not None:
        logger.warning("Unknown severity level: %s, defaulting to white", severity)
        return "white"
    return color


def x__get_severity_color__mutmut_4(severity: Severity) -> str:
    """Get color for severity, defaulting to white for unknown values."""
    color = SEVERITY_COLORS.get(severity)
    if color is None:
        logger.warning(None, severity)
        return "white"
    return color


def x__get_severity_color__mutmut_5(severity: Severity) -> str:
    """Get color for severity, defaulting to white for unknown values."""
    color = SEVERITY_COLORS.get(severity)
    if color is None:
        logger.warning("Unknown severity level: %s, defaulting to white", None)
        return "white"
    return color


def x__get_severity_color__mutmut_6(severity: Severity) -> str:
    """Get color for severity, defaulting to white for unknown values."""
    color = SEVERITY_COLORS.get(severity)
    if color is None:
        logger.warning(severity)
        return "white"
    return color


def x__get_severity_color__mutmut_7(severity: Severity) -> str:
    """Get color for severity, defaulting to white for unknown values."""
    color = SEVERITY_COLORS.get(severity)
    if color is None:
        logger.warning("Unknown severity level: %s, defaulting to white", )
        return "white"
    return color


def x__get_severity_color__mutmut_8(severity: Severity) -> str:
    """Get color for severity, defaulting to white for unknown values."""
    color = SEVERITY_COLORS.get(severity)
    if color is None:
        logger.warning("XXUnknown severity level: %s, defaulting to whiteXX", severity)
        return "white"
    return color


def x__get_severity_color__mutmut_9(severity: Severity) -> str:
    """Get color for severity, defaulting to white for unknown values."""
    color = SEVERITY_COLORS.get(severity)
    if color is None:
        logger.warning("unknown severity level: %s, defaulting to white", severity)
        return "white"
    return color


def x__get_severity_color__mutmut_10(severity: Severity) -> str:
    """Get color for severity, defaulting to white for unknown values."""
    color = SEVERITY_COLORS.get(severity)
    if color is None:
        logger.warning("UNKNOWN SEVERITY LEVEL: %S, DEFAULTING TO WHITE", severity)
        return "white"
    return color


def x__get_severity_color__mutmut_11(severity: Severity) -> str:
    """Get color for severity, defaulting to white for unknown values."""
    color = SEVERITY_COLORS.get(severity)
    if color is None:
        logger.warning("Unknown severity level: %s, defaulting to white", severity)
        return "XXwhiteXX"
    return color


def x__get_severity_color__mutmut_12(severity: Severity) -> str:
    """Get color for severity, defaulting to white for unknown values."""
    color = SEVERITY_COLORS.get(severity)
    if color is None:
        logger.warning("Unknown severity level: %s, defaulting to white", severity)
        return "WHITE"
    return color

x__get_severity_color__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__get_severity_color__mutmut_1': x__get_severity_color__mutmut_1, 
    'x__get_severity_color__mutmut_2': x__get_severity_color__mutmut_2, 
    'x__get_severity_color__mutmut_3': x__get_severity_color__mutmut_3, 
    'x__get_severity_color__mutmut_4': x__get_severity_color__mutmut_4, 
    'x__get_severity_color__mutmut_5': x__get_severity_color__mutmut_5, 
    'x__get_severity_color__mutmut_6': x__get_severity_color__mutmut_6, 
    'x__get_severity_color__mutmut_7': x__get_severity_color__mutmut_7, 
    'x__get_severity_color__mutmut_8': x__get_severity_color__mutmut_8, 
    'x__get_severity_color__mutmut_9': x__get_severity_color__mutmut_9, 
    'x__get_severity_color__mutmut_10': x__get_severity_color__mutmut_10, 
    'x__get_severity_color__mutmut_11': x__get_severity_color__mutmut_11, 
    'x__get_severity_color__mutmut_12': x__get_severity_color__mutmut_12
}
x__get_severity_color__mutmut_orig.__name__ = 'x__get_severity_color'


def _get_severity_icon(severity: Severity) -> str:
    args = [severity]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__get_severity_icon__mutmut_orig, x__get_severity_icon__mutmut_mutants, args, kwargs, None)


def x__get_severity_icon__mutmut_orig(severity: Severity) -> str:
    """Get icon for severity, defaulting to '?' for unknown values."""
    icon = SEVERITY_ICONS.get(severity)
    if icon is None:
        logger.warning("Unknown severity level: %s, defaulting to '?'", severity)
        return "?"
    return icon


def x__get_severity_icon__mutmut_1(severity: Severity) -> str:
    """Get icon for severity, defaulting to '?' for unknown values."""
    icon = None
    if icon is None:
        logger.warning("Unknown severity level: %s, defaulting to '?'", severity)
        return "?"
    return icon


def x__get_severity_icon__mutmut_2(severity: Severity) -> str:
    """Get icon for severity, defaulting to '?' for unknown values."""
    icon = SEVERITY_ICONS.get(None)
    if icon is None:
        logger.warning("Unknown severity level: %s, defaulting to '?'", severity)
        return "?"
    return icon


def x__get_severity_icon__mutmut_3(severity: Severity) -> str:
    """Get icon for severity, defaulting to '?' for unknown values."""
    icon = SEVERITY_ICONS.get(severity)
    if icon is not None:
        logger.warning("Unknown severity level: %s, defaulting to '?'", severity)
        return "?"
    return icon


def x__get_severity_icon__mutmut_4(severity: Severity) -> str:
    """Get icon for severity, defaulting to '?' for unknown values."""
    icon = SEVERITY_ICONS.get(severity)
    if icon is None:
        logger.warning(None, severity)
        return "?"
    return icon


def x__get_severity_icon__mutmut_5(severity: Severity) -> str:
    """Get icon for severity, defaulting to '?' for unknown values."""
    icon = SEVERITY_ICONS.get(severity)
    if icon is None:
        logger.warning("Unknown severity level: %s, defaulting to '?'", None)
        return "?"
    return icon


def x__get_severity_icon__mutmut_6(severity: Severity) -> str:
    """Get icon for severity, defaulting to '?' for unknown values."""
    icon = SEVERITY_ICONS.get(severity)
    if icon is None:
        logger.warning(severity)
        return "?"
    return icon


def x__get_severity_icon__mutmut_7(severity: Severity) -> str:
    """Get icon for severity, defaulting to '?' for unknown values."""
    icon = SEVERITY_ICONS.get(severity)
    if icon is None:
        logger.warning("Unknown severity level: %s, defaulting to '?'", )
        return "?"
    return icon


def x__get_severity_icon__mutmut_8(severity: Severity) -> str:
    """Get icon for severity, defaulting to '?' for unknown values."""
    icon = SEVERITY_ICONS.get(severity)
    if icon is None:
        logger.warning("XXUnknown severity level: %s, defaulting to '?'XX", severity)
        return "?"
    return icon


def x__get_severity_icon__mutmut_9(severity: Severity) -> str:
    """Get icon for severity, defaulting to '?' for unknown values."""
    icon = SEVERITY_ICONS.get(severity)
    if icon is None:
        logger.warning("unknown severity level: %s, defaulting to '?'", severity)
        return "?"
    return icon


def x__get_severity_icon__mutmut_10(severity: Severity) -> str:
    """Get icon for severity, defaulting to '?' for unknown values."""
    icon = SEVERITY_ICONS.get(severity)
    if icon is None:
        logger.warning("UNKNOWN SEVERITY LEVEL: %S, DEFAULTING TO '?'", severity)
        return "?"
    return icon


def x__get_severity_icon__mutmut_11(severity: Severity) -> str:
    """Get icon for severity, defaulting to '?' for unknown values."""
    icon = SEVERITY_ICONS.get(severity)
    if icon is None:
        logger.warning("Unknown severity level: %s, defaulting to '?'", severity)
        return "XX?XX"
    return icon

x__get_severity_icon__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__get_severity_icon__mutmut_1': x__get_severity_icon__mutmut_1, 
    'x__get_severity_icon__mutmut_2': x__get_severity_icon__mutmut_2, 
    'x__get_severity_icon__mutmut_3': x__get_severity_icon__mutmut_3, 
    'x__get_severity_icon__mutmut_4': x__get_severity_icon__mutmut_4, 
    'x__get_severity_icon__mutmut_5': x__get_severity_icon__mutmut_5, 
    'x__get_severity_icon__mutmut_6': x__get_severity_icon__mutmut_6, 
    'x__get_severity_icon__mutmut_7': x__get_severity_icon__mutmut_7, 
    'x__get_severity_icon__mutmut_8': x__get_severity_icon__mutmut_8, 
    'x__get_severity_icon__mutmut_9': x__get_severity_icon__mutmut_9, 
    'x__get_severity_icon__mutmut_10': x__get_severity_icon__mutmut_10, 
    'x__get_severity_icon__mutmut_11': x__get_severity_icon__mutmut_11
}
x__get_severity_icon__mutmut_orig.__name__ = 'x__get_severity_icon'


def render_conflict(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    args = [console, conflict]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_render_conflict__mutmut_orig, x_render_conflict__mutmut_mutants, args, kwargs, None)


def x_render_conflict__mutmut_orig(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_1(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = None
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_2(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(None)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_3(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = None

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_4(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(None)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_5(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = None

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_6(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = None

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_7(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(None)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_8(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = None
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_9(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=None, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_10(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style=None)
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_11(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_12(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, )
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_13(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=False, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_14(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="XXbold magentaXX")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_15(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="BOLD MAGENTA")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_16(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column(None, style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_17(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style=None, width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_18(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=None)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_19(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column(style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_20(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_21(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", )
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_22(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("XX#XX", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_23(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="XXcyanXX", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_24(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="CYAN", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_25(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=4)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_26(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column(None, style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_27(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style=None)
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_28(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column(style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_29(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", )
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_30(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("XXScopeXX", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_31(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_32(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("SCOPE", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_33(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="XXgreenXX")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_34(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="GREEN")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_35(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column(None, style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_36(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style=None)
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_37(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column(style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_38(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", )
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_39(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("XXDefinitionXX", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_40(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_41(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("DEFINITION", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_42(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="XXwhiteXX")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_43(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="WHITE")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_44(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column(None, justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_45(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify=None, style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_46(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style=None)

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_47(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column(justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_48(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_49(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", )

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_50(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("XXConfidenceXX", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_51(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_52(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("CONFIDENCE", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_53(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="XXrightXX", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_54(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="RIGHT", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_55(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="XXyellowXX")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_56(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="YELLOW")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_57(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(None, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_58(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=None):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_59(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_60(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, ):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_61(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=2):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_62(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                None,
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_63(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                None,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_64(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                None,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_65(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                None,
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_66(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_67(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_68(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_69(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_70(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(None),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_71(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = None
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_72(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = None

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_73(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "XX(No candidates available)XX"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_74(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(no candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_75(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(NO CANDIDATES AVAILABLE)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_76(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = None

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_77(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = None

    console.print(panel)


def x_render_conflict__mutmut_78(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        None,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_79(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=None,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_80(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=None,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_81(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=None,
    )

    console.print(panel)


def x_render_conflict__mutmut_82(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_83(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_84(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        border_style=severity_color,
    )

    console.print(panel)


def x_render_conflict__mutmut_85(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        )

    console.print(panel)


def x_render_conflict__mutmut_86(
    console: Console,
    conflict: SemanticConflict,
) -> None:
    """Render a single conflict with Rich formatting.

    Displays:
    - Severity icon and level (color-coded)
    - Term surface text
    - Context (usage location)
    - Ranked candidate senses (scope + definition + confidence)

    Args:
        console: Rich console instance
        conflict: Semantic conflict to render
    """
    severity_color = _get_severity_color(conflict.severity)
    severity_icon = _get_severity_icon(conflict.severity)

    # Create title with severity
    title = (
        f"[{severity_color}]{severity_icon}[/{severity_color}] "
        f'conflict: "{conflict.term.surface_text}"'
    )

    # Sort candidates by scope precedence then descending confidence
    ranked_candidates = sort_candidates(conflict.candidate_senses)

    # Create table for candidates
    if ranked_candidates:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Scope", style="green")
        table.add_column("Definition", style="white")
        table.add_column("Confidence", justify="right", style="yellow")

        # Add ranked candidates
        for idx, sense in enumerate(ranked_candidates, start=1):
            table.add_row(
                str(idx),
                sense.scope,
                sense.definition,
                f"{sense.confidence:.2f}",
            )

        body = table
    else:
        body = "(No candidates available)"

    # Create metadata subtitle
    metadata = (
        f"[bold]Term:[/bold] {conflict.term.surface_text}  "
        f"[bold]Type:[/bold] {conflict.conflict_type.value}  "
        f"[bold]Context:[/bold] {conflict.context}"
    )

    panel = Panel(
        body,
        title=title,
        subtitle=metadata,
        border_style=severity_color,
    )

    console.print(None)

x_render_conflict__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_render_conflict__mutmut_1': x_render_conflict__mutmut_1, 
    'x_render_conflict__mutmut_2': x_render_conflict__mutmut_2, 
    'x_render_conflict__mutmut_3': x_render_conflict__mutmut_3, 
    'x_render_conflict__mutmut_4': x_render_conflict__mutmut_4, 
    'x_render_conflict__mutmut_5': x_render_conflict__mutmut_5, 
    'x_render_conflict__mutmut_6': x_render_conflict__mutmut_6, 
    'x_render_conflict__mutmut_7': x_render_conflict__mutmut_7, 
    'x_render_conflict__mutmut_8': x_render_conflict__mutmut_8, 
    'x_render_conflict__mutmut_9': x_render_conflict__mutmut_9, 
    'x_render_conflict__mutmut_10': x_render_conflict__mutmut_10, 
    'x_render_conflict__mutmut_11': x_render_conflict__mutmut_11, 
    'x_render_conflict__mutmut_12': x_render_conflict__mutmut_12, 
    'x_render_conflict__mutmut_13': x_render_conflict__mutmut_13, 
    'x_render_conflict__mutmut_14': x_render_conflict__mutmut_14, 
    'x_render_conflict__mutmut_15': x_render_conflict__mutmut_15, 
    'x_render_conflict__mutmut_16': x_render_conflict__mutmut_16, 
    'x_render_conflict__mutmut_17': x_render_conflict__mutmut_17, 
    'x_render_conflict__mutmut_18': x_render_conflict__mutmut_18, 
    'x_render_conflict__mutmut_19': x_render_conflict__mutmut_19, 
    'x_render_conflict__mutmut_20': x_render_conflict__mutmut_20, 
    'x_render_conflict__mutmut_21': x_render_conflict__mutmut_21, 
    'x_render_conflict__mutmut_22': x_render_conflict__mutmut_22, 
    'x_render_conflict__mutmut_23': x_render_conflict__mutmut_23, 
    'x_render_conflict__mutmut_24': x_render_conflict__mutmut_24, 
    'x_render_conflict__mutmut_25': x_render_conflict__mutmut_25, 
    'x_render_conflict__mutmut_26': x_render_conflict__mutmut_26, 
    'x_render_conflict__mutmut_27': x_render_conflict__mutmut_27, 
    'x_render_conflict__mutmut_28': x_render_conflict__mutmut_28, 
    'x_render_conflict__mutmut_29': x_render_conflict__mutmut_29, 
    'x_render_conflict__mutmut_30': x_render_conflict__mutmut_30, 
    'x_render_conflict__mutmut_31': x_render_conflict__mutmut_31, 
    'x_render_conflict__mutmut_32': x_render_conflict__mutmut_32, 
    'x_render_conflict__mutmut_33': x_render_conflict__mutmut_33, 
    'x_render_conflict__mutmut_34': x_render_conflict__mutmut_34, 
    'x_render_conflict__mutmut_35': x_render_conflict__mutmut_35, 
    'x_render_conflict__mutmut_36': x_render_conflict__mutmut_36, 
    'x_render_conflict__mutmut_37': x_render_conflict__mutmut_37, 
    'x_render_conflict__mutmut_38': x_render_conflict__mutmut_38, 
    'x_render_conflict__mutmut_39': x_render_conflict__mutmut_39, 
    'x_render_conflict__mutmut_40': x_render_conflict__mutmut_40, 
    'x_render_conflict__mutmut_41': x_render_conflict__mutmut_41, 
    'x_render_conflict__mutmut_42': x_render_conflict__mutmut_42, 
    'x_render_conflict__mutmut_43': x_render_conflict__mutmut_43, 
    'x_render_conflict__mutmut_44': x_render_conflict__mutmut_44, 
    'x_render_conflict__mutmut_45': x_render_conflict__mutmut_45, 
    'x_render_conflict__mutmut_46': x_render_conflict__mutmut_46, 
    'x_render_conflict__mutmut_47': x_render_conflict__mutmut_47, 
    'x_render_conflict__mutmut_48': x_render_conflict__mutmut_48, 
    'x_render_conflict__mutmut_49': x_render_conflict__mutmut_49, 
    'x_render_conflict__mutmut_50': x_render_conflict__mutmut_50, 
    'x_render_conflict__mutmut_51': x_render_conflict__mutmut_51, 
    'x_render_conflict__mutmut_52': x_render_conflict__mutmut_52, 
    'x_render_conflict__mutmut_53': x_render_conflict__mutmut_53, 
    'x_render_conflict__mutmut_54': x_render_conflict__mutmut_54, 
    'x_render_conflict__mutmut_55': x_render_conflict__mutmut_55, 
    'x_render_conflict__mutmut_56': x_render_conflict__mutmut_56, 
    'x_render_conflict__mutmut_57': x_render_conflict__mutmut_57, 
    'x_render_conflict__mutmut_58': x_render_conflict__mutmut_58, 
    'x_render_conflict__mutmut_59': x_render_conflict__mutmut_59, 
    'x_render_conflict__mutmut_60': x_render_conflict__mutmut_60, 
    'x_render_conflict__mutmut_61': x_render_conflict__mutmut_61, 
    'x_render_conflict__mutmut_62': x_render_conflict__mutmut_62, 
    'x_render_conflict__mutmut_63': x_render_conflict__mutmut_63, 
    'x_render_conflict__mutmut_64': x_render_conflict__mutmut_64, 
    'x_render_conflict__mutmut_65': x_render_conflict__mutmut_65, 
    'x_render_conflict__mutmut_66': x_render_conflict__mutmut_66, 
    'x_render_conflict__mutmut_67': x_render_conflict__mutmut_67, 
    'x_render_conflict__mutmut_68': x_render_conflict__mutmut_68, 
    'x_render_conflict__mutmut_69': x_render_conflict__mutmut_69, 
    'x_render_conflict__mutmut_70': x_render_conflict__mutmut_70, 
    'x_render_conflict__mutmut_71': x_render_conflict__mutmut_71, 
    'x_render_conflict__mutmut_72': x_render_conflict__mutmut_72, 
    'x_render_conflict__mutmut_73': x_render_conflict__mutmut_73, 
    'x_render_conflict__mutmut_74': x_render_conflict__mutmut_74, 
    'x_render_conflict__mutmut_75': x_render_conflict__mutmut_75, 
    'x_render_conflict__mutmut_76': x_render_conflict__mutmut_76, 
    'x_render_conflict__mutmut_77': x_render_conflict__mutmut_77, 
    'x_render_conflict__mutmut_78': x_render_conflict__mutmut_78, 
    'x_render_conflict__mutmut_79': x_render_conflict__mutmut_79, 
    'x_render_conflict__mutmut_80': x_render_conflict__mutmut_80, 
    'x_render_conflict__mutmut_81': x_render_conflict__mutmut_81, 
    'x_render_conflict__mutmut_82': x_render_conflict__mutmut_82, 
    'x_render_conflict__mutmut_83': x_render_conflict__mutmut_83, 
    'x_render_conflict__mutmut_84': x_render_conflict__mutmut_84, 
    'x_render_conflict__mutmut_85': x_render_conflict__mutmut_85, 
    'x_render_conflict__mutmut_86': x_render_conflict__mutmut_86
}
x_render_conflict__mutmut_orig.__name__ = 'x_render_conflict'


def render_conflict_batch(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    args = [console, conflicts, max_questions]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_render_conflict_batch__mutmut_orig, x_render_conflict_batch__mutmut_mutants, args, kwargs, None)


def x_render_conflict_batch__mutmut_orig(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_1(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 4,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_2(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = None
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_3(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 1, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_4(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 2, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_5(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 3}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_6(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = None

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_7(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        None,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_8(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=None,
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_9(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_10(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_11(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: None,
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_12(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(None, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_13(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, None), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_14(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_15(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, ), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_16(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 100), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_17(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = None

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_18(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) >= max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_19(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = None
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_20(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) + max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_21(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            None
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_22(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(None, conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_23(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, None)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_24(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(conflict)
        console.print()  # Blank line between conflicts

    return to_prompt


def x_render_conflict_batch__mutmut_25(
    console: Console,
    conflicts: List[SemanticConflict],
    max_questions: int = 3,
) -> List[SemanticConflict]:
    """Render conflicts prioritized by severity, capped at max_questions.

    Args:
        console: Rich console instance
        conflicts: All conflicts detected
        max_questions: Maximum conflicts to show (default 3)

    Returns:
        List of conflicts to prompt for (sorted by severity, capped)
    """
    # Sort by severity (high -> medium -> low), then by term text for determinism
    severity_order = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    sorted_conflicts = sorted(
        conflicts,
        key=lambda c: (severity_order.get(c.severity, 99), c.term.surface_text),
    )

    # Cap to max_questions
    to_prompt = sorted_conflicts[:max_questions]

    # Render summary if truncated
    if len(sorted_conflicts) > max_questions:
        remaining = len(sorted_conflicts) - max_questions
        console.print(
            f"\n[yellow]Note:[/yellow] Showing {max_questions} of "
            f"{len(sorted_conflicts)} conflicts. "
            f"{remaining} lower-priority conflict(s) deferred to async resolution.\n"
        )

    # Render each conflict
    for conflict in to_prompt:
        render_conflict(console, )
        console.print()  # Blank line between conflicts

    return to_prompt

x_render_conflict_batch__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_render_conflict_batch__mutmut_1': x_render_conflict_batch__mutmut_1, 
    'x_render_conflict_batch__mutmut_2': x_render_conflict_batch__mutmut_2, 
    'x_render_conflict_batch__mutmut_3': x_render_conflict_batch__mutmut_3, 
    'x_render_conflict_batch__mutmut_4': x_render_conflict_batch__mutmut_4, 
    'x_render_conflict_batch__mutmut_5': x_render_conflict_batch__mutmut_5, 
    'x_render_conflict_batch__mutmut_6': x_render_conflict_batch__mutmut_6, 
    'x_render_conflict_batch__mutmut_7': x_render_conflict_batch__mutmut_7, 
    'x_render_conflict_batch__mutmut_8': x_render_conflict_batch__mutmut_8, 
    'x_render_conflict_batch__mutmut_9': x_render_conflict_batch__mutmut_9, 
    'x_render_conflict_batch__mutmut_10': x_render_conflict_batch__mutmut_10, 
    'x_render_conflict_batch__mutmut_11': x_render_conflict_batch__mutmut_11, 
    'x_render_conflict_batch__mutmut_12': x_render_conflict_batch__mutmut_12, 
    'x_render_conflict_batch__mutmut_13': x_render_conflict_batch__mutmut_13, 
    'x_render_conflict_batch__mutmut_14': x_render_conflict_batch__mutmut_14, 
    'x_render_conflict_batch__mutmut_15': x_render_conflict_batch__mutmut_15, 
    'x_render_conflict_batch__mutmut_16': x_render_conflict_batch__mutmut_16, 
    'x_render_conflict_batch__mutmut_17': x_render_conflict_batch__mutmut_17, 
    'x_render_conflict_batch__mutmut_18': x_render_conflict_batch__mutmut_18, 
    'x_render_conflict_batch__mutmut_19': x_render_conflict_batch__mutmut_19, 
    'x_render_conflict_batch__mutmut_20': x_render_conflict_batch__mutmut_20, 
    'x_render_conflict_batch__mutmut_21': x_render_conflict_batch__mutmut_21, 
    'x_render_conflict_batch__mutmut_22': x_render_conflict_batch__mutmut_22, 
    'x_render_conflict_batch__mutmut_23': x_render_conflict_batch__mutmut_23, 
    'x_render_conflict_batch__mutmut_24': x_render_conflict_batch__mutmut_24, 
    'x_render_conflict_batch__mutmut_25': x_render_conflict_batch__mutmut_25
}
x_render_conflict_batch__mutmut_orig.__name__ = 'x_render_conflict_batch'
