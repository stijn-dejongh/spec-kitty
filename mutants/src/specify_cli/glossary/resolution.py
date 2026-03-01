"""Scope resolution logic (WP04).

This module implements term resolution against the scope hierarchy.
Terms are resolved in precedence order: mission_local → team_domain → audience_domain → spec_kitty_core.
"""

from __future__ import annotations

from typing import List

from .models import TermSense
from .scope import GlossaryScope
from .store import GlossaryStore
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


def resolve_term(
    surface: str,
    scopes: List[GlossaryScope],
    store: GlossaryStore,
) -> List[TermSense]:
    args = [surface, scopes, store]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_resolve_term__mutmut_orig, x_resolve_term__mutmut_mutants, args, kwargs, None)


def x_resolve_term__mutmut_orig(
    surface: str,
    scopes: List[GlossaryScope],
    store: GlossaryStore,
) -> List[TermSense]:
    """Resolve term against scope hierarchy.

    Args:
        surface: Term surface text (normalized)
        scopes: List of GlossaryScope in precedence order
        store: GlossaryStore to query

    Returns:
        List of matching TermSense objects across all scopes.
        Results maintain scope precedence order.

    Example:
        >>> scopes = [GlossaryScope.MISSION_LOCAL, GlossaryScope.TEAM_DOMAIN]
        >>> results = resolve_term("workspace", scopes, store)
        >>> # Returns matches from mission_local first, then team_domain
    """
    # Convert enum values to strings for store lookup
    scope_values = tuple(s.value for s in scopes)
    return store.lookup(surface, scope_values)


def x_resolve_term__mutmut_1(
    surface: str,
    scopes: List[GlossaryScope],
    store: GlossaryStore,
) -> List[TermSense]:
    """Resolve term against scope hierarchy.

    Args:
        surface: Term surface text (normalized)
        scopes: List of GlossaryScope in precedence order
        store: GlossaryStore to query

    Returns:
        List of matching TermSense objects across all scopes.
        Results maintain scope precedence order.

    Example:
        >>> scopes = [GlossaryScope.MISSION_LOCAL, GlossaryScope.TEAM_DOMAIN]
        >>> results = resolve_term("workspace", scopes, store)
        >>> # Returns matches from mission_local first, then team_domain
    """
    # Convert enum values to strings for store lookup
    scope_values = None
    return store.lookup(surface, scope_values)


def x_resolve_term__mutmut_2(
    surface: str,
    scopes: List[GlossaryScope],
    store: GlossaryStore,
) -> List[TermSense]:
    """Resolve term against scope hierarchy.

    Args:
        surface: Term surface text (normalized)
        scopes: List of GlossaryScope in precedence order
        store: GlossaryStore to query

    Returns:
        List of matching TermSense objects across all scopes.
        Results maintain scope precedence order.

    Example:
        >>> scopes = [GlossaryScope.MISSION_LOCAL, GlossaryScope.TEAM_DOMAIN]
        >>> results = resolve_term("workspace", scopes, store)
        >>> # Returns matches from mission_local first, then team_domain
    """
    # Convert enum values to strings for store lookup
    scope_values = tuple(None)
    return store.lookup(surface, scope_values)


def x_resolve_term__mutmut_3(
    surface: str,
    scopes: List[GlossaryScope],
    store: GlossaryStore,
) -> List[TermSense]:
    """Resolve term against scope hierarchy.

    Args:
        surface: Term surface text (normalized)
        scopes: List of GlossaryScope in precedence order
        store: GlossaryStore to query

    Returns:
        List of matching TermSense objects across all scopes.
        Results maintain scope precedence order.

    Example:
        >>> scopes = [GlossaryScope.MISSION_LOCAL, GlossaryScope.TEAM_DOMAIN]
        >>> results = resolve_term("workspace", scopes, store)
        >>> # Returns matches from mission_local first, then team_domain
    """
    # Convert enum values to strings for store lookup
    scope_values = tuple(s.value for s in scopes)
    return store.lookup(None, scope_values)


def x_resolve_term__mutmut_4(
    surface: str,
    scopes: List[GlossaryScope],
    store: GlossaryStore,
) -> List[TermSense]:
    """Resolve term against scope hierarchy.

    Args:
        surface: Term surface text (normalized)
        scopes: List of GlossaryScope in precedence order
        store: GlossaryStore to query

    Returns:
        List of matching TermSense objects across all scopes.
        Results maintain scope precedence order.

    Example:
        >>> scopes = [GlossaryScope.MISSION_LOCAL, GlossaryScope.TEAM_DOMAIN]
        >>> results = resolve_term("workspace", scopes, store)
        >>> # Returns matches from mission_local first, then team_domain
    """
    # Convert enum values to strings for store lookup
    scope_values = tuple(s.value for s in scopes)
    return store.lookup(surface, None)


def x_resolve_term__mutmut_5(
    surface: str,
    scopes: List[GlossaryScope],
    store: GlossaryStore,
) -> List[TermSense]:
    """Resolve term against scope hierarchy.

    Args:
        surface: Term surface text (normalized)
        scopes: List of GlossaryScope in precedence order
        store: GlossaryStore to query

    Returns:
        List of matching TermSense objects across all scopes.
        Results maintain scope precedence order.

    Example:
        >>> scopes = [GlossaryScope.MISSION_LOCAL, GlossaryScope.TEAM_DOMAIN]
        >>> results = resolve_term("workspace", scopes, store)
        >>> # Returns matches from mission_local first, then team_domain
    """
    # Convert enum values to strings for store lookup
    scope_values = tuple(s.value for s in scopes)
    return store.lookup(scope_values)


def x_resolve_term__mutmut_6(
    surface: str,
    scopes: List[GlossaryScope],
    store: GlossaryStore,
) -> List[TermSense]:
    """Resolve term against scope hierarchy.

    Args:
        surface: Term surface text (normalized)
        scopes: List of GlossaryScope in precedence order
        store: GlossaryStore to query

    Returns:
        List of matching TermSense objects across all scopes.
        Results maintain scope precedence order.

    Example:
        >>> scopes = [GlossaryScope.MISSION_LOCAL, GlossaryScope.TEAM_DOMAIN]
        >>> results = resolve_term("workspace", scopes, store)
        >>> # Returns matches from mission_local first, then team_domain
    """
    # Convert enum values to strings for store lookup
    scope_values = tuple(s.value for s in scopes)
    return store.lookup(surface, )

x_resolve_term__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_resolve_term__mutmut_1': x_resolve_term__mutmut_1, 
    'x_resolve_term__mutmut_2': x_resolve_term__mutmut_2, 
    'x_resolve_term__mutmut_3': x_resolve_term__mutmut_3, 
    'x_resolve_term__mutmut_4': x_resolve_term__mutmut_4, 
    'x_resolve_term__mutmut_5': x_resolve_term__mutmut_5, 
    'x_resolve_term__mutmut_6': x_resolve_term__mutmut_6
}
x_resolve_term__mutmut_orig.__name__ = 'x_resolve_term'
