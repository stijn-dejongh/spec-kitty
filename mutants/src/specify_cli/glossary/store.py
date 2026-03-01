"""In-memory glossary store backed by event log."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict, List

from .models import TermSense
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


class GlossaryStore:
    """In-memory glossary store backed by event log."""

    def __init__(self, event_log_path: Path):
        args = [event_log_path]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁGlossaryStoreǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁGlossaryStoreǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁGlossaryStoreǁ__init____mutmut_orig(self, event_log_path: Path):
        self.event_log_path = event_log_path
        self._cache: Dict[str, Dict[str, List[TermSense]]] = {}
        # Format: {scope: {surface: [senses]}}
        # Create instance-specific cached lookup function
        self._lookup_cached = lru_cache(maxsize=10000)(self._lookup_impl)

    def xǁGlossaryStoreǁ__init____mutmut_1(self, event_log_path: Path):
        self.event_log_path = None
        self._cache: Dict[str, Dict[str, List[TermSense]]] = {}
        # Format: {scope: {surface: [senses]}}
        # Create instance-specific cached lookup function
        self._lookup_cached = lru_cache(maxsize=10000)(self._lookup_impl)

    def xǁGlossaryStoreǁ__init____mutmut_2(self, event_log_path: Path):
        self.event_log_path = event_log_path
        self._cache: Dict[str, Dict[str, List[TermSense]]] = None
        # Format: {scope: {surface: [senses]}}
        # Create instance-specific cached lookup function
        self._lookup_cached = lru_cache(maxsize=10000)(self._lookup_impl)

    def xǁGlossaryStoreǁ__init____mutmut_3(self, event_log_path: Path):
        self.event_log_path = event_log_path
        self._cache: Dict[str, Dict[str, List[TermSense]]] = {}
        # Format: {scope: {surface: [senses]}}
        # Create instance-specific cached lookup function
        self._lookup_cached = None

    def xǁGlossaryStoreǁ__init____mutmut_4(self, event_log_path: Path):
        self.event_log_path = event_log_path
        self._cache: Dict[str, Dict[str, List[TermSense]]] = {}
        # Format: {scope: {surface: [senses]}}
        # Create instance-specific cached lookup function
        self._lookup_cached = lru_cache(maxsize=10000)(None)

    def xǁGlossaryStoreǁ__init____mutmut_5(self, event_log_path: Path):
        self.event_log_path = event_log_path
        self._cache: Dict[str, Dict[str, List[TermSense]]] = {}
        # Format: {scope: {surface: [senses]}}
        # Create instance-specific cached lookup function
        self._lookup_cached = lru_cache(maxsize=None)(self._lookup_impl)

    def xǁGlossaryStoreǁ__init____mutmut_6(self, event_log_path: Path):
        self.event_log_path = event_log_path
        self._cache: Dict[str, Dict[str, List[TermSense]]] = {}
        # Format: {scope: {surface: [senses]}}
        # Create instance-specific cached lookup function
        self._lookup_cached = lru_cache(maxsize=10001)(self._lookup_impl)
    
    xǁGlossaryStoreǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁGlossaryStoreǁ__init____mutmut_1': xǁGlossaryStoreǁ__init____mutmut_1, 
        'xǁGlossaryStoreǁ__init____mutmut_2': xǁGlossaryStoreǁ__init____mutmut_2, 
        'xǁGlossaryStoreǁ__init____mutmut_3': xǁGlossaryStoreǁ__init____mutmut_3, 
        'xǁGlossaryStoreǁ__init____mutmut_4': xǁGlossaryStoreǁ__init____mutmut_4, 
        'xǁGlossaryStoreǁ__init____mutmut_5': xǁGlossaryStoreǁ__init____mutmut_5, 
        'xǁGlossaryStoreǁ__init____mutmut_6': xǁGlossaryStoreǁ__init____mutmut_6
    }
    xǁGlossaryStoreǁ__init____mutmut_orig.__name__ = 'xǁGlossaryStoreǁ__init__'

    def load_from_events(self) -> None:
        """Rebuild glossary from event log."""
        # Read GlossarySenseUpdated events from log
        # Populate self._cache
        pass  # WP08 will implement event reading

    def add_sense(self, sense: TermSense) -> None:
        args = [sense]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁGlossaryStoreǁadd_sense__mutmut_orig'), object.__getattribute__(self, 'xǁGlossaryStoreǁadd_sense__mutmut_mutants'), args, kwargs, self)

    def xǁGlossaryStoreǁadd_sense__mutmut_orig(self, sense: TermSense) -> None:
        """
        Add a sense to the store.

        Args:
            sense: TermSense to add
        """
        scope = sense.scope
        surface = sense.surface.surface_text

        if scope not in self._cache:
            self._cache[scope] = {}
        if surface not in self._cache[scope]:
            self._cache[scope][surface] = []

        self._cache[scope][surface].append(sense)

        # Clear lookup cache when sense is added (cache invalidation)
        self._lookup_cached.cache_clear()

    def xǁGlossaryStoreǁadd_sense__mutmut_1(self, sense: TermSense) -> None:
        """
        Add a sense to the store.

        Args:
            sense: TermSense to add
        """
        scope = None
        surface = sense.surface.surface_text

        if scope not in self._cache:
            self._cache[scope] = {}
        if surface not in self._cache[scope]:
            self._cache[scope][surface] = []

        self._cache[scope][surface].append(sense)

        # Clear lookup cache when sense is added (cache invalidation)
        self._lookup_cached.cache_clear()

    def xǁGlossaryStoreǁadd_sense__mutmut_2(self, sense: TermSense) -> None:
        """
        Add a sense to the store.

        Args:
            sense: TermSense to add
        """
        scope = sense.scope
        surface = None

        if scope not in self._cache:
            self._cache[scope] = {}
        if surface not in self._cache[scope]:
            self._cache[scope][surface] = []

        self._cache[scope][surface].append(sense)

        # Clear lookup cache when sense is added (cache invalidation)
        self._lookup_cached.cache_clear()

    def xǁGlossaryStoreǁadd_sense__mutmut_3(self, sense: TermSense) -> None:
        """
        Add a sense to the store.

        Args:
            sense: TermSense to add
        """
        scope = sense.scope
        surface = sense.surface.surface_text

        if scope in self._cache:
            self._cache[scope] = {}
        if surface not in self._cache[scope]:
            self._cache[scope][surface] = []

        self._cache[scope][surface].append(sense)

        # Clear lookup cache when sense is added (cache invalidation)
        self._lookup_cached.cache_clear()

    def xǁGlossaryStoreǁadd_sense__mutmut_4(self, sense: TermSense) -> None:
        """
        Add a sense to the store.

        Args:
            sense: TermSense to add
        """
        scope = sense.scope
        surface = sense.surface.surface_text

        if scope not in self._cache:
            self._cache[scope] = None
        if surface not in self._cache[scope]:
            self._cache[scope][surface] = []

        self._cache[scope][surface].append(sense)

        # Clear lookup cache when sense is added (cache invalidation)
        self._lookup_cached.cache_clear()

    def xǁGlossaryStoreǁadd_sense__mutmut_5(self, sense: TermSense) -> None:
        """
        Add a sense to the store.

        Args:
            sense: TermSense to add
        """
        scope = sense.scope
        surface = sense.surface.surface_text

        if scope not in self._cache:
            self._cache[scope] = {}
        if surface in self._cache[scope]:
            self._cache[scope][surface] = []

        self._cache[scope][surface].append(sense)

        # Clear lookup cache when sense is added (cache invalidation)
        self._lookup_cached.cache_clear()

    def xǁGlossaryStoreǁadd_sense__mutmut_6(self, sense: TermSense) -> None:
        """
        Add a sense to the store.

        Args:
            sense: TermSense to add
        """
        scope = sense.scope
        surface = sense.surface.surface_text

        if scope not in self._cache:
            self._cache[scope] = {}
        if surface not in self._cache[scope]:
            self._cache[scope][surface] = None

        self._cache[scope][surface].append(sense)

        # Clear lookup cache when sense is added (cache invalidation)
        self._lookup_cached.cache_clear()

    def xǁGlossaryStoreǁadd_sense__mutmut_7(self, sense: TermSense) -> None:
        """
        Add a sense to the store.

        Args:
            sense: TermSense to add
        """
        scope = sense.scope
        surface = sense.surface.surface_text

        if scope not in self._cache:
            self._cache[scope] = {}
        if surface not in self._cache[scope]:
            self._cache[scope][surface] = []

        self._cache[scope][surface].append(None)

        # Clear lookup cache when sense is added (cache invalidation)
        self._lookup_cached.cache_clear()
    
    xǁGlossaryStoreǁadd_sense__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁGlossaryStoreǁadd_sense__mutmut_1': xǁGlossaryStoreǁadd_sense__mutmut_1, 
        'xǁGlossaryStoreǁadd_sense__mutmut_2': xǁGlossaryStoreǁadd_sense__mutmut_2, 
        'xǁGlossaryStoreǁadd_sense__mutmut_3': xǁGlossaryStoreǁadd_sense__mutmut_3, 
        'xǁGlossaryStoreǁadd_sense__mutmut_4': xǁGlossaryStoreǁadd_sense__mutmut_4, 
        'xǁGlossaryStoreǁadd_sense__mutmut_5': xǁGlossaryStoreǁadd_sense__mutmut_5, 
        'xǁGlossaryStoreǁadd_sense__mutmut_6': xǁGlossaryStoreǁadd_sense__mutmut_6, 
        'xǁGlossaryStoreǁadd_sense__mutmut_7': xǁGlossaryStoreǁadd_sense__mutmut_7
    }
    xǁGlossaryStoreǁadd_sense__mutmut_orig.__name__ = 'xǁGlossaryStoreǁadd_sense'

    def _lookup_impl(self, surface: str, scopes: tuple[str, ...]) -> tuple[TermSense, ...]:
        args = [surface, scopes]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁGlossaryStoreǁ_lookup_impl__mutmut_orig'), object.__getattribute__(self, 'xǁGlossaryStoreǁ_lookup_impl__mutmut_mutants'), args, kwargs, self)

    def xǁGlossaryStoreǁ_lookup_impl__mutmut_orig(self, surface: str, scopes: tuple[str, ...]) -> tuple[TermSense, ...]:
        """
        Internal cached lookup implementation.

        Returns tuple instead of list for immutability (required for caching).
        """
        results: List[TermSense] = []
        for scope in scopes:
            if scope in self._cache and surface in self._cache[scope]:
                results.extend(self._cache[scope][surface])
        return tuple(results)

    def xǁGlossaryStoreǁ_lookup_impl__mutmut_1(self, surface: str, scopes: tuple[str, ...]) -> tuple[TermSense, ...]:
        """
        Internal cached lookup implementation.

        Returns tuple instead of list for immutability (required for caching).
        """
        results: List[TermSense] = None
        for scope in scopes:
            if scope in self._cache and surface in self._cache[scope]:
                results.extend(self._cache[scope][surface])
        return tuple(results)

    def xǁGlossaryStoreǁ_lookup_impl__mutmut_2(self, surface: str, scopes: tuple[str, ...]) -> tuple[TermSense, ...]:
        """
        Internal cached lookup implementation.

        Returns tuple instead of list for immutability (required for caching).
        """
        results: List[TermSense] = []
        for scope in scopes:
            if scope in self._cache or surface in self._cache[scope]:
                results.extend(self._cache[scope][surface])
        return tuple(results)

    def xǁGlossaryStoreǁ_lookup_impl__mutmut_3(self, surface: str, scopes: tuple[str, ...]) -> tuple[TermSense, ...]:
        """
        Internal cached lookup implementation.

        Returns tuple instead of list for immutability (required for caching).
        """
        results: List[TermSense] = []
        for scope in scopes:
            if scope not in self._cache and surface in self._cache[scope]:
                results.extend(self._cache[scope][surface])
        return tuple(results)

    def xǁGlossaryStoreǁ_lookup_impl__mutmut_4(self, surface: str, scopes: tuple[str, ...]) -> tuple[TermSense, ...]:
        """
        Internal cached lookup implementation.

        Returns tuple instead of list for immutability (required for caching).
        """
        results: List[TermSense] = []
        for scope in scopes:
            if scope in self._cache and surface not in self._cache[scope]:
                results.extend(self._cache[scope][surface])
        return tuple(results)

    def xǁGlossaryStoreǁ_lookup_impl__mutmut_5(self, surface: str, scopes: tuple[str, ...]) -> tuple[TermSense, ...]:
        """
        Internal cached lookup implementation.

        Returns tuple instead of list for immutability (required for caching).
        """
        results: List[TermSense] = []
        for scope in scopes:
            if scope in self._cache and surface in self._cache[scope]:
                results.extend(None)
        return tuple(results)

    def xǁGlossaryStoreǁ_lookup_impl__mutmut_6(self, surface: str, scopes: tuple[str, ...]) -> tuple[TermSense, ...]:
        """
        Internal cached lookup implementation.

        Returns tuple instead of list for immutability (required for caching).
        """
        results: List[TermSense] = []
        for scope in scopes:
            if scope in self._cache and surface in self._cache[scope]:
                results.extend(self._cache[scope][surface])
        return tuple(None)
    
    xǁGlossaryStoreǁ_lookup_impl__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁGlossaryStoreǁ_lookup_impl__mutmut_1': xǁGlossaryStoreǁ_lookup_impl__mutmut_1, 
        'xǁGlossaryStoreǁ_lookup_impl__mutmut_2': xǁGlossaryStoreǁ_lookup_impl__mutmut_2, 
        'xǁGlossaryStoreǁ_lookup_impl__mutmut_3': xǁGlossaryStoreǁ_lookup_impl__mutmut_3, 
        'xǁGlossaryStoreǁ_lookup_impl__mutmut_4': xǁGlossaryStoreǁ_lookup_impl__mutmut_4, 
        'xǁGlossaryStoreǁ_lookup_impl__mutmut_5': xǁGlossaryStoreǁ_lookup_impl__mutmut_5, 
        'xǁGlossaryStoreǁ_lookup_impl__mutmut_6': xǁGlossaryStoreǁ_lookup_impl__mutmut_6
    }
    xǁGlossaryStoreǁ_lookup_impl__mutmut_orig.__name__ = 'xǁGlossaryStoreǁ_lookup_impl'

    def lookup(self, surface: str, scopes: tuple[str, ...]) -> List[TermSense]:
        args = [surface, scopes]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁGlossaryStoreǁlookup__mutmut_orig'), object.__getattribute__(self, 'xǁGlossaryStoreǁlookup__mutmut_mutants'), args, kwargs, self)

    def xǁGlossaryStoreǁlookup__mutmut_orig(self, surface: str, scopes: tuple[str, ...]) -> List[TermSense]:
        """
        Look up term in scope hierarchy (with LRU cache).

        Args:
            surface: Term surface text (normalized)
            scopes: Tuple of scope names in precedence order

        Returns:
            List of matching TermSense objects in scope order
        """
        # Use cached implementation and convert back to list
        return list(self._lookup_cached(surface, scopes))

    def xǁGlossaryStoreǁlookup__mutmut_1(self, surface: str, scopes: tuple[str, ...]) -> List[TermSense]:
        """
        Look up term in scope hierarchy (with LRU cache).

        Args:
            surface: Term surface text (normalized)
            scopes: Tuple of scope names in precedence order

        Returns:
            List of matching TermSense objects in scope order
        """
        # Use cached implementation and convert back to list
        return list(None)

    def xǁGlossaryStoreǁlookup__mutmut_2(self, surface: str, scopes: tuple[str, ...]) -> List[TermSense]:
        """
        Look up term in scope hierarchy (with LRU cache).

        Args:
            surface: Term surface text (normalized)
            scopes: Tuple of scope names in precedence order

        Returns:
            List of matching TermSense objects in scope order
        """
        # Use cached implementation and convert back to list
        return list(self._lookup_cached(None, scopes))

    def xǁGlossaryStoreǁlookup__mutmut_3(self, surface: str, scopes: tuple[str, ...]) -> List[TermSense]:
        """
        Look up term in scope hierarchy (with LRU cache).

        Args:
            surface: Term surface text (normalized)
            scopes: Tuple of scope names in precedence order

        Returns:
            List of matching TermSense objects in scope order
        """
        # Use cached implementation and convert back to list
        return list(self._lookup_cached(surface, None))

    def xǁGlossaryStoreǁlookup__mutmut_4(self, surface: str, scopes: tuple[str, ...]) -> List[TermSense]:
        """
        Look up term in scope hierarchy (with LRU cache).

        Args:
            surface: Term surface text (normalized)
            scopes: Tuple of scope names in precedence order

        Returns:
            List of matching TermSense objects in scope order
        """
        # Use cached implementation and convert back to list
        return list(self._lookup_cached(scopes))

    def xǁGlossaryStoreǁlookup__mutmut_5(self, surface: str, scopes: tuple[str, ...]) -> List[TermSense]:
        """
        Look up term in scope hierarchy (with LRU cache).

        Args:
            surface: Term surface text (normalized)
            scopes: Tuple of scope names in precedence order

        Returns:
            List of matching TermSense objects in scope order
        """
        # Use cached implementation and convert back to list
        return list(self._lookup_cached(surface, ))
    
    xǁGlossaryStoreǁlookup__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁGlossaryStoreǁlookup__mutmut_1': xǁGlossaryStoreǁlookup__mutmut_1, 
        'xǁGlossaryStoreǁlookup__mutmut_2': xǁGlossaryStoreǁlookup__mutmut_2, 
        'xǁGlossaryStoreǁlookup__mutmut_3': xǁGlossaryStoreǁlookup__mutmut_3, 
        'xǁGlossaryStoreǁlookup__mutmut_4': xǁGlossaryStoreǁlookup__mutmut_4, 
        'xǁGlossaryStoreǁlookup__mutmut_5': xǁGlossaryStoreǁlookup__mutmut_5
    }
    xǁGlossaryStoreǁlookup__mutmut_orig.__name__ = 'xǁGlossaryStoreǁlookup'
