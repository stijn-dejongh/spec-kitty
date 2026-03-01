"""Interactive clarification middleware (WP06, WP08).

This module implements the ClarificationMiddleware that handles interactive
conflict resolution. It emits 3 event types at its boundaries:

- GlossaryClarificationRequested: when user defers a conflict
- GlossaryClarificationResolved: when user selects a candidate sense
- GlossarySenseUpdated: when user provides a custom sense definition

Pipeline position: Layer 4 (after extraction, semantic check, and gate)
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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


class ClarificationMiddleware:
    """Middleware for interactive conflict clarification.

    When conflicts are detected and generation is not blocked (or after
    the user resolves a blocking conflict), this middleware handles:

    1. Presenting conflicts to the user for resolution
    2. Accepting user's choice: select a candidate sense OR provide custom
    3. Emitting appropriate events for each resolution action
    4. Updating the execution context with resolved senses

    Usage:
        clarification = ClarificationMiddleware(
            repo_root=Path("."),
            prompt_fn=my_prompt_function,
        )
        context = clarification.process(context)
    """

    def __init__(
        self,
        repo_root: Path | None = None,
        prompt_fn: Any = None,
        glossary_store: Any = None,
    ) -> None:
        args = [repo_root, prompt_fn, glossary_store]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁClarificationMiddlewareǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁClarificationMiddlewareǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁClarificationMiddlewareǁ__init____mutmut_orig(
        self,
        repo_root: Path | None = None,
        prompt_fn: Any = None,
        glossary_store: Any = None,
    ) -> None:
        """Initialize clarification middleware.

        Args:
            repo_root: Repository root for event log persistence.
                If None, events are logged but not persisted.
            prompt_fn: Optional function to prompt user for resolution.
                Signature: (conflict, candidates) -> (choice: str, custom_def: str | None)
                Returns ("select", None) with index in conflict.selected_index
                or ("custom", "definition text") for custom sense.
                If None, all conflicts are deferred.
            glossary_store: Optional GlossaryStore instance. When provided,
                custom senses are applied in-memory immediately after
                clarification so subsequent checks in the same run see
                updated meanings.
        """
        self.repo_root = repo_root
        self.prompt_fn = prompt_fn
        self.glossary_store = glossary_store

    def xǁClarificationMiddlewareǁ__init____mutmut_1(
        self,
        repo_root: Path | None = None,
        prompt_fn: Any = None,
        glossary_store: Any = None,
    ) -> None:
        """Initialize clarification middleware.

        Args:
            repo_root: Repository root for event log persistence.
                If None, events are logged but not persisted.
            prompt_fn: Optional function to prompt user for resolution.
                Signature: (conflict, candidates) -> (choice: str, custom_def: str | None)
                Returns ("select", None) with index in conflict.selected_index
                or ("custom", "definition text") for custom sense.
                If None, all conflicts are deferred.
            glossary_store: Optional GlossaryStore instance. When provided,
                custom senses are applied in-memory immediately after
                clarification so subsequent checks in the same run see
                updated meanings.
        """
        self.repo_root = None
        self.prompt_fn = prompt_fn
        self.glossary_store = glossary_store

    def xǁClarificationMiddlewareǁ__init____mutmut_2(
        self,
        repo_root: Path | None = None,
        prompt_fn: Any = None,
        glossary_store: Any = None,
    ) -> None:
        """Initialize clarification middleware.

        Args:
            repo_root: Repository root for event log persistence.
                If None, events are logged but not persisted.
            prompt_fn: Optional function to prompt user for resolution.
                Signature: (conflict, candidates) -> (choice: str, custom_def: str | None)
                Returns ("select", None) with index in conflict.selected_index
                or ("custom", "definition text") for custom sense.
                If None, all conflicts are deferred.
            glossary_store: Optional GlossaryStore instance. When provided,
                custom senses are applied in-memory immediately after
                clarification so subsequent checks in the same run see
                updated meanings.
        """
        self.repo_root = repo_root
        self.prompt_fn = None
        self.glossary_store = glossary_store

    def xǁClarificationMiddlewareǁ__init____mutmut_3(
        self,
        repo_root: Path | None = None,
        prompt_fn: Any = None,
        glossary_store: Any = None,
    ) -> None:
        """Initialize clarification middleware.

        Args:
            repo_root: Repository root for event log persistence.
                If None, events are logged but not persisted.
            prompt_fn: Optional function to prompt user for resolution.
                Signature: (conflict, candidates) -> (choice: str, custom_def: str | None)
                Returns ("select", None) with index in conflict.selected_index
                or ("custom", "definition text") for custom sense.
                If None, all conflicts are deferred.
            glossary_store: Optional GlossaryStore instance. When provided,
                custom senses are applied in-memory immediately after
                clarification so subsequent checks in the same run see
                updated meanings.
        """
        self.repo_root = repo_root
        self.prompt_fn = prompt_fn
        self.glossary_store = None
    
    xǁClarificationMiddlewareǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁClarificationMiddlewareǁ__init____mutmut_1': xǁClarificationMiddlewareǁ__init____mutmut_1, 
        'xǁClarificationMiddlewareǁ__init____mutmut_2': xǁClarificationMiddlewareǁ__init____mutmut_2, 
        'xǁClarificationMiddlewareǁ__init____mutmut_3': xǁClarificationMiddlewareǁ__init____mutmut_3
    }
    xǁClarificationMiddlewareǁ__init____mutmut_orig.__name__ = 'xǁClarificationMiddlewareǁ__init__'

    def process(
        self,
        context: Any,
    ) -> Any:
        args = [context]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁClarificationMiddlewareǁprocess__mutmut_orig'), object.__getattribute__(self, 'xǁClarificationMiddlewareǁprocess__mutmut_mutants'), args, kwargs, self)

    def xǁClarificationMiddlewareǁprocess__mutmut_orig(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_1(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = None
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_2(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(None, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_3(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, None, [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_4(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", None)
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_5(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr("conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_6(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_7(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", )
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_8(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "XXconflictsXX", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_9(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "CONFLICTS", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_10(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_11(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = None

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_12(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = None
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_13(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(None)
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_14(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(None, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_15(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, None, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_16(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, None)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_17(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_18(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_19(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, )

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_20(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_21(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = None
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_22(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        None, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_23(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, None
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_24(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_25(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_26(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        None,
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_27(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        None,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_28(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        None,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_29(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_30(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_31(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_32(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "XXPrompt function failed for %s: %sXX",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_33(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_34(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "PROMPT FUNCTION FAILED FOR %S: %S",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_35(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    break

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_36(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" or conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_37(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice != "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_38(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "XXselectXX" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_39(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "SELECT" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_40(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = None
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_41(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(None, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_42(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, None, 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_43(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", None)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_44(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr("selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_45(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_46(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", )
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_47(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "XXselected_indexXX", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_48(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "SELECTED_INDEX", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_49(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 1)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_50(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 1 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_51(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 < selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_52(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx <= len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_53(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = None
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_54(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = None
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_55(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[1]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_56(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        None, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_57(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, None, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_58(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, None, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_59(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, None
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_60(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_61(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_62(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_63(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_64(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(None)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_65(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" or custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_66(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice != "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_67(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "XXcustomXX" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_68(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "CUSTOM" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_69(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        None, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_70(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, None, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_71(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, None, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_72(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, None
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_73(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_74(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_75(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_76(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_77(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(None)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_78(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = None
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_79(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_80(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(None, "conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_81(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, None, remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_82(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", None)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_83(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr("conflicts", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_84(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_85(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", )
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_86(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "XXconflictsXX", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_87(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "CONFLICTS", remaining)
        setattr(context, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_88(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(None, "resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_89(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, None, resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_90(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", None)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_91(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr("resolved_conflicts", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_92(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_93(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "resolved_conflicts", )

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_94(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "XXresolved_conflictsXX", resolved_conflicts)

        return context

    def xǁClarificationMiddlewareǁprocess__mutmut_95(
        self,
        context: Any,
    ) -> Any:
        """Process conflicts requiring clarification.

        For each unresolved conflict in context.conflicts, either:
        - Prompt user for resolution (if prompt_fn is provided)
        - Defer to async (emit GlossaryClarificationRequested)

        Args:
            context: Execution context with conflicts populated

        Returns:
            Updated context with resolved conflicts removed
        """
        conflicts = getattr(context, "conflicts", [])
        if not conflicts:
            return context

        resolved_conflicts: list[Any] = []

        for conflict in conflicts:
            conflict_id = str(uuid.uuid4())
            # Always emit the request event first so any eventual resolution
            # references an existing clarification request.
            self._emit_requested(conflict, conflict_id, context)

            if self.prompt_fn is not None:
                # Interactive mode: prompt user
                try:
                    choice, custom_def = self.prompt_fn(
                        conflict, conflict.candidate_senses
                    )
                except Exception as exc:
                    logger.error(
                        "Prompt function failed for %s: %s",
                        conflict.term.surface_text,
                        exc,
                    )
                    # Defer on prompt failure
                    continue

                if choice == "select" and conflict.candidate_senses:
                    # User selected a candidate sense
                    selected_idx = getattr(conflict, "selected_index", 0)
                    if 0 <= selected_idx < len(conflict.candidate_senses):
                        selected_sense = conflict.candidate_senses[selected_idx]
                    else:
                        selected_sense = conflict.candidate_senses[0]
                    self._handle_candidate_selection(
                        conflict, conflict_id, selected_sense, context
                    )
                    resolved_conflicts.append(conflict)
                elif choice == "custom" and custom_def:
                    # User provided custom definition
                    self._handle_custom_sense(
                        conflict, conflict_id, custom_def, context
                    )
                    resolved_conflicts.append(conflict)
                # Any other response means deferred. Request event already emitted.
            # No prompt function means deferred (request event already emitted).

        # Remove resolved conflicts from context
        remaining = [c for c in conflicts if c not in resolved_conflicts]
        setattr(context, "conflicts", remaining)
        setattr(context, "RESOLVED_CONFLICTS", resolved_conflicts)

        return context
    
    xǁClarificationMiddlewareǁprocess__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁClarificationMiddlewareǁprocess__mutmut_1': xǁClarificationMiddlewareǁprocess__mutmut_1, 
        'xǁClarificationMiddlewareǁprocess__mutmut_2': xǁClarificationMiddlewareǁprocess__mutmut_2, 
        'xǁClarificationMiddlewareǁprocess__mutmut_3': xǁClarificationMiddlewareǁprocess__mutmut_3, 
        'xǁClarificationMiddlewareǁprocess__mutmut_4': xǁClarificationMiddlewareǁprocess__mutmut_4, 
        'xǁClarificationMiddlewareǁprocess__mutmut_5': xǁClarificationMiddlewareǁprocess__mutmut_5, 
        'xǁClarificationMiddlewareǁprocess__mutmut_6': xǁClarificationMiddlewareǁprocess__mutmut_6, 
        'xǁClarificationMiddlewareǁprocess__mutmut_7': xǁClarificationMiddlewareǁprocess__mutmut_7, 
        'xǁClarificationMiddlewareǁprocess__mutmut_8': xǁClarificationMiddlewareǁprocess__mutmut_8, 
        'xǁClarificationMiddlewareǁprocess__mutmut_9': xǁClarificationMiddlewareǁprocess__mutmut_9, 
        'xǁClarificationMiddlewareǁprocess__mutmut_10': xǁClarificationMiddlewareǁprocess__mutmut_10, 
        'xǁClarificationMiddlewareǁprocess__mutmut_11': xǁClarificationMiddlewareǁprocess__mutmut_11, 
        'xǁClarificationMiddlewareǁprocess__mutmut_12': xǁClarificationMiddlewareǁprocess__mutmut_12, 
        'xǁClarificationMiddlewareǁprocess__mutmut_13': xǁClarificationMiddlewareǁprocess__mutmut_13, 
        'xǁClarificationMiddlewareǁprocess__mutmut_14': xǁClarificationMiddlewareǁprocess__mutmut_14, 
        'xǁClarificationMiddlewareǁprocess__mutmut_15': xǁClarificationMiddlewareǁprocess__mutmut_15, 
        'xǁClarificationMiddlewareǁprocess__mutmut_16': xǁClarificationMiddlewareǁprocess__mutmut_16, 
        'xǁClarificationMiddlewareǁprocess__mutmut_17': xǁClarificationMiddlewareǁprocess__mutmut_17, 
        'xǁClarificationMiddlewareǁprocess__mutmut_18': xǁClarificationMiddlewareǁprocess__mutmut_18, 
        'xǁClarificationMiddlewareǁprocess__mutmut_19': xǁClarificationMiddlewareǁprocess__mutmut_19, 
        'xǁClarificationMiddlewareǁprocess__mutmut_20': xǁClarificationMiddlewareǁprocess__mutmut_20, 
        'xǁClarificationMiddlewareǁprocess__mutmut_21': xǁClarificationMiddlewareǁprocess__mutmut_21, 
        'xǁClarificationMiddlewareǁprocess__mutmut_22': xǁClarificationMiddlewareǁprocess__mutmut_22, 
        'xǁClarificationMiddlewareǁprocess__mutmut_23': xǁClarificationMiddlewareǁprocess__mutmut_23, 
        'xǁClarificationMiddlewareǁprocess__mutmut_24': xǁClarificationMiddlewareǁprocess__mutmut_24, 
        'xǁClarificationMiddlewareǁprocess__mutmut_25': xǁClarificationMiddlewareǁprocess__mutmut_25, 
        'xǁClarificationMiddlewareǁprocess__mutmut_26': xǁClarificationMiddlewareǁprocess__mutmut_26, 
        'xǁClarificationMiddlewareǁprocess__mutmut_27': xǁClarificationMiddlewareǁprocess__mutmut_27, 
        'xǁClarificationMiddlewareǁprocess__mutmut_28': xǁClarificationMiddlewareǁprocess__mutmut_28, 
        'xǁClarificationMiddlewareǁprocess__mutmut_29': xǁClarificationMiddlewareǁprocess__mutmut_29, 
        'xǁClarificationMiddlewareǁprocess__mutmut_30': xǁClarificationMiddlewareǁprocess__mutmut_30, 
        'xǁClarificationMiddlewareǁprocess__mutmut_31': xǁClarificationMiddlewareǁprocess__mutmut_31, 
        'xǁClarificationMiddlewareǁprocess__mutmut_32': xǁClarificationMiddlewareǁprocess__mutmut_32, 
        'xǁClarificationMiddlewareǁprocess__mutmut_33': xǁClarificationMiddlewareǁprocess__mutmut_33, 
        'xǁClarificationMiddlewareǁprocess__mutmut_34': xǁClarificationMiddlewareǁprocess__mutmut_34, 
        'xǁClarificationMiddlewareǁprocess__mutmut_35': xǁClarificationMiddlewareǁprocess__mutmut_35, 
        'xǁClarificationMiddlewareǁprocess__mutmut_36': xǁClarificationMiddlewareǁprocess__mutmut_36, 
        'xǁClarificationMiddlewareǁprocess__mutmut_37': xǁClarificationMiddlewareǁprocess__mutmut_37, 
        'xǁClarificationMiddlewareǁprocess__mutmut_38': xǁClarificationMiddlewareǁprocess__mutmut_38, 
        'xǁClarificationMiddlewareǁprocess__mutmut_39': xǁClarificationMiddlewareǁprocess__mutmut_39, 
        'xǁClarificationMiddlewareǁprocess__mutmut_40': xǁClarificationMiddlewareǁprocess__mutmut_40, 
        'xǁClarificationMiddlewareǁprocess__mutmut_41': xǁClarificationMiddlewareǁprocess__mutmut_41, 
        'xǁClarificationMiddlewareǁprocess__mutmut_42': xǁClarificationMiddlewareǁprocess__mutmut_42, 
        'xǁClarificationMiddlewareǁprocess__mutmut_43': xǁClarificationMiddlewareǁprocess__mutmut_43, 
        'xǁClarificationMiddlewareǁprocess__mutmut_44': xǁClarificationMiddlewareǁprocess__mutmut_44, 
        'xǁClarificationMiddlewareǁprocess__mutmut_45': xǁClarificationMiddlewareǁprocess__mutmut_45, 
        'xǁClarificationMiddlewareǁprocess__mutmut_46': xǁClarificationMiddlewareǁprocess__mutmut_46, 
        'xǁClarificationMiddlewareǁprocess__mutmut_47': xǁClarificationMiddlewareǁprocess__mutmut_47, 
        'xǁClarificationMiddlewareǁprocess__mutmut_48': xǁClarificationMiddlewareǁprocess__mutmut_48, 
        'xǁClarificationMiddlewareǁprocess__mutmut_49': xǁClarificationMiddlewareǁprocess__mutmut_49, 
        'xǁClarificationMiddlewareǁprocess__mutmut_50': xǁClarificationMiddlewareǁprocess__mutmut_50, 
        'xǁClarificationMiddlewareǁprocess__mutmut_51': xǁClarificationMiddlewareǁprocess__mutmut_51, 
        'xǁClarificationMiddlewareǁprocess__mutmut_52': xǁClarificationMiddlewareǁprocess__mutmut_52, 
        'xǁClarificationMiddlewareǁprocess__mutmut_53': xǁClarificationMiddlewareǁprocess__mutmut_53, 
        'xǁClarificationMiddlewareǁprocess__mutmut_54': xǁClarificationMiddlewareǁprocess__mutmut_54, 
        'xǁClarificationMiddlewareǁprocess__mutmut_55': xǁClarificationMiddlewareǁprocess__mutmut_55, 
        'xǁClarificationMiddlewareǁprocess__mutmut_56': xǁClarificationMiddlewareǁprocess__mutmut_56, 
        'xǁClarificationMiddlewareǁprocess__mutmut_57': xǁClarificationMiddlewareǁprocess__mutmut_57, 
        'xǁClarificationMiddlewareǁprocess__mutmut_58': xǁClarificationMiddlewareǁprocess__mutmut_58, 
        'xǁClarificationMiddlewareǁprocess__mutmut_59': xǁClarificationMiddlewareǁprocess__mutmut_59, 
        'xǁClarificationMiddlewareǁprocess__mutmut_60': xǁClarificationMiddlewareǁprocess__mutmut_60, 
        'xǁClarificationMiddlewareǁprocess__mutmut_61': xǁClarificationMiddlewareǁprocess__mutmut_61, 
        'xǁClarificationMiddlewareǁprocess__mutmut_62': xǁClarificationMiddlewareǁprocess__mutmut_62, 
        'xǁClarificationMiddlewareǁprocess__mutmut_63': xǁClarificationMiddlewareǁprocess__mutmut_63, 
        'xǁClarificationMiddlewareǁprocess__mutmut_64': xǁClarificationMiddlewareǁprocess__mutmut_64, 
        'xǁClarificationMiddlewareǁprocess__mutmut_65': xǁClarificationMiddlewareǁprocess__mutmut_65, 
        'xǁClarificationMiddlewareǁprocess__mutmut_66': xǁClarificationMiddlewareǁprocess__mutmut_66, 
        'xǁClarificationMiddlewareǁprocess__mutmut_67': xǁClarificationMiddlewareǁprocess__mutmut_67, 
        'xǁClarificationMiddlewareǁprocess__mutmut_68': xǁClarificationMiddlewareǁprocess__mutmut_68, 
        'xǁClarificationMiddlewareǁprocess__mutmut_69': xǁClarificationMiddlewareǁprocess__mutmut_69, 
        'xǁClarificationMiddlewareǁprocess__mutmut_70': xǁClarificationMiddlewareǁprocess__mutmut_70, 
        'xǁClarificationMiddlewareǁprocess__mutmut_71': xǁClarificationMiddlewareǁprocess__mutmut_71, 
        'xǁClarificationMiddlewareǁprocess__mutmut_72': xǁClarificationMiddlewareǁprocess__mutmut_72, 
        'xǁClarificationMiddlewareǁprocess__mutmut_73': xǁClarificationMiddlewareǁprocess__mutmut_73, 
        'xǁClarificationMiddlewareǁprocess__mutmut_74': xǁClarificationMiddlewareǁprocess__mutmut_74, 
        'xǁClarificationMiddlewareǁprocess__mutmut_75': xǁClarificationMiddlewareǁprocess__mutmut_75, 
        'xǁClarificationMiddlewareǁprocess__mutmut_76': xǁClarificationMiddlewareǁprocess__mutmut_76, 
        'xǁClarificationMiddlewareǁprocess__mutmut_77': xǁClarificationMiddlewareǁprocess__mutmut_77, 
        'xǁClarificationMiddlewareǁprocess__mutmut_78': xǁClarificationMiddlewareǁprocess__mutmut_78, 
        'xǁClarificationMiddlewareǁprocess__mutmut_79': xǁClarificationMiddlewareǁprocess__mutmut_79, 
        'xǁClarificationMiddlewareǁprocess__mutmut_80': xǁClarificationMiddlewareǁprocess__mutmut_80, 
        'xǁClarificationMiddlewareǁprocess__mutmut_81': xǁClarificationMiddlewareǁprocess__mutmut_81, 
        'xǁClarificationMiddlewareǁprocess__mutmut_82': xǁClarificationMiddlewareǁprocess__mutmut_82, 
        'xǁClarificationMiddlewareǁprocess__mutmut_83': xǁClarificationMiddlewareǁprocess__mutmut_83, 
        'xǁClarificationMiddlewareǁprocess__mutmut_84': xǁClarificationMiddlewareǁprocess__mutmut_84, 
        'xǁClarificationMiddlewareǁprocess__mutmut_85': xǁClarificationMiddlewareǁprocess__mutmut_85, 
        'xǁClarificationMiddlewareǁprocess__mutmut_86': xǁClarificationMiddlewareǁprocess__mutmut_86, 
        'xǁClarificationMiddlewareǁprocess__mutmut_87': xǁClarificationMiddlewareǁprocess__mutmut_87, 
        'xǁClarificationMiddlewareǁprocess__mutmut_88': xǁClarificationMiddlewareǁprocess__mutmut_88, 
        'xǁClarificationMiddlewareǁprocess__mutmut_89': xǁClarificationMiddlewareǁprocess__mutmut_89, 
        'xǁClarificationMiddlewareǁprocess__mutmut_90': xǁClarificationMiddlewareǁprocess__mutmut_90, 
        'xǁClarificationMiddlewareǁprocess__mutmut_91': xǁClarificationMiddlewareǁprocess__mutmut_91, 
        'xǁClarificationMiddlewareǁprocess__mutmut_92': xǁClarificationMiddlewareǁprocess__mutmut_92, 
        'xǁClarificationMiddlewareǁprocess__mutmut_93': xǁClarificationMiddlewareǁprocess__mutmut_93, 
        'xǁClarificationMiddlewareǁprocess__mutmut_94': xǁClarificationMiddlewareǁprocess__mutmut_94, 
        'xǁClarificationMiddlewareǁprocess__mutmut_95': xǁClarificationMiddlewareǁprocess__mutmut_95
    }
    xǁClarificationMiddlewareǁprocess__mutmut_orig.__name__ = 'xǁClarificationMiddlewareǁprocess'

    def _emit_requested(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        args = [conflict, conflict_id, context]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁClarificationMiddlewareǁ_emit_requested__mutmut_orig'), object.__getattribute__(self, 'xǁClarificationMiddlewareǁ_emit_requested__mutmut_mutants'), args, kwargs, self)

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_orig(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationRequested for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_1(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=None,
                context=context,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationRequested for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_2(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=None,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationRequested for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_3(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                conflict_id=None,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationRequested for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_4(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                conflict_id=conflict_id,
                repo_root=None,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationRequested for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_5(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                context=context,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationRequested for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_6(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationRequested for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_7(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationRequested for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_8(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                conflict_id=conflict_id,
                )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationRequested for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_9(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                None,
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_10(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationRequested for %s: %s",
                None,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_11(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationRequested for %s: %s",
                conflict.term.surface_text,
                None,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_12(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_13(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationRequested for %s: %s",
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_14(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationRequested for %s: %s",
                conflict.term.surface_text,
                )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_15(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "XXFailed to emit ClarificationRequested for %s: %sXX",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_16(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "failed to emit clarificationrequested for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_emit_requested__mutmut_17(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Emit GlossaryClarificationRequested for a deferred conflict.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID tracking ID
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_requested

        try:
            emit_clarification_requested(
                conflict=conflict,
                context=context,
                conflict_id=conflict_id,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "FAILED TO EMIT CLARIFICATIONREQUESTED FOR %S: %S",
                conflict.term.surface_text,
                exc,
            )
    
    xǁClarificationMiddlewareǁ_emit_requested__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁClarificationMiddlewareǁ_emit_requested__mutmut_1': xǁClarificationMiddlewareǁ_emit_requested__mutmut_1, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_2': xǁClarificationMiddlewareǁ_emit_requested__mutmut_2, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_3': xǁClarificationMiddlewareǁ_emit_requested__mutmut_3, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_4': xǁClarificationMiddlewareǁ_emit_requested__mutmut_4, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_5': xǁClarificationMiddlewareǁ_emit_requested__mutmut_5, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_6': xǁClarificationMiddlewareǁ_emit_requested__mutmut_6, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_7': xǁClarificationMiddlewareǁ_emit_requested__mutmut_7, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_8': xǁClarificationMiddlewareǁ_emit_requested__mutmut_8, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_9': xǁClarificationMiddlewareǁ_emit_requested__mutmut_9, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_10': xǁClarificationMiddlewareǁ_emit_requested__mutmut_10, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_11': xǁClarificationMiddlewareǁ_emit_requested__mutmut_11, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_12': xǁClarificationMiddlewareǁ_emit_requested__mutmut_12, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_13': xǁClarificationMiddlewareǁ_emit_requested__mutmut_13, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_14': xǁClarificationMiddlewareǁ_emit_requested__mutmut_14, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_15': xǁClarificationMiddlewareǁ_emit_requested__mutmut_15, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_16': xǁClarificationMiddlewareǁ_emit_requested__mutmut_16, 
        'xǁClarificationMiddlewareǁ_emit_requested__mutmut_17': xǁClarificationMiddlewareǁ_emit_requested__mutmut_17
    }
    xǁClarificationMiddlewareǁ_emit_requested__mutmut_orig.__name__ = 'xǁClarificationMiddlewareǁ_emit_requested'

    def _emit_deferred(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        args = [conflict, conflict_id, context]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁClarificationMiddlewareǁ_emit_deferred__mutmut_orig'), object.__getattribute__(self, 'xǁClarificationMiddlewareǁ_emit_deferred__mutmut_mutants'), args, kwargs, self)

    def xǁClarificationMiddlewareǁ_emit_deferred__mutmut_orig(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Backward-compat alias for deferred request emission."""
        self._emit_requested(conflict, conflict_id, context)

    def xǁClarificationMiddlewareǁ_emit_deferred__mutmut_1(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Backward-compat alias for deferred request emission."""
        self._emit_requested(None, conflict_id, context)

    def xǁClarificationMiddlewareǁ_emit_deferred__mutmut_2(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Backward-compat alias for deferred request emission."""
        self._emit_requested(conflict, None, context)

    def xǁClarificationMiddlewareǁ_emit_deferred__mutmut_3(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Backward-compat alias for deferred request emission."""
        self._emit_requested(conflict, conflict_id, None)

    def xǁClarificationMiddlewareǁ_emit_deferred__mutmut_4(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Backward-compat alias for deferred request emission."""
        self._emit_requested(conflict_id, context)

    def xǁClarificationMiddlewareǁ_emit_deferred__mutmut_5(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Backward-compat alias for deferred request emission."""
        self._emit_requested(conflict, context)

    def xǁClarificationMiddlewareǁ_emit_deferred__mutmut_6(
        self,
        conflict: Any,
        conflict_id: str,
        context: Any,
    ) -> None:
        """Backward-compat alias for deferred request emission."""
        self._emit_requested(conflict, conflict_id, )
    
    xǁClarificationMiddlewareǁ_emit_deferred__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁClarificationMiddlewareǁ_emit_deferred__mutmut_1': xǁClarificationMiddlewareǁ_emit_deferred__mutmut_1, 
        'xǁClarificationMiddlewareǁ_emit_deferred__mutmut_2': xǁClarificationMiddlewareǁ_emit_deferred__mutmut_2, 
        'xǁClarificationMiddlewareǁ_emit_deferred__mutmut_3': xǁClarificationMiddlewareǁ_emit_deferred__mutmut_3, 
        'xǁClarificationMiddlewareǁ_emit_deferred__mutmut_4': xǁClarificationMiddlewareǁ_emit_deferred__mutmut_4, 
        'xǁClarificationMiddlewareǁ_emit_deferred__mutmut_5': xǁClarificationMiddlewareǁ_emit_deferred__mutmut_5, 
        'xǁClarificationMiddlewareǁ_emit_deferred__mutmut_6': xǁClarificationMiddlewareǁ_emit_deferred__mutmut_6
    }
    xǁClarificationMiddlewareǁ_emit_deferred__mutmut_orig.__name__ = 'xǁClarificationMiddlewareǁ_emit_deferred'

    def _handle_candidate_selection(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        args = [conflict, conflict_id, selected_sense, context]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_orig'), object.__getattribute__(self, 'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_mutants'), args, kwargs, self)

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_orig(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_1(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=None,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_2(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=None,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_3(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=None,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_4(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=None,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_5(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode=None,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_6(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=None,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_7(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_8(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_9(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_10(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_11(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_12(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_13(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="XXinteractiveXX",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_14(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="INTERACTIVE",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_15(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                None,
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_16(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                None,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_17(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                None,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_18(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_19(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_20(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "Failed to emit ClarificationResolved for %s: %s",
                conflict.term.surface_text,
                )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_21(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "XXFailed to emit ClarificationResolved for %s: %sXX",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_22(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "failed to emit clarificationresolved for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_23(
        self,
        conflict: Any,
        conflict_id: str,
        selected_sense: Any,
        context: Any,
    ) -> None:
        """Handle user selecting a candidate sense.

        Emits GlossaryClarificationResolved event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            selected_sense: SenseRef that was selected
            context: PrimitiveExecutionContext
        """
        from .events import emit_clarification_resolved

        try:
            emit_clarification_resolved(
                conflict_id=conflict_id,
                conflict=conflict,
                selected_sense=selected_sense,
                context=context,
                resolution_mode="interactive",
                repo_root=self.repo_root,
            )
        except Exception as exc:
            logger.error(
                "FAILED TO EMIT CLARIFICATIONRESOLVED FOR %S: %S",
                conflict.term.surface_text,
                exc,
            )
    
    xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_1': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_1, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_2': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_2, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_3': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_3, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_4': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_4, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_5': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_5, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_6': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_6, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_7': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_7, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_8': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_8, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_9': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_9, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_10': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_10, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_11': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_11, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_12': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_12, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_13': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_13, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_14': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_14, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_15': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_15, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_16': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_16, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_17': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_17, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_18': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_18, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_19': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_19, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_20': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_20, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_21': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_21, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_22': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_22, 
        'xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_23': xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_23
    }
    xǁClarificationMiddlewareǁ_handle_candidate_selection__mutmut_orig.__name__ = 'xǁClarificationMiddlewareǁ_handle_candidate_selection'

    def _handle_custom_sense(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        args = [conflict, conflict_id, custom_definition, context]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_orig'), object.__getattribute__(self, 'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_mutants'), args, kwargs, self)

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_orig(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_1(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=None,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_2(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=None,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_3(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value=None,
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_4(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=None,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_5(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type=None,
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_6(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=None,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_7(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_8(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_9(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_10(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_11(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_12(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_13(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="XXteam_domainXX",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_14(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="TEAM_DOMAIN",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_15(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="XXcreateXX",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_16(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="CREATE",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_17(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_18(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = None
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_19(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(None, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_20(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, None, "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_21(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", None)
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_22(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr("actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_23(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_24(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", )
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_25(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "XXactor_idXX", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_26(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "ACTOR_ID", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_27(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "XXunknownXX")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_28(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "UNKNOWN")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_29(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = None
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_30(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=None,
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_31(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=None,
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_32(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source=None,
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_33(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_34(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_35(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_36(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(None),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_37(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(None),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_38(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="XXuser_clarificationXX",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_39(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="USER_CLARIFICATION",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_40(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = None
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_41(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=None,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_42(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope=None,
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_43(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=None,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_44(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=None,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_45(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=None,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_46(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=None,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_47(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_48(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_49(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_50(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_51(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_52(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_53(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="XXteam_domainXX",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_54(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="TEAM_DOMAIN",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_55(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=2.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_56(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(None)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_57(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                None,
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_58(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                None,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_59(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                None,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_60(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_61(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_62(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "Failed to emit SenseUpdated for %s: %s",
                conflict.term.surface_text,
                )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_63(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "XXFailed to emit SenseUpdated for %s: %sXX",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_64(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "failed to emit senseupdated for %s: %s",
                conflict.term.surface_text,
                exc,
            )

    def xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_65(
        self,
        conflict: Any,
        conflict_id: str,
        custom_definition: str,
        context: Any,
    ) -> None:
        """Handle user providing a custom sense definition.

        Emits GlossarySenseUpdated event.

        Args:
            conflict: SemanticConflict instance
            conflict_id: UUID from the requesting event
            custom_definition: Custom definition text from user
            context: PrimitiveExecutionContext
        """
        from .events import emit_sense_updated
        from .models import Provenance, SenseStatus, TermSense

        try:
            emit_sense_updated(
                conflict=conflict,
                custom_definition=custom_definition,
                scope_value="team_domain",
                context=context,
                update_type="create",
                repo_root=self.repo_root,
            )
            if self.glossary_store is not None:
                actor_id = getattr(context, "actor_id", "unknown")
                provenance = Provenance(
                    actor_id=str(actor_id),
                    timestamp=datetime.now(timezone.utc),
                    source="user_clarification",
                )
                term_sense = TermSense(
                    surface=conflict.term,
                    scope="team_domain",
                    definition=custom_definition,
                    provenance=provenance,
                    confidence=1.0,
                    status=SenseStatus.ACTIVE,
                )
                self.glossary_store.add_sense(term_sense)
        except Exception as exc:
            logger.error(
                "FAILED TO EMIT SENSEUPDATED FOR %S: %S",
                conflict.term.surface_text,
                exc,
            )
    
    xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_1': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_1, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_2': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_2, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_3': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_3, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_4': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_4, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_5': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_5, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_6': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_6, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_7': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_7, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_8': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_8, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_9': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_9, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_10': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_10, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_11': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_11, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_12': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_12, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_13': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_13, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_14': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_14, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_15': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_15, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_16': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_16, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_17': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_17, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_18': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_18, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_19': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_19, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_20': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_20, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_21': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_21, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_22': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_22, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_23': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_23, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_24': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_24, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_25': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_25, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_26': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_26, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_27': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_27, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_28': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_28, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_29': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_29, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_30': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_30, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_31': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_31, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_32': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_32, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_33': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_33, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_34': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_34, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_35': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_35, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_36': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_36, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_37': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_37, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_38': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_38, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_39': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_39, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_40': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_40, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_41': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_41, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_42': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_42, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_43': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_43, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_44': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_44, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_45': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_45, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_46': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_46, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_47': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_47, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_48': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_48, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_49': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_49, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_50': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_50, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_51': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_51, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_52': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_52, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_53': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_53, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_54': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_54, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_55': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_55, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_56': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_56, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_57': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_57, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_58': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_58, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_59': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_59, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_60': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_60, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_61': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_61, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_62': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_62, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_63': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_63, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_64': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_64, 
        'xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_65': xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_65
    }
    xǁClarificationMiddlewareǁ_handle_custom_sense__mutmut_orig.__name__ = 'xǁClarificationMiddlewareǁ_handle_custom_sense'
