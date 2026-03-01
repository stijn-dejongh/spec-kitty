"""
VCS Abstraction Package
=======================

This package provides a unified interface for Version Control System operations,
supporting both Git and Jujutsu (jj) backends.

Usage:
    from specify_cli.core.vcs import (
        get_vcs,
        VCSProtocol,
        VCSBackend,
        VCSCapabilities,
        GIT_CAPABILITIES,
        JJ_CAPABILITIES,
        is_jj_available,
        is_git_available,
    )

    # Get appropriate VCS implementation
    vcs = get_vcs(feature_path)  # Auto-detect, prefers jj
    vcs = get_vcs(feature_path, backend=VCSBackend.GIT)  # Explicit git

See kitty-specs/015-first-class-jujutsu-vcs-integration/ for full documentation.
"""

from __future__ import annotations

# Enums
from .types import (
    ConflictType,
    SyncStatus,
    VCSBackend,
)

# Dataclasses
from .types import (
    ChangeInfo,
    ConflictInfo,
    FeatureVCSConfig,
    OperationInfo,
    ProjectVCSConfig,
    SyncResult,
    VCSCapabilities,
    WorkspaceCreateResult,
    WorkspaceInfo,
)

# Capability constants
from .types import (
    GIT_CAPABILITIES,
    JJ_CAPABILITIES,
)

# Protocol
from .protocol import VCSProtocol

# Exceptions
from .exceptions import (
    VCSBackendMismatchError,
    VCSCapabilityError,
    VCSConflictError,
    VCSError,
    VCSLockError,
    VCSNotFoundError,
    VCSSyncError,
)

# Detection and factory functions
from .detection import (
    detect_available_backends,
    get_git_version,
    get_jj_version,
    get_vcs,
    is_git_available,
    is_jj_available,
)

__all__ = [
    # Enums
    "VCSBackend",
    "SyncStatus",
    "ConflictType",
    # Dataclasses
    "VCSCapabilities",
    "ChangeInfo",
    "ConflictInfo",
    "SyncResult",
    "WorkspaceInfo",
    "OperationInfo",
    "WorkspaceCreateResult",
    "ProjectVCSConfig",
    "FeatureVCSConfig",
    # Capability constants
    "GIT_CAPABILITIES",
    "JJ_CAPABILITIES",
    # Protocol
    "VCSProtocol",
    # Exceptions
    "VCSError",
    "VCSNotFoundError",
    "VCSCapabilityError",
    "VCSBackendMismatchError",
    "VCSLockError",
    "VCSConflictError",
    "VCSSyncError",
    # Detection and factory
    "get_vcs",
    "is_jj_available",
    "is_git_available",
    "get_jj_version",
    "get_git_version",
    "detect_available_backends",
]
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
