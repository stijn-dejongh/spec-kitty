"""Metadata-driven glossary pipeline attachment to mission primitives (WP09).

This module provides the mechanism to attach the glossary middleware pipeline
to mission primitive execution. The attachment is driven by metadata in step
definitions: ``glossary_check: enabled`` (or the default, which is enabled
per FR-020).

Usage as a callable processor::

    processor = attach_glossary_pipeline(
        repo_root=Path("."),
        runtime_strictness=Strictness.MEDIUM,
        interaction_mode="interactive",
    )
    processed_context = processor(context)

Usage as a decorator on mission primitive functions::

    @glossary_enabled(repo_root=Path("."))
    def my_primitive(context: PrimitiveExecutionContext) -> dict:
        # Glossary pipeline runs automatically before this body
        return {"result": "ok"}

Usage as a direct wrapper::

    result_context = run_with_glossary(
        context=ctx,
        repo_root=Path("."),
        runtime_strictness=Strictness.OFF,
    )
"""

from __future__ import annotations

import functools
import logging
import time
from pathlib import Path
from typing import Any, Callable, Optional

from specify_cli.glossary.exceptions import (
    AbortResume,
    BlockedByConflict,
    DeferredToAsync,
)
from specify_cli.glossary.pipeline import create_standard_pipeline
from specify_cli.glossary.strictness import Strictness

logger = logging.getLogger(__name__)
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


def attach_glossary_pipeline(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    args = [repo_root, runtime_strictness, interaction_mode]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_attach_glossary_pipeline__mutmut_orig, x_attach_glossary_pipeline__mutmut_mutants, args, kwargs, None)


