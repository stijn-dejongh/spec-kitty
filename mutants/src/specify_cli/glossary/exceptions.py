"""Exception hierarchy for glossary semantic integrity."""

from __future__ import annotations

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .models import SemanticConflict
    from .strictness import Strictness
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


class GlossaryError(Exception):
    """Base exception for glossary errors."""
    pass


class BlockedByConflict(GlossaryError):
    """Generation blocked by unresolved semantic conflicts.

    This exception is raised by the generation gate middleware when
    the effective strictness policy requires blocking generation.
    """

    def __init__(
        self,
        conflicts: List["SemanticConflict"],
        strictness: "Strictness | None" = None,
        message: str | None = None,
    ):
        args = [conflicts, strictness, message]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlockedByConflictǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁBlockedByConflictǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁBlockedByConflictǁ__init____mutmut_orig(
        self,
        conflicts: List["SemanticConflict"],
        strictness: "Strictness | None" = None,
        message: str | None = None,
    ):
        """Initialize BlockedByConflict exception.

        Args:
            conflicts: List of conflicts that triggered the block
            strictness: The effective strictness mode (for context)
            message: Optional custom message (defaults to generic message)
        """
        self.conflicts = conflicts
        self.strictness = strictness

        # Use custom message if provided, otherwise generate default
        if message:
            super().__init__(message)
        else:
            conflict_count = len(conflicts)
            super().__init__(
                f"Generation blocked by {conflict_count} semantic conflict(s). "
                f"Resolve conflicts or use --strictness off to bypass."
            )

    def xǁBlockedByConflictǁ__init____mutmut_1(
        self,
        conflicts: List["SemanticConflict"],
        strictness: "Strictness | None" = None,
        message: str | None = None,
    ):
        """Initialize BlockedByConflict exception.

        Args:
            conflicts: List of conflicts that triggered the block
            strictness: The effective strictness mode (for context)
            message: Optional custom message (defaults to generic message)
        """
        self.conflicts = None
        self.strictness = strictness

        # Use custom message if provided, otherwise generate default
        if message:
            super().__init__(message)
        else:
            conflict_count = len(conflicts)
            super().__init__(
                f"Generation blocked by {conflict_count} semantic conflict(s). "
                f"Resolve conflicts or use --strictness off to bypass."
            )

    def xǁBlockedByConflictǁ__init____mutmut_2(
        self,
        conflicts: List["SemanticConflict"],
        strictness: "Strictness | None" = None,
        message: str | None = None,
    ):
        """Initialize BlockedByConflict exception.

        Args:
            conflicts: List of conflicts that triggered the block
            strictness: The effective strictness mode (for context)
            message: Optional custom message (defaults to generic message)
        """
        self.conflicts = conflicts
        self.strictness = None

        # Use custom message if provided, otherwise generate default
        if message:
            super().__init__(message)
        else:
            conflict_count = len(conflicts)
            super().__init__(
                f"Generation blocked by {conflict_count} semantic conflict(s). "
                f"Resolve conflicts or use --strictness off to bypass."
            )

    def xǁBlockedByConflictǁ__init____mutmut_3(
        self,
        conflicts: List["SemanticConflict"],
        strictness: "Strictness | None" = None,
        message: str | None = None,
    ):
        """Initialize BlockedByConflict exception.

        Args:
            conflicts: List of conflicts that triggered the block
            strictness: The effective strictness mode (for context)
            message: Optional custom message (defaults to generic message)
        """
        self.conflicts = conflicts
        self.strictness = strictness

        # Use custom message if provided, otherwise generate default
        if message:
            super().__init__(None)
        else:
            conflict_count = len(conflicts)
            super().__init__(
                f"Generation blocked by {conflict_count} semantic conflict(s). "
                f"Resolve conflicts or use --strictness off to bypass."
            )

    def xǁBlockedByConflictǁ__init____mutmut_4(
        self,
        conflicts: List["SemanticConflict"],
        strictness: "Strictness | None" = None,
        message: str | None = None,
    ):
        """Initialize BlockedByConflict exception.

        Args:
            conflicts: List of conflicts that triggered the block
            strictness: The effective strictness mode (for context)
            message: Optional custom message (defaults to generic message)
        """
        self.conflicts = conflicts
        self.strictness = strictness

        # Use custom message if provided, otherwise generate default
        if message:
            super().__init__(message)
        else:
            conflict_count = None
            super().__init__(
                f"Generation blocked by {conflict_count} semantic conflict(s). "
                f"Resolve conflicts or use --strictness off to bypass."
            )

    def xǁBlockedByConflictǁ__init____mutmut_5(
        self,
        conflicts: List["SemanticConflict"],
        strictness: "Strictness | None" = None,
        message: str | None = None,
    ):
        """Initialize BlockedByConflict exception.

        Args:
            conflicts: List of conflicts that triggered the block
            strictness: The effective strictness mode (for context)
            message: Optional custom message (defaults to generic message)
        """
        self.conflicts = conflicts
        self.strictness = strictness

        # Use custom message if provided, otherwise generate default
        if message:
            super().__init__(message)
        else:
            conflict_count = len(conflicts)
            super().__init__(
                None
            )
    
    xǁBlockedByConflictǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlockedByConflictǁ__init____mutmut_1': xǁBlockedByConflictǁ__init____mutmut_1, 
        'xǁBlockedByConflictǁ__init____mutmut_2': xǁBlockedByConflictǁ__init____mutmut_2, 
        'xǁBlockedByConflictǁ__init____mutmut_3': xǁBlockedByConflictǁ__init____mutmut_3, 
        'xǁBlockedByConflictǁ__init____mutmut_4': xǁBlockedByConflictǁ__init____mutmut_4, 
        'xǁBlockedByConflictǁ__init____mutmut_5': xǁBlockedByConflictǁ__init____mutmut_5
    }
    xǁBlockedByConflictǁ__init____mutmut_orig.__name__ = 'xǁBlockedByConflictǁ__init__'


