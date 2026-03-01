"""
VCS Exceptions Module
=====================

This module defines the exception hierarchy for VCS operations.
All VCS-related exceptions inherit from VCSError.
"""

from __future__ import annotations
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


class VCSError(Exception):
    """
    Base exception for VCS operations.

    All VCS-related exceptions inherit from this class.
    """

    pass


class VCSNotFoundError(VCSError):
    """
    Neither jj nor git is available.

    Raised when attempting VCS operations but no supported
    VCS tool is installed or accessible.
    """

    pass


class VCSCapabilityError(VCSError):
    """
    Operation not supported by this backend.

    Raised when attempting an operation that the current
    VCS backend does not support (e.g., jj undo on git).
    """

    pass


class VCSBackendMismatchError(VCSError):
    """
    Requested backend doesn't match feature's locked VCS.

    Raised when explicitly requesting a backend that differs
    from the VCS locked in the feature's meta.json.
    """

    pass


class VCSLockError(VCSError):
    """
    Attempted to change VCS for a feature after it was locked.

    Once a feature has its VCS set (on first workspace creation),
    it cannot be changed. This exception is raised on such attempts.
    """

    pass


class VCSConflictError(VCSError):
    """
    Operation blocked due to unresolved conflicts.

    Raised when an operation cannot proceed because the
    workspace has unresolved conflicts that must be addressed first.
    """

    pass


class VCSSyncError(VCSError):
    """
    Sync operation failed.

    Raised when workspace synchronization fails due to
    network issues, permissions, or other errors.
    """

    pass