def x_attach_glossary_pipeline__mutmut_orig(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_1(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "XXinteractiveXX",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_2(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "INTERACTIVE",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_3(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = None

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_4(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=None,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_5(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=None,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_6(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=None,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_7(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_8(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_9(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_10(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = None
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_11(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = None
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_12(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(None)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_13(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = None
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_14(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() + start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_15(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                None,
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_16(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                None,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_17(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                None,
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_18(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_19(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_20(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_21(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "XXGlossary pipeline completed in %.3fs for step=%sXX",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_22(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_23(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "GLOSSARY PIPELINE COMPLETED IN %.3FS FOR STEP=%S",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_24(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(None, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_25(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, None, "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_26(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", None),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_27(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr("step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_28(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_29(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", ),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_30(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "XXstep_idXX", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_31(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "STEP_ID", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_32(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "XXunknownXX"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_33(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "UNKNOWN"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_34(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = None
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_35(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() + start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_36(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                None,
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_37(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                None,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_38(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                None,
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_39(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_40(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_41(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_42(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "XXGlossary pipeline halted after %.3fs for step=%sXX",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_43(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_44(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "GLOSSARY PIPELINE HALTED AFTER %.3FS FOR STEP=%S",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_45(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(None, "step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_46(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, None, "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_47(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", None),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_48(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr("step_id", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_49(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_50(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", ),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_51(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "XXstep_idXX", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_52(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "STEP_ID", "unknown"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_53(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "XXunknownXX"),
            )
            raise

    return process_with_glossary


def x_attach_glossary_pipeline__mutmut_54(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[[Any], Any]:
    """Create a glossary pipeline processor for mission primitives.

    Builds the standard 5-layer pipeline and returns a callable that
    processes any PrimitiveExecutionContext through it.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.

    Returns:
        A function that accepts a PrimitiveExecutionContext and returns
        the processed context. The function may raise BlockedByConflict,
        DeferredToAsync, or AbortResume.
    """
    pipeline = create_standard_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )

    def process_with_glossary(context: Any) -> Any:
        """Process context through the glossary middleware pipeline.

        Args:
            context: PrimitiveExecutionContext to process.

        Returns:
            Processed context with glossary fields populated.

        Raises:
            BlockedByConflict: Generation blocked by unresolved conflicts.
            DeferredToAsync: Conflict resolution deferred.
            AbortResume: User aborted resume.
        """
        start = time.perf_counter()
        try:
            result = pipeline.process(context)
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline completed in %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "unknown"),
            )
            return result
        except (BlockedByConflict, DeferredToAsync, AbortResume):
            elapsed = time.perf_counter() - start
            logger.info(
                "Glossary pipeline halted after %.3fs for step=%s",
                elapsed,
                getattr(context, "step_id", "UNKNOWN"),
            )
            raise

    return process_with_glossary

x_attach_glossary_pipeline__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_attach_glossary_pipeline__mutmut_1': x_attach_glossary_pipeline__mutmut_1, 
    'x_attach_glossary_pipeline__mutmut_2': x_attach_glossary_pipeline__mutmut_2, 
    'x_attach_glossary_pipeline__mutmut_3': x_attach_glossary_pipeline__mutmut_3, 
    'x_attach_glossary_pipeline__mutmut_4': x_attach_glossary_pipeline__mutmut_4, 
    'x_attach_glossary_pipeline__mutmut_5': x_attach_glossary_pipeline__mutmut_5, 
    'x_attach_glossary_pipeline__mutmut_6': x_attach_glossary_pipeline__mutmut_6, 
    'x_attach_glossary_pipeline__mutmut_7': x_attach_glossary_pipeline__mutmut_7, 
    'x_attach_glossary_pipeline__mutmut_8': x_attach_glossary_pipeline__mutmut_8, 
    'x_attach_glossary_pipeline__mutmut_9': x_attach_glossary_pipeline__mutmut_9, 
    'x_attach_glossary_pipeline__mutmut_10': x_attach_glossary_pipeline__mutmut_10, 
    'x_attach_glossary_pipeline__mutmut_11': x_attach_glossary_pipeline__mutmut_11, 
    'x_attach_glossary_pipeline__mutmut_12': x_attach_glossary_pipeline__mutmut_12, 
    'x_attach_glossary_pipeline__mutmut_13': x_attach_glossary_pipeline__mutmut_13, 
    'x_attach_glossary_pipeline__mutmut_14': x_attach_glossary_pipeline__mutmut_14, 
    'x_attach_glossary_pipeline__mutmut_15': x_attach_glossary_pipeline__mutmut_15, 
    'x_attach_glossary_pipeline__mutmut_16': x_attach_glossary_pipeline__mutmut_16, 
    'x_attach_glossary_pipeline__mutmut_17': x_attach_glossary_pipeline__mutmut_17, 
    'x_attach_glossary_pipeline__mutmut_18': x_attach_glossary_pipeline__mutmut_18, 
    'x_attach_glossary_pipeline__mutmut_19': x_attach_glossary_pipeline__mutmut_19, 
    'x_attach_glossary_pipeline__mutmut_20': x_attach_glossary_pipeline__mutmut_20, 
    'x_attach_glossary_pipeline__mutmut_21': x_attach_glossary_pipeline__mutmut_21, 
    'x_attach_glossary_pipeline__mutmut_22': x_attach_glossary_pipeline__mutmut_22, 
    'x_attach_glossary_pipeline__mutmut_23': x_attach_glossary_pipeline__mutmut_23, 
    'x_attach_glossary_pipeline__mutmut_24': x_attach_glossary_pipeline__mutmut_24, 
    'x_attach_glossary_pipeline__mutmut_25': x_attach_glossary_pipeline__mutmut_25, 
    'x_attach_glossary_pipeline__mutmut_26': x_attach_glossary_pipeline__mutmut_26, 
    'x_attach_glossary_pipeline__mutmut_27': x_attach_glossary_pipeline__mutmut_27, 
    'x_attach_glossary_pipeline__mutmut_28': x_attach_glossary_pipeline__mutmut_28, 
    'x_attach_glossary_pipeline__mutmut_29': x_attach_glossary_pipeline__mutmut_29, 
    'x_attach_glossary_pipeline__mutmut_30': x_attach_glossary_pipeline__mutmut_30, 
    'x_attach_glossary_pipeline__mutmut_31': x_attach_glossary_pipeline__mutmut_31, 
    'x_attach_glossary_pipeline__mutmut_32': x_attach_glossary_pipeline__mutmut_32, 
    'x_attach_glossary_pipeline__mutmut_33': x_attach_glossary_pipeline__mutmut_33, 
    'x_attach_glossary_pipeline__mutmut_34': x_attach_glossary_pipeline__mutmut_34, 
    'x_attach_glossary_pipeline__mutmut_35': x_attach_glossary_pipeline__mutmut_35, 
    'x_attach_glossary_pipeline__mutmut_36': x_attach_glossary_pipeline__mutmut_36, 
    'x_attach_glossary_pipeline__mutmut_37': x_attach_glossary_pipeline__mutmut_37, 
    'x_attach_glossary_pipeline__mutmut_38': x_attach_glossary_pipeline__mutmut_38, 
    'x_attach_glossary_pipeline__mutmut_39': x_attach_glossary_pipeline__mutmut_39, 
    'x_attach_glossary_pipeline__mutmut_40': x_attach_glossary_pipeline__mutmut_40, 
    'x_attach_glossary_pipeline__mutmut_41': x_attach_glossary_pipeline__mutmut_41, 
    'x_attach_glossary_pipeline__mutmut_42': x_attach_glossary_pipeline__mutmut_42, 
    'x_attach_glossary_pipeline__mutmut_43': x_attach_glossary_pipeline__mutmut_43, 
    'x_attach_glossary_pipeline__mutmut_44': x_attach_glossary_pipeline__mutmut_44, 
    'x_attach_glossary_pipeline__mutmut_45': x_attach_glossary_pipeline__mutmut_45, 
    'x_attach_glossary_pipeline__mutmut_46': x_attach_glossary_pipeline__mutmut_46, 
    'x_attach_glossary_pipeline__mutmut_47': x_attach_glossary_pipeline__mutmut_47, 
    'x_attach_glossary_pipeline__mutmut_48': x_attach_glossary_pipeline__mutmut_48, 
    'x_attach_glossary_pipeline__mutmut_49': x_attach_glossary_pipeline__mutmut_49, 
    'x_attach_glossary_pipeline__mutmut_50': x_attach_glossary_pipeline__mutmut_50, 
    'x_attach_glossary_pipeline__mutmut_51': x_attach_glossary_pipeline__mutmut_51, 
    'x_attach_glossary_pipeline__mutmut_52': x_attach_glossary_pipeline__mutmut_52, 
    'x_attach_glossary_pipeline__mutmut_53': x_attach_glossary_pipeline__mutmut_53, 
    'x_attach_glossary_pipeline__mutmut_54': x_attach_glossary_pipeline__mutmut_54
}
x_attach_glossary_pipeline__mutmut_orig.__name__ = 'x_attach_glossary_pipeline'


def read_glossary_check_metadata(step_metadata: dict[str, Any]) -> bool:
    args = [step_metadata]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_read_glossary_check_metadata__mutmut_orig, x_read_glossary_check_metadata__mutmut_mutants, args, kwargs, None)


def x_read_glossary_check_metadata__mutmut_orig(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return False
        if value.lower() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_1(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = None

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return False
        if value.lower() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_2(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get(None)

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return False
        if value.lower() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_3(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("XXglossary_checkXX")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return False
        if value.lower() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_4(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("GLOSSARY_CHECK")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return False
        if value.lower() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_5(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is not None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return False
        if value.lower() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_6(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return False

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return False
        if value.lower() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_7(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.upper() == "disabled":
            return False
        if value.lower() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_8(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() != "disabled":
            return False
        if value.lower() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_9(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "XXdisabledXX":
            return False
        if value.lower() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_10(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "DISABLED":
            return False
        if value.lower() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_11(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return True
        if value.lower() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_12(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return False
        if value.upper() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_13(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return False
        if value.lower() != "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_14(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return False
        if value.lower() == "XXenabledXX":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_15(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return False
        if value.lower() == "ENABLED":
            return True

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_16(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return False
        if value.lower() == "enabled":
            return False

    # Unknown value -> treat as enabled (safe default)
    return True


def x_read_glossary_check_metadata__mutmut_17(step_metadata: dict[str, Any]) -> bool:
    """Read glossary_check metadata from a mission step definition.

    This function interprets the ``glossary_check`` field from mission.yaml
    step definitions.

    Args:
        step_metadata: Step metadata dictionary from mission.yaml.

    Returns:
        True if glossary checks are enabled for this step, False otherwise.
        Default is True (enabled) per FR-020.
    """
    value = step_metadata.get("glossary_check")

    if value is None:
        # Not specified -> enabled by default (FR-020)
        return True

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() == "disabled":
            return False
        if value.lower() == "enabled":
            return True

    # Unknown value -> treat as enabled (safe default)
    return False

x_read_glossary_check_metadata__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_read_glossary_check_metadata__mutmut_1': x_read_glossary_check_metadata__mutmut_1, 
    'x_read_glossary_check_metadata__mutmut_2': x_read_glossary_check_metadata__mutmut_2, 
    'x_read_glossary_check_metadata__mutmut_3': x_read_glossary_check_metadata__mutmut_3, 
    'x_read_glossary_check_metadata__mutmut_4': x_read_glossary_check_metadata__mutmut_4, 
    'x_read_glossary_check_metadata__mutmut_5': x_read_glossary_check_metadata__mutmut_5, 
    'x_read_glossary_check_metadata__mutmut_6': x_read_glossary_check_metadata__mutmut_6, 
    'x_read_glossary_check_metadata__mutmut_7': x_read_glossary_check_metadata__mutmut_7, 
    'x_read_glossary_check_metadata__mutmut_8': x_read_glossary_check_metadata__mutmut_8, 
    'x_read_glossary_check_metadata__mutmut_9': x_read_glossary_check_metadata__mutmut_9, 
    'x_read_glossary_check_metadata__mutmut_10': x_read_glossary_check_metadata__mutmut_10, 
    'x_read_glossary_check_metadata__mutmut_11': x_read_glossary_check_metadata__mutmut_11, 
    'x_read_glossary_check_metadata__mutmut_12': x_read_glossary_check_metadata__mutmut_12, 
    'x_read_glossary_check_metadata__mutmut_13': x_read_glossary_check_metadata__mutmut_13, 
    'x_read_glossary_check_metadata__mutmut_14': x_read_glossary_check_metadata__mutmut_14, 
    'x_read_glossary_check_metadata__mutmut_15': x_read_glossary_check_metadata__mutmut_15, 
    'x_read_glossary_check_metadata__mutmut_16': x_read_glossary_check_metadata__mutmut_16, 
    'x_read_glossary_check_metadata__mutmut_17': x_read_glossary_check_metadata__mutmut_17
}
x_read_glossary_check_metadata__mutmut_orig.__name__ = 'x_read_glossary_check_metadata'


def run_with_glossary(
    context: Any,
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Any:
    args = [context, repo_root, runtime_strictness, interaction_mode]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_run_with_glossary__mutmut_orig, x_run_with_glossary__mutmut_mutants, args, kwargs, None)


def x_run_with_glossary__mutmut_orig(
    context: Any,
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Any:
    """Run the glossary pipeline on a PrimitiveExecutionContext.

    This is the primary hook point for mission primitive executors.
    Call this before executing the primitive logic to ensure glossary
    checks run when ``glossary_check`` is enabled (the default).

    Args:
        context: PrimitiveExecutionContext to process.
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Processed context with glossary fields populated.

    Raises:
        BlockedByConflict: Generation blocked by unresolved conflicts.
        DeferredToAsync: Conflict resolution deferred.
        AbortResume: User aborted resume.
    """
    processor = attach_glossary_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )
    return processor(context)


def x_run_with_glossary__mutmut_1(
    context: Any,
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "XXinteractiveXX",
) -> Any:
    """Run the glossary pipeline on a PrimitiveExecutionContext.

    This is the primary hook point for mission primitive executors.
    Call this before executing the primitive logic to ensure glossary
    checks run when ``glossary_check`` is enabled (the default).

    Args:
        context: PrimitiveExecutionContext to process.
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Processed context with glossary fields populated.

    Raises:
        BlockedByConflict: Generation blocked by unresolved conflicts.
        DeferredToAsync: Conflict resolution deferred.
        AbortResume: User aborted resume.
    """
    processor = attach_glossary_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )
    return processor(context)


def x_run_with_glossary__mutmut_2(
    context: Any,
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "INTERACTIVE",
) -> Any:
    """Run the glossary pipeline on a PrimitiveExecutionContext.

    This is the primary hook point for mission primitive executors.
    Call this before executing the primitive logic to ensure glossary
    checks run when ``glossary_check`` is enabled (the default).

    Args:
        context: PrimitiveExecutionContext to process.
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Processed context with glossary fields populated.

    Raises:
        BlockedByConflict: Generation blocked by unresolved conflicts.
        DeferredToAsync: Conflict resolution deferred.
        AbortResume: User aborted resume.
    """
    processor = attach_glossary_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )
    return processor(context)


def x_run_with_glossary__mutmut_3(
    context: Any,
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Any:
    """Run the glossary pipeline on a PrimitiveExecutionContext.

    This is the primary hook point for mission primitive executors.
    Call this before executing the primitive logic to ensure glossary
    checks run when ``glossary_check`` is enabled (the default).

    Args:
        context: PrimitiveExecutionContext to process.
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Processed context with glossary fields populated.

    Raises:
        BlockedByConflict: Generation blocked by unresolved conflicts.
        DeferredToAsync: Conflict resolution deferred.
        AbortResume: User aborted resume.
    """
    processor = None
    return processor(context)


def x_run_with_glossary__mutmut_4(
    context: Any,
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Any:
    """Run the glossary pipeline on a PrimitiveExecutionContext.

    This is the primary hook point for mission primitive executors.
    Call this before executing the primitive logic to ensure glossary
    checks run when ``glossary_check`` is enabled (the default).

    Args:
        context: PrimitiveExecutionContext to process.
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Processed context with glossary fields populated.

    Raises:
        BlockedByConflict: Generation blocked by unresolved conflicts.
        DeferredToAsync: Conflict resolution deferred.
        AbortResume: User aborted resume.
    """
    processor = attach_glossary_pipeline(
        repo_root=None,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )
    return processor(context)


def x_run_with_glossary__mutmut_5(
    context: Any,
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Any:
    """Run the glossary pipeline on a PrimitiveExecutionContext.

    This is the primary hook point for mission primitive executors.
    Call this before executing the primitive logic to ensure glossary
    checks run when ``glossary_check`` is enabled (the default).

    Args:
        context: PrimitiveExecutionContext to process.
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Processed context with glossary fields populated.

    Raises:
        BlockedByConflict: Generation blocked by unresolved conflicts.
        DeferredToAsync: Conflict resolution deferred.
        AbortResume: User aborted resume.
    """
    processor = attach_glossary_pipeline(
        repo_root=repo_root,
        runtime_strictness=None,
        interaction_mode=interaction_mode,
    )
    return processor(context)


def x_run_with_glossary__mutmut_6(
    context: Any,
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Any:
    """Run the glossary pipeline on a PrimitiveExecutionContext.

    This is the primary hook point for mission primitive executors.
    Call this before executing the primitive logic to ensure glossary
    checks run when ``glossary_check`` is enabled (the default).

    Args:
        context: PrimitiveExecutionContext to process.
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Processed context with glossary fields populated.

    Raises:
        BlockedByConflict: Generation blocked by unresolved conflicts.
        DeferredToAsync: Conflict resolution deferred.
        AbortResume: User aborted resume.
    """
    processor = attach_glossary_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=None,
    )
    return processor(context)


def x_run_with_glossary__mutmut_7(
    context: Any,
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Any:
    """Run the glossary pipeline on a PrimitiveExecutionContext.

    This is the primary hook point for mission primitive executors.
    Call this before executing the primitive logic to ensure glossary
    checks run when ``glossary_check`` is enabled (the default).

    Args:
        context: PrimitiveExecutionContext to process.
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Processed context with glossary fields populated.

    Raises:
        BlockedByConflict: Generation blocked by unresolved conflicts.
        DeferredToAsync: Conflict resolution deferred.
        AbortResume: User aborted resume.
    """
    processor = attach_glossary_pipeline(
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )
    return processor(context)


def x_run_with_glossary__mutmut_8(
    context: Any,
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Any:
    """Run the glossary pipeline on a PrimitiveExecutionContext.

    This is the primary hook point for mission primitive executors.
    Call this before executing the primitive logic to ensure glossary
    checks run when ``glossary_check`` is enabled (the default).

    Args:
        context: PrimitiveExecutionContext to process.
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Processed context with glossary fields populated.

    Raises:
        BlockedByConflict: Generation blocked by unresolved conflicts.
        DeferredToAsync: Conflict resolution deferred.
        AbortResume: User aborted resume.
    """
    processor = attach_glossary_pipeline(
        repo_root=repo_root,
        interaction_mode=interaction_mode,
    )
    return processor(context)


def x_run_with_glossary__mutmut_9(
    context: Any,
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Any:
    """Run the glossary pipeline on a PrimitiveExecutionContext.

    This is the primary hook point for mission primitive executors.
    Call this before executing the primitive logic to ensure glossary
    checks run when ``glossary_check`` is enabled (the default).

    Args:
        context: PrimitiveExecutionContext to process.
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Processed context with glossary fields populated.

    Raises:
        BlockedByConflict: Generation blocked by unresolved conflicts.
        DeferredToAsync: Conflict resolution deferred.
        AbortResume: User aborted resume.
    """
    processor = attach_glossary_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        )
    return processor(context)


def x_run_with_glossary__mutmut_10(
    context: Any,
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Any:
    """Run the glossary pipeline on a PrimitiveExecutionContext.

    This is the primary hook point for mission primitive executors.
    Call this before executing the primitive logic to ensure glossary
    checks run when ``glossary_check`` is enabled (the default).

    Args:
        context: PrimitiveExecutionContext to process.
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Processed context with glossary fields populated.

    Raises:
        BlockedByConflict: Generation blocked by unresolved conflicts.
        DeferredToAsync: Conflict resolution deferred.
        AbortResume: User aborted resume.
    """
    processor = attach_glossary_pipeline(
        repo_root=repo_root,
        runtime_strictness=runtime_strictness,
        interaction_mode=interaction_mode,
    )
    return processor(None)

x_run_with_glossary__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_run_with_glossary__mutmut_1': x_run_with_glossary__mutmut_1, 
    'x_run_with_glossary__mutmut_2': x_run_with_glossary__mutmut_2, 
    'x_run_with_glossary__mutmut_3': x_run_with_glossary__mutmut_3, 
    'x_run_with_glossary__mutmut_4': x_run_with_glossary__mutmut_4, 
    'x_run_with_glossary__mutmut_5': x_run_with_glossary__mutmut_5, 
    'x_run_with_glossary__mutmut_6': x_run_with_glossary__mutmut_6, 
    'x_run_with_glossary__mutmut_7': x_run_with_glossary__mutmut_7, 
    'x_run_with_glossary__mutmut_8': x_run_with_glossary__mutmut_8, 
    'x_run_with_glossary__mutmut_9': x_run_with_glossary__mutmut_9, 
    'x_run_with_glossary__mutmut_10': x_run_with_glossary__mutmut_10
}
x_run_with_glossary__mutmut_orig.__name__ = 'x_run_with_glossary'


class GlossaryAwarePrimitiveRunner:
    """Runner that wraps any primitive function with the glossary pipeline.

    This class provides the concrete call site for integrating the glossary
    pipeline into mission primitive execution. Mission executors instantiate
    a runner and call ``execute()`` to run a primitive with glossary checks.

    The runner:
    1. Runs the glossary middleware pipeline on the context (pre-processing)
    2. Executes the primitive function with the processed context
    3. Returns the primitive's result

    If the glossary pipeline raises BlockedByConflict (after clarification
    has had its chance), the exception propagates to the caller.

    Usage::

        runner = GlossaryAwarePrimitiveRunner(
            repo_root=Path("."),
            runtime_strictness=Strictness.MEDIUM,
        )
        result = runner.execute(my_primitive_fn, context)
    """

    def __init__(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "interactive",
    ) -> None:
        args = [repo_root, runtime_strictness, interaction_mode]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_orig(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "interactive",
    ) -> None:
        """Initialize the runner.

        Args:
            repo_root: Path to repository root.
            runtime_strictness: CLI ``--strictness`` override (highest precedence).
            interaction_mode: ``"interactive"`` or ``"non-interactive"``.
        """
        self.repo_root = repo_root
        self.runtime_strictness = runtime_strictness
        self.interaction_mode = interaction_mode
        self._processor = attach_glossary_pipeline(
            repo_root=repo_root,
            runtime_strictness=runtime_strictness,
            interaction_mode=interaction_mode,
        )

    def xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_1(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "XXinteractiveXX",
    ) -> None:
        """Initialize the runner.

        Args:
            repo_root: Path to repository root.
            runtime_strictness: CLI ``--strictness`` override (highest precedence).
            interaction_mode: ``"interactive"`` or ``"non-interactive"``.
        """
        self.repo_root = repo_root
        self.runtime_strictness = runtime_strictness
        self.interaction_mode = interaction_mode
        self._processor = attach_glossary_pipeline(
            repo_root=repo_root,
            runtime_strictness=runtime_strictness,
            interaction_mode=interaction_mode,
        )

    def xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_2(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "INTERACTIVE",
    ) -> None:
        """Initialize the runner.

        Args:
            repo_root: Path to repository root.
            runtime_strictness: CLI ``--strictness`` override (highest precedence).
            interaction_mode: ``"interactive"`` or ``"non-interactive"``.
        """
        self.repo_root = repo_root
        self.runtime_strictness = runtime_strictness
        self.interaction_mode = interaction_mode
        self._processor = attach_glossary_pipeline(
            repo_root=repo_root,
            runtime_strictness=runtime_strictness,
            interaction_mode=interaction_mode,
        )

    def xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_3(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "interactive",
    ) -> None:
        """Initialize the runner.

        Args:
            repo_root: Path to repository root.
            runtime_strictness: CLI ``--strictness`` override (highest precedence).
            interaction_mode: ``"interactive"`` or ``"non-interactive"``.
        """
        self.repo_root = None
        self.runtime_strictness = runtime_strictness
        self.interaction_mode = interaction_mode
        self._processor = attach_glossary_pipeline(
            repo_root=repo_root,
            runtime_strictness=runtime_strictness,
            interaction_mode=interaction_mode,
        )

    def xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_4(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "interactive",
    ) -> None:
        """Initialize the runner.

        Args:
            repo_root: Path to repository root.
            runtime_strictness: CLI ``--strictness`` override (highest precedence).
            interaction_mode: ``"interactive"`` or ``"non-interactive"``.
        """
        self.repo_root = repo_root
        self.runtime_strictness = None
        self.interaction_mode = interaction_mode
        self._processor = attach_glossary_pipeline(
            repo_root=repo_root,
            runtime_strictness=runtime_strictness,
            interaction_mode=interaction_mode,
        )

    def xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_5(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "interactive",
    ) -> None:
        """Initialize the runner.

        Args:
            repo_root: Path to repository root.
            runtime_strictness: CLI ``--strictness`` override (highest precedence).
            interaction_mode: ``"interactive"`` or ``"non-interactive"``.
        """
        self.repo_root = repo_root
        self.runtime_strictness = runtime_strictness
        self.interaction_mode = None
        self._processor = attach_glossary_pipeline(
            repo_root=repo_root,
            runtime_strictness=runtime_strictness,
            interaction_mode=interaction_mode,
        )

    def xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_6(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "interactive",
    ) -> None:
        """Initialize the runner.

        Args:
            repo_root: Path to repository root.
            runtime_strictness: CLI ``--strictness`` override (highest precedence).
            interaction_mode: ``"interactive"`` or ``"non-interactive"``.
        """
        self.repo_root = repo_root
        self.runtime_strictness = runtime_strictness
        self.interaction_mode = interaction_mode
        self._processor = None

    def xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_7(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "interactive",
    ) -> None:
        """Initialize the runner.

        Args:
            repo_root: Path to repository root.
            runtime_strictness: CLI ``--strictness`` override (highest precedence).
            interaction_mode: ``"interactive"`` or ``"non-interactive"``.
        """
        self.repo_root = repo_root
        self.runtime_strictness = runtime_strictness
        self.interaction_mode = interaction_mode
        self._processor = attach_glossary_pipeline(
            repo_root=None,
            runtime_strictness=runtime_strictness,
            interaction_mode=interaction_mode,
        )

    def xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_8(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "interactive",
    ) -> None:
        """Initialize the runner.

        Args:
            repo_root: Path to repository root.
            runtime_strictness: CLI ``--strictness`` override (highest precedence).
            interaction_mode: ``"interactive"`` or ``"non-interactive"``.
        """
        self.repo_root = repo_root
        self.runtime_strictness = runtime_strictness
        self.interaction_mode = interaction_mode
        self._processor = attach_glossary_pipeline(
            repo_root=repo_root,
            runtime_strictness=None,
            interaction_mode=interaction_mode,
        )

    def xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_9(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "interactive",
    ) -> None:
        """Initialize the runner.

        Args:
            repo_root: Path to repository root.
            runtime_strictness: CLI ``--strictness`` override (highest precedence).
            interaction_mode: ``"interactive"`` or ``"non-interactive"``.
        """
        self.repo_root = repo_root
        self.runtime_strictness = runtime_strictness
        self.interaction_mode = interaction_mode
        self._processor = attach_glossary_pipeline(
            repo_root=repo_root,
            runtime_strictness=runtime_strictness,
            interaction_mode=None,
        )

    def xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_10(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "interactive",
    ) -> None:
        """Initialize the runner.

        Args:
            repo_root: Path to repository root.
            runtime_strictness: CLI ``--strictness`` override (highest precedence).
            interaction_mode: ``"interactive"`` or ``"non-interactive"``.
        """
        self.repo_root = repo_root
        self.runtime_strictness = runtime_strictness
        self.interaction_mode = interaction_mode
        self._processor = attach_glossary_pipeline(
            runtime_strictness=runtime_strictness,
            interaction_mode=interaction_mode,
        )

    def xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_11(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "interactive",
    ) -> None:
        """Initialize the runner.

        Args:
            repo_root: Path to repository root.
            runtime_strictness: CLI ``--strictness`` override (highest precedence).
            interaction_mode: ``"interactive"`` or ``"non-interactive"``.
        """
        self.repo_root = repo_root
        self.runtime_strictness = runtime_strictness
        self.interaction_mode = interaction_mode
        self._processor = attach_glossary_pipeline(
            repo_root=repo_root,
            interaction_mode=interaction_mode,
        )

    def xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_12(
        self,
        repo_root: Path,
        runtime_strictness: Optional[Strictness] = None,
        interaction_mode: str = "interactive",
    ) -> None:
        """Initialize the runner.

        Args:
            repo_root: Path to repository root.
            runtime_strictness: CLI ``--strictness`` override (highest precedence).
            interaction_mode: ``"interactive"`` or ``"non-interactive"``.
        """
        self.repo_root = repo_root
        self.runtime_strictness = runtime_strictness
        self.interaction_mode = interaction_mode
        self._processor = attach_glossary_pipeline(
            repo_root=repo_root,
            runtime_strictness=runtime_strictness,
            )
    
    xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_1': xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_1, 
        'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_2': xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_2, 
        'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_3': xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_3, 
        'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_4': xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_4, 
        'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_5': xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_5, 
        'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_6': xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_6, 
        'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_7': xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_7, 
        'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_8': xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_8, 
        'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_9': xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_9, 
        'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_10': xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_10, 
        'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_11': xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_11, 
        'xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_12': xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_12
    }
    xǁGlossaryAwarePrimitiveRunnerǁ__init____mutmut_orig.__name__ = 'xǁGlossaryAwarePrimitiveRunnerǁ__init__'

    def execute(
        self,
        primitive_fn: Callable[..., Any],
        context: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        args = [primitive_fn, context, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_orig'), object.__getattribute__(self, 'xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_mutants'), args, kwargs, self)

    def xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_orig(
        self,
        primitive_fn: Callable[..., Any],
        context: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Execute a primitive function with glossary pre-processing.

        Args:
            primitive_fn: The primitive function to execute.
                Must accept a PrimitiveExecutionContext as first argument.
            context: PrimitiveExecutionContext to process.
            *args: Extra positional arguments forwarded to primitive_fn.
            **kwargs: Extra keyword arguments forwarded to primitive_fn.

        Returns:
            Whatever primitive_fn returns.

        Raises:
            BlockedByConflict: If unresolved conflicts block generation
                (after clarification has run).
            DeferredToAsync: If user deferred conflict resolution.
            AbortResume: If user aborted resume.
        """
        processed_context = self._processor(context)
        return primitive_fn(processed_context, *args, **kwargs)

    def xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_1(
        self,
        primitive_fn: Callable[..., Any],
        context: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Execute a primitive function with glossary pre-processing.

        Args:
            primitive_fn: The primitive function to execute.
                Must accept a PrimitiveExecutionContext as first argument.
            context: PrimitiveExecutionContext to process.
            *args: Extra positional arguments forwarded to primitive_fn.
            **kwargs: Extra keyword arguments forwarded to primitive_fn.

        Returns:
            Whatever primitive_fn returns.

        Raises:
            BlockedByConflict: If unresolved conflicts block generation
                (after clarification has run).
            DeferredToAsync: If user deferred conflict resolution.
            AbortResume: If user aborted resume.
        """
        processed_context = None
        return primitive_fn(processed_context, *args, **kwargs)

    def xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_2(
        self,
        primitive_fn: Callable[..., Any],
        context: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Execute a primitive function with glossary pre-processing.

        Args:
            primitive_fn: The primitive function to execute.
                Must accept a PrimitiveExecutionContext as first argument.
            context: PrimitiveExecutionContext to process.
            *args: Extra positional arguments forwarded to primitive_fn.
            **kwargs: Extra keyword arguments forwarded to primitive_fn.

        Returns:
            Whatever primitive_fn returns.

        Raises:
            BlockedByConflict: If unresolved conflicts block generation
                (after clarification has run).
            DeferredToAsync: If user deferred conflict resolution.
            AbortResume: If user aborted resume.
        """
        processed_context = self._processor(None)
        return primitive_fn(processed_context, *args, **kwargs)

    def xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_3(
        self,
        primitive_fn: Callable[..., Any],
        context: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Execute a primitive function with glossary pre-processing.

        Args:
            primitive_fn: The primitive function to execute.
                Must accept a PrimitiveExecutionContext as first argument.
            context: PrimitiveExecutionContext to process.
            *args: Extra positional arguments forwarded to primitive_fn.
            **kwargs: Extra keyword arguments forwarded to primitive_fn.

        Returns:
            Whatever primitive_fn returns.

        Raises:
            BlockedByConflict: If unresolved conflicts block generation
                (after clarification has run).
            DeferredToAsync: If user deferred conflict resolution.
            AbortResume: If user aborted resume.
        """
        processed_context = self._processor(context)
        return primitive_fn(None, *args, **kwargs)

    def xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_4(
        self,
        primitive_fn: Callable[..., Any],
        context: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Execute a primitive function with glossary pre-processing.

        Args:
            primitive_fn: The primitive function to execute.
                Must accept a PrimitiveExecutionContext as first argument.
            context: PrimitiveExecutionContext to process.
            *args: Extra positional arguments forwarded to primitive_fn.
            **kwargs: Extra keyword arguments forwarded to primitive_fn.

        Returns:
            Whatever primitive_fn returns.

        Raises:
            BlockedByConflict: If unresolved conflicts block generation
                (after clarification has run).
            DeferredToAsync: If user deferred conflict resolution.
            AbortResume: If user aborted resume.
        """
        processed_context = self._processor(context)
        return primitive_fn(*args, **kwargs)

    def xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_5(
        self,
        primitive_fn: Callable[..., Any],
        context: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Execute a primitive function with glossary pre-processing.

        Args:
            primitive_fn: The primitive function to execute.
                Must accept a PrimitiveExecutionContext as first argument.
            context: PrimitiveExecutionContext to process.
            *args: Extra positional arguments forwarded to primitive_fn.
            **kwargs: Extra keyword arguments forwarded to primitive_fn.

        Returns:
            Whatever primitive_fn returns.

        Raises:
            BlockedByConflict: If unresolved conflicts block generation
                (after clarification has run).
            DeferredToAsync: If user deferred conflict resolution.
            AbortResume: If user aborted resume.
        """
        processed_context = self._processor(context)
        return primitive_fn(processed_context, **kwargs)

    def xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_6(
        self,
        primitive_fn: Callable[..., Any],
        context: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Execute a primitive function with glossary pre-processing.

        Args:
            primitive_fn: The primitive function to execute.
                Must accept a PrimitiveExecutionContext as first argument.
            context: PrimitiveExecutionContext to process.
            *args: Extra positional arguments forwarded to primitive_fn.
            **kwargs: Extra keyword arguments forwarded to primitive_fn.

        Returns:
            Whatever primitive_fn returns.

        Raises:
            BlockedByConflict: If unresolved conflicts block generation
                (after clarification has run).
            DeferredToAsync: If user deferred conflict resolution.
            AbortResume: If user aborted resume.
        """
        processed_context = self._processor(context)
        return primitive_fn(processed_context, *args, )
    
    xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_1': xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_1, 
        'xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_2': xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_2, 
        'xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_3': xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_3, 
        'xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_4': xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_4, 
        'xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_5': xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_5, 
        'xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_6': xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_6
    }
    xǁGlossaryAwarePrimitiveRunnerǁexecute__mutmut_orig.__name__ = 'xǁGlossaryAwarePrimitiveRunnerǁexecute'


def glossary_enabled(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[..., Any]:
    args = [repo_root, runtime_strictness, interaction_mode]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_glossary_enabled__mutmut_orig, x_glossary_enabled__mutmut_mutants, args, kwargs, None)


def x_glossary_enabled__mutmut_orig(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "interactive",
) -> Callable[..., Any]:
    """Decorator that runs the glossary pipeline before a mission primitive.

    The decorated function's first positional argument must be a
    ``PrimitiveExecutionContext``. The pipeline processes the context
    before the function body executes.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Decorator function.

    Example::

        @glossary_enabled(repo_root=Path("."))
        def execute_specify(context: PrimitiveExecutionContext) -> dict:
            # context has already been processed by the glossary pipeline
            return {"result": context.effective_strictness}
    """
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)
        def wrapper(context: Any, *args: Any, **kwargs: Any) -> Any:
            processed = run_with_glossary(
                context=context,
                repo_root=repo_root,
                runtime_strictness=runtime_strictness,
                interaction_mode=interaction_mode,
            )
            return fn(processed, *args, **kwargs)
        return wrapper
    return decorator


def x_glossary_enabled__mutmut_1(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "XXinteractiveXX",
) -> Callable[..., Any]:
    """Decorator that runs the glossary pipeline before a mission primitive.

    The decorated function's first positional argument must be a
    ``PrimitiveExecutionContext``. The pipeline processes the context
    before the function body executes.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Decorator function.

    Example::

        @glossary_enabled(repo_root=Path("."))
        def execute_specify(context: PrimitiveExecutionContext) -> dict:
            # context has already been processed by the glossary pipeline
            return {"result": context.effective_strictness}
    """
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)
        def wrapper(context: Any, *args: Any, **kwargs: Any) -> Any:
            processed = run_with_glossary(
                context=context,
                repo_root=repo_root,
                runtime_strictness=runtime_strictness,
                interaction_mode=interaction_mode,
            )
            return fn(processed, *args, **kwargs)
        return wrapper
    return decorator


def x_glossary_enabled__mutmut_2(
    repo_root: Path,
    runtime_strictness: Optional[Strictness] = None,
    interaction_mode: str = "INTERACTIVE",
) -> Callable[..., Any]:
    """Decorator that runs the glossary pipeline before a mission primitive.

    The decorated function's first positional argument must be a
    ``PrimitiveExecutionContext``. The pipeline processes the context
    before the function body executes.

    Args:
        repo_root: Path to repository root.
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non_interactive"``.

    Returns:
        Decorator function.

    Example::

        @glossary_enabled(repo_root=Path("."))
        def execute_specify(context: PrimitiveExecutionContext) -> dict:
            # context has already been processed by the glossary pipeline
            return {"result": context.effective_strictness}
    """
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)
        def wrapper(context: Any, *args: Any, **kwargs: Any) -> Any:
            processed = run_with_glossary(
                context=context,
                repo_root=repo_root,
                runtime_strictness=runtime_strictness,
                interaction_mode=interaction_mode,
            )
            return fn(processed, *args, **kwargs)
        return wrapper
    return decorator

x_glossary_enabled__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_glossary_enabled__mutmut_1': x_glossary_enabled__mutmut_1, 
    'x_glossary_enabled__mutmut_2': x_glossary_enabled__mutmut_2
}
x_glossary_enabled__mutmut_orig.__name__ = 'x_glossary_enabled'