class DeferredToAsync(GlossaryError):
    """User deferred conflict resolution to async mode."""

    def __init__(self, conflict_id: str):
        args = [conflict_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁDeferredToAsyncǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁDeferredToAsyncǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁDeferredToAsyncǁ__init____mutmut_orig(self, conflict_id: str):
        self.conflict_id = conflict_id
        super().__init__(
            f"Conflict {conflict_id} deferred to async resolution. "
            f"Generation remains blocked. Resolve via CLI or SaaS decision inbox."
        )

    def xǁDeferredToAsyncǁ__init____mutmut_1(self, conflict_id: str):
        self.conflict_id = None
        super().__init__(
            f"Conflict {conflict_id} deferred to async resolution. "
            f"Generation remains blocked. Resolve via CLI or SaaS decision inbox."
        )

    def xǁDeferredToAsyncǁ__init____mutmut_2(self, conflict_id: str):
        self.conflict_id = conflict_id
        super().__init__(
            None
        )
    
    xǁDeferredToAsyncǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁDeferredToAsyncǁ__init____mutmut_1': xǁDeferredToAsyncǁ__init____mutmut_1, 
        'xǁDeferredToAsyncǁ__init____mutmut_2': xǁDeferredToAsyncǁ__init____mutmut_2
    }
    xǁDeferredToAsyncǁ__init____mutmut_orig.__name__ = 'xǁDeferredToAsyncǁ__init__'


class AbortResume(GlossaryError):
    """User aborted resume (context changed)."""

    def __init__(self, reason: str):
        args = [reason]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAbortResumeǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁAbortResumeǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁAbortResumeǁ__init____mutmut_orig(self, reason: str):
        self.reason = reason
        super().__init__(f"Resume aborted: {reason}")

    def xǁAbortResumeǁ__init____mutmut_1(self, reason: str):
        self.reason = None
        super().__init__(f"Resume aborted: {reason}")

    def xǁAbortResumeǁ__init____mutmut_2(self, reason: str):
        self.reason = reason
        super().__init__(None)
    
    xǁAbortResumeǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAbortResumeǁ__init____mutmut_1': xǁAbortResumeǁ__init____mutmut_1, 
        'xǁAbortResumeǁ__init____mutmut_2': xǁAbortResumeǁ__init____mutmut_2
    }
    xǁAbortResumeǁ__init____mutmut_orig.__name__ = 'xǁAbortResumeǁ__init__'
