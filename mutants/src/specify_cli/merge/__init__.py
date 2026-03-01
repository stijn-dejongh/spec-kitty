"""Merge subpackage for spec-kitty merge operations.

This package provides functionality for merging work package branches
back into the main branch with pre-flight validation, conflict forecasting,
and automatic status file resolution.

Modules:
    preflight: Pre-flight validation before merge
    forecast: Conflict prediction for dry-run mode
    ordering: Dependency-based merge ordering
    status_resolver: Auto-resolution of status file conflicts
    state: Merge state persistence and resume
    executor: Core merge execution logic
"""

from __future__ import annotations

from specify_cli.merge.executor import (
    MergeExecutionError,
    MergeResult,
    execute_legacy_merge,
    execute_merge,
)
from specify_cli.merge.forecast import ConflictPrediction, is_status_file, predict_conflicts
from specify_cli.merge.ordering import MergeOrderError, get_merge_order, has_dependency_info
from specify_cli.merge.preflight import PreflightResult, WPStatus, run_preflight
from specify_cli.merge.state import (
    MergeState,
    clear_state,
    has_active_merge,
    load_state,
    save_state,
)
from specify_cli.merge.status_resolver import ResolutionResult, resolve_status_conflicts

__all__ = [
    # Executor
    "execute_merge",
    "execute_legacy_merge",
    "MergeResult",
    "MergeExecutionError",
    # Forecast
    "predict_conflicts",
    "ConflictPrediction",
    "is_status_file",
    # Ordering
    "get_merge_order",
    "MergeOrderError",
    "has_dependency_info",
    # Preflight
    "run_preflight",
    "PreflightResult",
    "WPStatus",
    # Status resolver
    "resolve_status_conflicts",
    "ResolutionResult",
    # State persistence
    "MergeState",
    "save_state",
    "load_state",
    "clear_state",
    "has_active_merge",
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
