"""Glossary middleware pipeline orchestrator (WP09).

This module implements the GlossaryMiddlewarePipeline that composes all
middleware components into a sequential execution chain:

    Layer 1: GlossaryCandidateExtractionMiddleware (term extraction)
    Layer 2: SemanticCheckMiddleware (conflict detection)
    Layer 3: ClarificationMiddleware (interactive conflict resolution)
    Layer 4: GenerationGateMiddleware (generation blocking)
    Layer 5: ResumeMiddleware (checkpoint/resume)

Clarification runs BEFORE the generation gate so that users get a chance
to resolve conflicts interactively. Only truly unresolved conflicts reach
the gate. Without this ordering the gate would raise BlockedByConflict
immediately and the clarification layer would never execute.

The pipeline executes middleware in order, passing the context object
through each layer. Expected exceptions (BlockedByConflict, DeferredToAsync,
AbortResume) propagate to the caller. Unexpected exceptions are wrapped
in RuntimeError with the offending middleware's class name for debugging.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, List, Protocol

from specify_cli.glossary.exceptions import (
    AbortResume,
    BlockedByConflict,
    DeferredToAsync,
)
from specify_cli.glossary.strictness import Strictness

if TYPE_CHECKING:
    from specify_cli.glossary.store import GlossaryStore

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


def prompt_conflict_resolution_safe(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    args = [conflict, candidates]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_prompt_conflict_resolution_safe__mutmut_orig, x_prompt_conflict_resolution_safe__mutmut_mutants, args, kwargs, None)


def x_prompt_conflict_resolution_safe__mutmut_orig(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_1(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = None
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_2(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(None)
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_3(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print(None)
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_4(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("XXCandidate senses:XX")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_5(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_6(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("CANDIDATE SENSES:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_7(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(None):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_8(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(None)
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_9(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx - 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_10(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 2}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_11(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print(None)
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_12(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("XX  [c] Provide a custom definitionXX")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_13(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_14(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [C] PROVIDE A CUSTOM DEFINITION")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_15(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print(None)

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_16(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("XX  [d] Defer resolutionXX")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_17(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_18(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [D] DEFER RESOLUTION")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_19(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = None

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_20(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().upper()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_21(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input(None).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_22(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(None)).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_23(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("XXSelect [1-{}/c/d]: XX".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_24(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_25(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("SELECT [1-{}/C/D]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_26(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" and choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_27(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice != "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_28(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "XXdXX" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_29(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "D" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_30(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice != "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_31(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "XXXX":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_32(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("XXdeferXX", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_33(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("DEFER", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_34(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice != "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_35(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "XXcXX":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_36(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "C":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_37(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = None
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_38(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input(None).strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_39(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("XXEnter custom definition: XX").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_40(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_41(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("ENTER CUSTOM DEFINITION: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_42(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("XXcustomXX", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_43(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("CUSTOM", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_44(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("XXdeferXX", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_45(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("DEFER", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_46(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = None
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_47(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) + 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_48(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(None) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_49(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 2
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_50(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 1 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_51(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 < idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_52(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx <= len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_53(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = None
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_54(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("XXselectXX", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_55(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("SELECT", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_56(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("XXdeferXX", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_57(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("DEFER", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("defer", None)


def x_prompt_conflict_resolution_safe__mutmut_58(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("XXdeferXX", None)


def x_prompt_conflict_resolution_safe__mutmut_59(
    conflict: Any,
    candidates: list[Any],
) -> tuple[str, str | None]:
    """Prompt the user to resolve a semantic conflict interactively.

    Presents candidate senses for the conflicting term and asks the user
    to select one or provide a custom definition. Wraps all I/O errors
    so the caller never gets an unhandled exception from stdin/stdout.

    Args:
        conflict: SemanticConflict instance with ``term.surface_text``.
        candidates: List of SenseRef candidate senses.

    Returns:
        Tuple of (choice, custom_definition):
        - ("select", None) when user picks a numbered candidate
          (sets ``conflict.selected_index`` to the chosen 0-based index).
        - ("custom", "definition text") when user types a custom sense.
        - ("defer", None) on invalid input or I/O failure.
    """
    try:
        term_name = conflict.term.surface_text
        print(f"\nConflict: term '{term_name}' is ambiguous.")
        print("Candidate senses:")
        for idx, sense in enumerate(candidates):
            print(f"  [{idx + 1}] {sense.definition} (scope={sense.scope}, confidence={sense.confidence})")
        print("  [c] Provide a custom definition")
        print("  [d] Defer resolution")

        choice = input("Select [1-{}/c/d]: ".format(len(candidates))).strip().lower()

        if choice == "d" or choice == "":
            return ("defer", None)

        if choice == "c":
            custom_def = input("Enter custom definition: ").strip()
            if custom_def:
                return ("custom", custom_def)
            return ("defer", None)

        # Try to parse as a number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                conflict.selected_index = idx
                return ("select", None)
        except ValueError:
            pass

        # Invalid input -> defer
        return ("defer", None)

    except (EOFError, KeyboardInterrupt, OSError):
        # Non-interactive environment or user interrupt
        return ("DEFER", None)

x_prompt_conflict_resolution_safe__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_prompt_conflict_resolution_safe__mutmut_1': x_prompt_conflict_resolution_safe__mutmut_1, 
    'x_prompt_conflict_resolution_safe__mutmut_2': x_prompt_conflict_resolution_safe__mutmut_2, 
    'x_prompt_conflict_resolution_safe__mutmut_3': x_prompt_conflict_resolution_safe__mutmut_3, 
    'x_prompt_conflict_resolution_safe__mutmut_4': x_prompt_conflict_resolution_safe__mutmut_4, 
    'x_prompt_conflict_resolution_safe__mutmut_5': x_prompt_conflict_resolution_safe__mutmut_5, 
    'x_prompt_conflict_resolution_safe__mutmut_6': x_prompt_conflict_resolution_safe__mutmut_6, 
    'x_prompt_conflict_resolution_safe__mutmut_7': x_prompt_conflict_resolution_safe__mutmut_7, 
    'x_prompt_conflict_resolution_safe__mutmut_8': x_prompt_conflict_resolution_safe__mutmut_8, 
    'x_prompt_conflict_resolution_safe__mutmut_9': x_prompt_conflict_resolution_safe__mutmut_9, 
    'x_prompt_conflict_resolution_safe__mutmut_10': x_prompt_conflict_resolution_safe__mutmut_10, 
    'x_prompt_conflict_resolution_safe__mutmut_11': x_prompt_conflict_resolution_safe__mutmut_11, 
    'x_prompt_conflict_resolution_safe__mutmut_12': x_prompt_conflict_resolution_safe__mutmut_12, 
    'x_prompt_conflict_resolution_safe__mutmut_13': x_prompt_conflict_resolution_safe__mutmut_13, 
    'x_prompt_conflict_resolution_safe__mutmut_14': x_prompt_conflict_resolution_safe__mutmut_14, 
    'x_prompt_conflict_resolution_safe__mutmut_15': x_prompt_conflict_resolution_safe__mutmut_15, 
    'x_prompt_conflict_resolution_safe__mutmut_16': x_prompt_conflict_resolution_safe__mutmut_16, 
    'x_prompt_conflict_resolution_safe__mutmut_17': x_prompt_conflict_resolution_safe__mutmut_17, 
    'x_prompt_conflict_resolution_safe__mutmut_18': x_prompt_conflict_resolution_safe__mutmut_18, 
    'x_prompt_conflict_resolution_safe__mutmut_19': x_prompt_conflict_resolution_safe__mutmut_19, 
    'x_prompt_conflict_resolution_safe__mutmut_20': x_prompt_conflict_resolution_safe__mutmut_20, 
    'x_prompt_conflict_resolution_safe__mutmut_21': x_prompt_conflict_resolution_safe__mutmut_21, 
    'x_prompt_conflict_resolution_safe__mutmut_22': x_prompt_conflict_resolution_safe__mutmut_22, 
    'x_prompt_conflict_resolution_safe__mutmut_23': x_prompt_conflict_resolution_safe__mutmut_23, 
    'x_prompt_conflict_resolution_safe__mutmut_24': x_prompt_conflict_resolution_safe__mutmut_24, 
    'x_prompt_conflict_resolution_safe__mutmut_25': x_prompt_conflict_resolution_safe__mutmut_25, 
    'x_prompt_conflict_resolution_safe__mutmut_26': x_prompt_conflict_resolution_safe__mutmut_26, 
    'x_prompt_conflict_resolution_safe__mutmut_27': x_prompt_conflict_resolution_safe__mutmut_27, 
    'x_prompt_conflict_resolution_safe__mutmut_28': x_prompt_conflict_resolution_safe__mutmut_28, 
    'x_prompt_conflict_resolution_safe__mutmut_29': x_prompt_conflict_resolution_safe__mutmut_29, 
    'x_prompt_conflict_resolution_safe__mutmut_30': x_prompt_conflict_resolution_safe__mutmut_30, 
    'x_prompt_conflict_resolution_safe__mutmut_31': x_prompt_conflict_resolution_safe__mutmut_31, 
    'x_prompt_conflict_resolution_safe__mutmut_32': x_prompt_conflict_resolution_safe__mutmut_32, 
    'x_prompt_conflict_resolution_safe__mutmut_33': x_prompt_conflict_resolution_safe__mutmut_33, 
    'x_prompt_conflict_resolution_safe__mutmut_34': x_prompt_conflict_resolution_safe__mutmut_34, 
    'x_prompt_conflict_resolution_safe__mutmut_35': x_prompt_conflict_resolution_safe__mutmut_35, 
    'x_prompt_conflict_resolution_safe__mutmut_36': x_prompt_conflict_resolution_safe__mutmut_36, 
    'x_prompt_conflict_resolution_safe__mutmut_37': x_prompt_conflict_resolution_safe__mutmut_37, 
    'x_prompt_conflict_resolution_safe__mutmut_38': x_prompt_conflict_resolution_safe__mutmut_38, 
    'x_prompt_conflict_resolution_safe__mutmut_39': x_prompt_conflict_resolution_safe__mutmut_39, 
    'x_prompt_conflict_resolution_safe__mutmut_40': x_prompt_conflict_resolution_safe__mutmut_40, 
    'x_prompt_conflict_resolution_safe__mutmut_41': x_prompt_conflict_resolution_safe__mutmut_41, 
    'x_prompt_conflict_resolution_safe__mutmut_42': x_prompt_conflict_resolution_safe__mutmut_42, 
    'x_prompt_conflict_resolution_safe__mutmut_43': x_prompt_conflict_resolution_safe__mutmut_43, 
    'x_prompt_conflict_resolution_safe__mutmut_44': x_prompt_conflict_resolution_safe__mutmut_44, 
    'x_prompt_conflict_resolution_safe__mutmut_45': x_prompt_conflict_resolution_safe__mutmut_45, 
    'x_prompt_conflict_resolution_safe__mutmut_46': x_prompt_conflict_resolution_safe__mutmut_46, 
    'x_prompt_conflict_resolution_safe__mutmut_47': x_prompt_conflict_resolution_safe__mutmut_47, 
    'x_prompt_conflict_resolution_safe__mutmut_48': x_prompt_conflict_resolution_safe__mutmut_48, 
    'x_prompt_conflict_resolution_safe__mutmut_49': x_prompt_conflict_resolution_safe__mutmut_49, 
    'x_prompt_conflict_resolution_safe__mutmut_50': x_prompt_conflict_resolution_safe__mutmut_50, 
    'x_prompt_conflict_resolution_safe__mutmut_51': x_prompt_conflict_resolution_safe__mutmut_51, 
    'x_prompt_conflict_resolution_safe__mutmut_52': x_prompt_conflict_resolution_safe__mutmut_52, 
    'x_prompt_conflict_resolution_safe__mutmut_53': x_prompt_conflict_resolution_safe__mutmut_53, 
    'x_prompt_conflict_resolution_safe__mutmut_54': x_prompt_conflict_resolution_safe__mutmut_54, 
    'x_prompt_conflict_resolution_safe__mutmut_55': x_prompt_conflict_resolution_safe__mutmut_55, 
    'x_prompt_conflict_resolution_safe__mutmut_56': x_prompt_conflict_resolution_safe__mutmut_56, 
    'x_prompt_conflict_resolution_safe__mutmut_57': x_prompt_conflict_resolution_safe__mutmut_57, 
    'x_prompt_conflict_resolution_safe__mutmut_58': x_prompt_conflict_resolution_safe__mutmut_58, 
    'x_prompt_conflict_resolution_safe__mutmut_59': x_prompt_conflict_resolution_safe__mutmut_59
}
x_prompt_conflict_resolution_safe__mutmut_orig.__name__ = 'x_prompt_conflict_resolution_safe'


class GlossaryMiddleware(Protocol):
    """Protocol for glossary middleware components.

    Every middleware must implement a ``process`` method that accepts
    a context object and returns the (possibly modified) context.
    """

    def process(self, context: Any) -> Any:
        """Process the execution context.

        Args:
            context: Current execution context (PrimitiveExecutionContext)

        Returns:
            Modified context (may add extracted_terms, conflicts, etc.)

        Raises:
            BlockedByConflict: If generation must be blocked.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted by the user.
        """
        ...


class GlossaryMiddlewarePipeline:
    """Orchestrate glossary middleware components in a sequential pipeline.

    The pipeline:
    - Checks if glossary is enabled for the current step
    - Executes middleware in the order provided
    - Validates that each middleware returns a non-None context
    - Propagates expected exceptions (BlockedByConflict, DeferredToAsync, AbortResume)
    - Wraps unexpected exceptions in RuntimeError with middleware class name
    """

    def __init__(
        self,
        middleware: List[GlossaryMiddleware],
        skip_on_disabled: bool = True,
    ) -> None:
        args = [middleware, skip_on_disabled]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁGlossaryMiddlewarePipelineǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁGlossaryMiddlewarePipelineǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁGlossaryMiddlewarePipelineǁ__init____mutmut_orig(
        self,
        middleware: List[GlossaryMiddleware],
        skip_on_disabled: bool = True,
    ) -> None:
        """Initialize the pipeline.

        Args:
            middleware: Ordered list of middleware components.
            skip_on_disabled: When True, skip pipeline entirely if
                ``context.is_glossary_enabled()`` returns False.
        """
        self.middleware = list(middleware)
        self.skip_on_disabled = skip_on_disabled

    def xǁGlossaryMiddlewarePipelineǁ__init____mutmut_1(
        self,
        middleware: List[GlossaryMiddleware],
        skip_on_disabled: bool = False,
    ) -> None:
        """Initialize the pipeline.

        Args:
            middleware: Ordered list of middleware components.
            skip_on_disabled: When True, skip pipeline entirely if
                ``context.is_glossary_enabled()`` returns False.
        """
        self.middleware = list(middleware)
        self.skip_on_disabled = skip_on_disabled

    def xǁGlossaryMiddlewarePipelineǁ__init____mutmut_2(
        self,
        middleware: List[GlossaryMiddleware],
        skip_on_disabled: bool = True,
    ) -> None:
        """Initialize the pipeline.

        Args:
            middleware: Ordered list of middleware components.
            skip_on_disabled: When True, skip pipeline entirely if
                ``context.is_glossary_enabled()`` returns False.
        """
        self.middleware = None
        self.skip_on_disabled = skip_on_disabled

    def xǁGlossaryMiddlewarePipelineǁ__init____mutmut_3(
        self,
        middleware: List[GlossaryMiddleware],
        skip_on_disabled: bool = True,
    ) -> None:
        """Initialize the pipeline.

        Args:
            middleware: Ordered list of middleware components.
            skip_on_disabled: When True, skip pipeline entirely if
                ``context.is_glossary_enabled()`` returns False.
        """
        self.middleware = list(None)
        self.skip_on_disabled = skip_on_disabled

    def xǁGlossaryMiddlewarePipelineǁ__init____mutmut_4(
        self,
        middleware: List[GlossaryMiddleware],
        skip_on_disabled: bool = True,
    ) -> None:
        """Initialize the pipeline.

        Args:
            middleware: Ordered list of middleware components.
            skip_on_disabled: When True, skip pipeline entirely if
                ``context.is_glossary_enabled()`` returns False.
        """
        self.middleware = list(middleware)
        self.skip_on_disabled = None
    
    xǁGlossaryMiddlewarePipelineǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁGlossaryMiddlewarePipelineǁ__init____mutmut_1': xǁGlossaryMiddlewarePipelineǁ__init____mutmut_1, 
        'xǁGlossaryMiddlewarePipelineǁ__init____mutmut_2': xǁGlossaryMiddlewarePipelineǁ__init____mutmut_2, 
        'xǁGlossaryMiddlewarePipelineǁ__init____mutmut_3': xǁGlossaryMiddlewarePipelineǁ__init____mutmut_3, 
        'xǁGlossaryMiddlewarePipelineǁ__init____mutmut_4': xǁGlossaryMiddlewarePipelineǁ__init____mutmut_4
    }
    xǁGlossaryMiddlewarePipelineǁ__init____mutmut_orig.__name__ = 'xǁGlossaryMiddlewarePipelineǁ__init__'

    def process(self, context: Any) -> Any:
        args = [context]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_orig'), object.__getattribute__(self, 'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_mutants'), args, kwargs, self)

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_orig(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_1(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is not None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_2(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError(None)

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_3(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("XXPipeline context must not be NoneXX")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_4(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("pipeline context must not be none")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_5(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("PIPELINE CONTEXT MUST NOT BE NONE")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_6(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled or hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_7(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(None, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_8(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, None):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_9(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr("is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_10(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, ):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_11(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "XXis_glossary_enabledXX"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_12(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "IS_GLOSSARY_ENABLED"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_13(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_14(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = None
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_15(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = None
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_16(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(None)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_17(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    None
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_18(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is not None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_19(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    None
                )

            current_context = result

        return current_context

    def xǁGlossaryMiddlewarePipelineǁprocess__mutmut_20(self, context: Any) -> Any:
        """Execute the middleware pipeline.

        Args:
            context: Initial execution context. Must not be None.

        Returns:
            Final context after all middleware have executed.

        Raises:
            ValueError: If context is None.
            BlockedByConflict: If the generation gate blocks.
            DeferredToAsync: If clarification is deferred.
            AbortResume: If resume is aborted.
            RuntimeError: If a middleware raises an unexpected exception.
        """
        if context is None:
            raise ValueError("Pipeline context must not be None")

        # Check if glossary is enabled for this step
        if self.skip_on_disabled and hasattr(context, "is_glossary_enabled"):
            if not context.is_glossary_enabled():
                return context

        current_context = context
        for mw in self.middleware:
            try:
                result = mw.process(current_context)
            except (BlockedByConflict, DeferredToAsync, AbortResume):
                # Expected exceptions -- re-raise for the caller
                raise
            except Exception as e:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} failed: {e}"
                ) from e

            if result is None:
                raise RuntimeError(
                    f"Glossary middleware {mw.__class__.__name__} returned None "
                    f"instead of a context object"
                )

            current_context = None

        return current_context
    
    xǁGlossaryMiddlewarePipelineǁprocess__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_1': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_1, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_2': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_2, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_3': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_3, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_4': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_4, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_5': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_5, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_6': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_6, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_7': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_7, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_8': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_8, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_9': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_9, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_10': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_10, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_11': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_11, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_12': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_12, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_13': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_13, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_14': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_14, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_15': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_15, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_16': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_16, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_17': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_17, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_18': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_18, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_19': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_19, 
        'xǁGlossaryMiddlewarePipelineǁprocess__mutmut_20': xǁGlossaryMiddlewarePipelineǁprocess__mutmut_20
    }
    xǁGlossaryMiddlewarePipelineǁprocess__mutmut_orig.__name__ = 'xǁGlossaryMiddlewarePipelineǁprocess'


def create_standard_pipeline(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    args = [repo_root, runtime_strictness, interaction_mode]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_create_standard_pipeline__mutmut_orig, x_create_standard_pipeline__mutmut_mutants, args, kwargs, None)


def x_create_standard_pipeline__mutmut_orig(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_1(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "XXinteractiveXX",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_2(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "INTERACTIVE",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_3(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = None
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_4(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" * "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_5(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" * "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_6(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root * ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_7(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / "XX.kittifyXX" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_8(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".KITTIFY" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_9(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "XXeventsXX" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_10(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "EVENTS" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_11(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "XXglossaryXX"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_12(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "GLOSSARY"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_13(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_14(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=None, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_15(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=None)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_16(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_17(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, )

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_18(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=False, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_19(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=False)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_20(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = None

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_21(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=None)

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_22(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir * "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_23(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "XXdefault.events.jsonlXX")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_24(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "DEFAULT.EVENTS.JSONL")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_25(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(None, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_26(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, None)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_27(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_28(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, )

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_29(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode != "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_30(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "XXinteractiveXX":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_31(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "INTERACTIVE":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_32(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = None
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_33(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = ""  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_34(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = None

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_35(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=None),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_36(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=None,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_37(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=None,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_38(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_39(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_40(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=None,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_41(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=None,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_42(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=None,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_43(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_44(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_45(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_46(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=None,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_47(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=None,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_48(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_49(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_50(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=None),
    ]

    return GlossaryMiddlewarePipeline(middleware=middleware)


def x_create_standard_pipeline__mutmut_51(
    repo_root: Path,
    runtime_strictness: Strictness | None = None,
    interaction_mode: str = "interactive",
) -> GlossaryMiddlewarePipeline:
    """Create the standard 5-layer glossary middleware pipeline.

    Args:
        repo_root: Path to repository root (for config loading and event logs).
        runtime_strictness: CLI ``--strictness`` override (highest precedence).
        interaction_mode: ``"interactive"`` or ``"non-interactive"``.
            In non-interactive mode, the clarification middleware defers all
            conflicts instead of prompting.

    Returns:
        Configured pipeline instance with 5 middleware layers in order:
        extraction -> semantic check -> clarification -> generation gate -> resume.

    The clarification middleware runs BEFORE the generation gate so that
    users get a chance to resolve conflicts interactively before the gate
    decides whether to block. Only truly unresolved conflicts (those the
    user declined to fix or deferred) reach the gate.
    """
    from specify_cli.glossary.checkpoint import ScopeRef  # noqa: F401 (used by store)
    from specify_cli.glossary.clarification import ClarificationMiddleware
    from specify_cli.glossary.middleware import (
        GlossaryCandidateExtractionMiddleware,
        GenerationGateMiddleware,
        ResumeMiddleware,
        SemanticCheckMiddleware,
    )
    from specify_cli.glossary.store import GlossaryStore

    # Create glossary store (in-memory, backed by event log)
    events_dir = repo_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        events_dir.mkdir(parents=True, exist_ok=True)

    # Use a default event log path -- the store doesn't need a real file
    # to function; it just needs to be initialized.
    store = GlossaryStore(event_log_path=events_dir / "default.events.jsonl")

    # Load seed files into store
    _load_seed_files_into_store(repo_root, store)

    # Determine prompt function for clarification
    if interaction_mode == "interactive":
        prompt_fn = prompt_conflict_resolution_safe
    else:
        prompt_fn = None  # Non-interactive: defer all conflicts

    # Build middleware layers in order.
    #
    # IMPORTANT: Clarification runs BEFORE the generation gate (layers 3/4).
    # This ensures users can resolve conflicts interactively before the
    # gate decides whether to block. Without this ordering, the gate would
    # raise BlockedByConflict immediately and clarification would never run.
    middleware: List[GlossaryMiddleware] = [
        # Layer 1: Extract term candidates from step inputs
        GlossaryCandidateExtractionMiddleware(repo_root=repo_root),
        # Layer 2: Resolve terms and detect conflicts
        SemanticCheckMiddleware(
            glossary_store=store,
            repo_root=repo_root,
        ),
        # Layer 3: Interactive conflict clarification (runs BEFORE gate)
        ClarificationMiddleware(
            repo_root=repo_root,
            prompt_fn=prompt_fn,
            glossary_store=store,
        ),
        # Layer 4: Block generation on unresolved conflicts (after clarification)
        GenerationGateMiddleware(
            repo_root=repo_root,
            runtime_override=runtime_strictness,
        ),
        # Layer 5: Checkpoint/resume
        ResumeMiddleware(project_root=repo_root),
    ]

    return GlossaryMiddlewarePipeline(middleware=None)

x_create_standard_pipeline__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_create_standard_pipeline__mutmut_1': x_create_standard_pipeline__mutmut_1, 
    'x_create_standard_pipeline__mutmut_2': x_create_standard_pipeline__mutmut_2, 
    'x_create_standard_pipeline__mutmut_3': x_create_standard_pipeline__mutmut_3, 
    'x_create_standard_pipeline__mutmut_4': x_create_standard_pipeline__mutmut_4, 
    'x_create_standard_pipeline__mutmut_5': x_create_standard_pipeline__mutmut_5, 
    'x_create_standard_pipeline__mutmut_6': x_create_standard_pipeline__mutmut_6, 
    'x_create_standard_pipeline__mutmut_7': x_create_standard_pipeline__mutmut_7, 
    'x_create_standard_pipeline__mutmut_8': x_create_standard_pipeline__mutmut_8, 
    'x_create_standard_pipeline__mutmut_9': x_create_standard_pipeline__mutmut_9, 
    'x_create_standard_pipeline__mutmut_10': x_create_standard_pipeline__mutmut_10, 
    'x_create_standard_pipeline__mutmut_11': x_create_standard_pipeline__mutmut_11, 
    'x_create_standard_pipeline__mutmut_12': x_create_standard_pipeline__mutmut_12, 
    'x_create_standard_pipeline__mutmut_13': x_create_standard_pipeline__mutmut_13, 
    'x_create_standard_pipeline__mutmut_14': x_create_standard_pipeline__mutmut_14, 
    'x_create_standard_pipeline__mutmut_15': x_create_standard_pipeline__mutmut_15, 
    'x_create_standard_pipeline__mutmut_16': x_create_standard_pipeline__mutmut_16, 
    'x_create_standard_pipeline__mutmut_17': x_create_standard_pipeline__mutmut_17, 
    'x_create_standard_pipeline__mutmut_18': x_create_standard_pipeline__mutmut_18, 
    'x_create_standard_pipeline__mutmut_19': x_create_standard_pipeline__mutmut_19, 
    'x_create_standard_pipeline__mutmut_20': x_create_standard_pipeline__mutmut_20, 
    'x_create_standard_pipeline__mutmut_21': x_create_standard_pipeline__mutmut_21, 
    'x_create_standard_pipeline__mutmut_22': x_create_standard_pipeline__mutmut_22, 
    'x_create_standard_pipeline__mutmut_23': x_create_standard_pipeline__mutmut_23, 
    'x_create_standard_pipeline__mutmut_24': x_create_standard_pipeline__mutmut_24, 
    'x_create_standard_pipeline__mutmut_25': x_create_standard_pipeline__mutmut_25, 
    'x_create_standard_pipeline__mutmut_26': x_create_standard_pipeline__mutmut_26, 
    'x_create_standard_pipeline__mutmut_27': x_create_standard_pipeline__mutmut_27, 
    'x_create_standard_pipeline__mutmut_28': x_create_standard_pipeline__mutmut_28, 
    'x_create_standard_pipeline__mutmut_29': x_create_standard_pipeline__mutmut_29, 
    'x_create_standard_pipeline__mutmut_30': x_create_standard_pipeline__mutmut_30, 
    'x_create_standard_pipeline__mutmut_31': x_create_standard_pipeline__mutmut_31, 
    'x_create_standard_pipeline__mutmut_32': x_create_standard_pipeline__mutmut_32, 
    'x_create_standard_pipeline__mutmut_33': x_create_standard_pipeline__mutmut_33, 
    'x_create_standard_pipeline__mutmut_34': x_create_standard_pipeline__mutmut_34, 
    'x_create_standard_pipeline__mutmut_35': x_create_standard_pipeline__mutmut_35, 
    'x_create_standard_pipeline__mutmut_36': x_create_standard_pipeline__mutmut_36, 
    'x_create_standard_pipeline__mutmut_37': x_create_standard_pipeline__mutmut_37, 
    'x_create_standard_pipeline__mutmut_38': x_create_standard_pipeline__mutmut_38, 
    'x_create_standard_pipeline__mutmut_39': x_create_standard_pipeline__mutmut_39, 
    'x_create_standard_pipeline__mutmut_40': x_create_standard_pipeline__mutmut_40, 
    'x_create_standard_pipeline__mutmut_41': x_create_standard_pipeline__mutmut_41, 
    'x_create_standard_pipeline__mutmut_42': x_create_standard_pipeline__mutmut_42, 
    'x_create_standard_pipeline__mutmut_43': x_create_standard_pipeline__mutmut_43, 
    'x_create_standard_pipeline__mutmut_44': x_create_standard_pipeline__mutmut_44, 
    'x_create_standard_pipeline__mutmut_45': x_create_standard_pipeline__mutmut_45, 
    'x_create_standard_pipeline__mutmut_46': x_create_standard_pipeline__mutmut_46, 
    'x_create_standard_pipeline__mutmut_47': x_create_standard_pipeline__mutmut_47, 
    'x_create_standard_pipeline__mutmut_48': x_create_standard_pipeline__mutmut_48, 
    'x_create_standard_pipeline__mutmut_49': x_create_standard_pipeline__mutmut_49, 
    'x_create_standard_pipeline__mutmut_50': x_create_standard_pipeline__mutmut_50, 
    'x_create_standard_pipeline__mutmut_51': x_create_standard_pipeline__mutmut_51
}
x_create_standard_pipeline__mutmut_orig.__name__ = 'x_create_standard_pipeline'


def _load_seed_files_into_store(repo_root: Path, store: "GlossaryStore") -> None:
    args = [repo_root, store]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__load_seed_files_into_store__mutmut_orig, x__load_seed_files_into_store__mutmut_mutants, args, kwargs, None)


def x__load_seed_files_into_store__mutmut_orig(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(scope, repo_root)
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                "Failed to load seed file for scope %s: %s",
                scope.value,
                exc,
            )


def x__load_seed_files_into_store__mutmut_1(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = None
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                "Failed to load seed file for scope %s: %s",
                scope.value,
                exc,
            )


def x__load_seed_files_into_store__mutmut_2(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(None, repo_root)
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                "Failed to load seed file for scope %s: %s",
                scope.value,
                exc,
            )


def x__load_seed_files_into_store__mutmut_3(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(scope, None)
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                "Failed to load seed file for scope %s: %s",
                scope.value,
                exc,
            )


def x__load_seed_files_into_store__mutmut_4(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(repo_root)
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                "Failed to load seed file for scope %s: %s",
                scope.value,
                exc,
            )


def x__load_seed_files_into_store__mutmut_5(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(scope, )
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                "Failed to load seed file for scope %s: %s",
                scope.value,
                exc,
            )


def x__load_seed_files_into_store__mutmut_6(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(scope, repo_root)
            for sense in senses:
                store.add_sense(None)
        except Exception as exc:
            logger.warning(
                "Failed to load seed file for scope %s: %s",
                scope.value,
                exc,
            )


def x__load_seed_files_into_store__mutmut_7(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(scope, repo_root)
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                None,
                scope.value,
                exc,
            )


def x__load_seed_files_into_store__mutmut_8(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(scope, repo_root)
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                "Failed to load seed file for scope %s: %s",
                None,
                exc,
            )


def x__load_seed_files_into_store__mutmut_9(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(scope, repo_root)
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                "Failed to load seed file for scope %s: %s",
                scope.value,
                None,
            )


def x__load_seed_files_into_store__mutmut_10(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(scope, repo_root)
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                scope.value,
                exc,
            )


def x__load_seed_files_into_store__mutmut_11(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(scope, repo_root)
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                "Failed to load seed file for scope %s: %s",
                exc,
            )


def x__load_seed_files_into_store__mutmut_12(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(scope, repo_root)
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                "Failed to load seed file for scope %s: %s",
                scope.value,
                )


def x__load_seed_files_into_store__mutmut_13(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(scope, repo_root)
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                "XXFailed to load seed file for scope %s: %sXX",
                scope.value,
                exc,
            )


def x__load_seed_files_into_store__mutmut_14(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(scope, repo_root)
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                "failed to load seed file for scope %s: %s",
                scope.value,
                exc,
            )


def x__load_seed_files_into_store__mutmut_15(repo_root: Path, store: "GlossaryStore") -> None:
    """Load seed files from .kittify/glossaries/ into the glossary store.

    Args:
        repo_root: Repository root path.
        store: GlossaryStore to populate.
    """
    from specify_cli.glossary.scope import GlossaryScope, load_seed_file

    for scope in GlossaryScope:
        try:
            senses = load_seed_file(scope, repo_root)
            for sense in senses:
                store.add_sense(sense)
        except Exception as exc:
            logger.warning(
                "FAILED TO LOAD SEED FILE FOR SCOPE %S: %S",
                scope.value,
                exc,
            )

x__load_seed_files_into_store__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__load_seed_files_into_store__mutmut_1': x__load_seed_files_into_store__mutmut_1, 
    'x__load_seed_files_into_store__mutmut_2': x__load_seed_files_into_store__mutmut_2, 
    'x__load_seed_files_into_store__mutmut_3': x__load_seed_files_into_store__mutmut_3, 
    'x__load_seed_files_into_store__mutmut_4': x__load_seed_files_into_store__mutmut_4, 
    'x__load_seed_files_into_store__mutmut_5': x__load_seed_files_into_store__mutmut_5, 
    'x__load_seed_files_into_store__mutmut_6': x__load_seed_files_into_store__mutmut_6, 
    'x__load_seed_files_into_store__mutmut_7': x__load_seed_files_into_store__mutmut_7, 
    'x__load_seed_files_into_store__mutmut_8': x__load_seed_files_into_store__mutmut_8, 
    'x__load_seed_files_into_store__mutmut_9': x__load_seed_files_into_store__mutmut_9, 
    'x__load_seed_files_into_store__mutmut_10': x__load_seed_files_into_store__mutmut_10, 
    'x__load_seed_files_into_store__mutmut_11': x__load_seed_files_into_store__mutmut_11, 
    'x__load_seed_files_into_store__mutmut_12': x__load_seed_files_into_store__mutmut_12, 
    'x__load_seed_files_into_store__mutmut_13': x__load_seed_files_into_store__mutmut_13, 
    'x__load_seed_files_into_store__mutmut_14': x__load_seed_files_into_store__mutmut_14, 
    'x__load_seed_files_into_store__mutmut_15': x__load_seed_files_into_store__mutmut_15
}
x__load_seed_files_into_store__mutmut_orig.__name__ = 'x__load_seed_files_into_store'
