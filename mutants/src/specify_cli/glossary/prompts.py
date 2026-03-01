"""Typer prompts for interactive clarification (WP06/T026, T027).

This module implements user prompts for conflict resolution and
non-interactive mode detection for CI environments.
"""

import logging
import os
import sys
from enum import StrEnum
from typing import List, Tuple

import typer

from .models import SemanticConflict

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


class PromptChoice(StrEnum):
    """User choice during clarification."""

    SELECT_CANDIDATE = "select"
    CUSTOM_SENSE = "custom"
    DEFER = "defer"


# --------------------------------------------------------------------------- #
# Non-interactive detection (T027)
# --------------------------------------------------------------------------- #

_CI_ENV_VARS = [
    "CI",
    "GITHUB_ACTIONS",
    "JENKINS_HOME",
    "GITLAB_CI",
    "CIRCLECI",
    "TRAVIS",
    "BUILDKITE",
]


def is_interactive() -> bool:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_is_interactive__mutmut_orig, x_is_interactive__mutmut_mutants, args, kwargs, None)


def x_is_interactive__mutmut_orig() -> bool:
    """Detect if running in an interactive terminal.

    Checks:
    1. sys.stdin.isatty() -- True if connected to a terminal
    2. CI environment variables (CI, GITHUB_ACTIONS, JENKINS_HOME, etc.)

    Returns:
        True if interactive, False if non-interactive (CI, piped input, etc.)
    """
    # Check if stdin is a TTY
    if not sys.stdin.isatty():
        return False

    # Check common CI environment variables
    for var in _CI_ENV_VARS:
        if os.getenv(var):
            return False

    return True


def x_is_interactive__mutmut_1() -> bool:
    """Detect if running in an interactive terminal.

    Checks:
    1. sys.stdin.isatty() -- True if connected to a terminal
    2. CI environment variables (CI, GITHUB_ACTIONS, JENKINS_HOME, etc.)

    Returns:
        True if interactive, False if non-interactive (CI, piped input, etc.)
    """
    # Check if stdin is a TTY
    if sys.stdin.isatty():
        return False

    # Check common CI environment variables
    for var in _CI_ENV_VARS:
        if os.getenv(var):
            return False

    return True


def x_is_interactive__mutmut_2() -> bool:
    """Detect if running in an interactive terminal.

    Checks:
    1. sys.stdin.isatty() -- True if connected to a terminal
    2. CI environment variables (CI, GITHUB_ACTIONS, JENKINS_HOME, etc.)

    Returns:
        True if interactive, False if non-interactive (CI, piped input, etc.)
    """
    # Check if stdin is a TTY
    if not sys.stdin.isatty():
        return True

    # Check common CI environment variables
    for var in _CI_ENV_VARS:
        if os.getenv(var):
            return False

    return True


def x_is_interactive__mutmut_3() -> bool:
    """Detect if running in an interactive terminal.

    Checks:
    1. sys.stdin.isatty() -- True if connected to a terminal
    2. CI environment variables (CI, GITHUB_ACTIONS, JENKINS_HOME, etc.)

    Returns:
        True if interactive, False if non-interactive (CI, piped input, etc.)
    """
    # Check if stdin is a TTY
    if not sys.stdin.isatty():
        return False

    # Check common CI environment variables
    for var in _CI_ENV_VARS:
        if os.getenv(None):
            return False

    return True


def x_is_interactive__mutmut_4() -> bool:
    """Detect if running in an interactive terminal.

    Checks:
    1. sys.stdin.isatty() -- True if connected to a terminal
    2. CI environment variables (CI, GITHUB_ACTIONS, JENKINS_HOME, etc.)

    Returns:
        True if interactive, False if non-interactive (CI, piped input, etc.)
    """
    # Check if stdin is a TTY
    if not sys.stdin.isatty():
        return False

    # Check common CI environment variables
    for var in _CI_ENV_VARS:
        if os.getenv(var):
            return True

    return True


def x_is_interactive__mutmut_5() -> bool:
    """Detect if running in an interactive terminal.

    Checks:
    1. sys.stdin.isatty() -- True if connected to a terminal
    2. CI environment variables (CI, GITHUB_ACTIONS, JENKINS_HOME, etc.)

    Returns:
        True if interactive, False if non-interactive (CI, piped input, etc.)
    """
    # Check if stdin is a TTY
    if not sys.stdin.isatty():
        return False

    # Check common CI environment variables
    for var in _CI_ENV_VARS:
        if os.getenv(var):
            return False

    return False

x_is_interactive__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_is_interactive__mutmut_1': x_is_interactive__mutmut_1, 
    'x_is_interactive__mutmut_2': x_is_interactive__mutmut_2, 
    'x_is_interactive__mutmut_3': x_is_interactive__mutmut_3, 
    'x_is_interactive__mutmut_4': x_is_interactive__mutmut_4, 
    'x_is_interactive__mutmut_5': x_is_interactive__mutmut_5
}
x_is_interactive__mutmut_orig.__name__ = 'x_is_interactive'


def log_non_interactive_context() -> None:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_log_non_interactive_context__mutmut_orig, x_log_non_interactive_context__mutmut_mutants, args, kwargs, None)


def x_log_non_interactive_context__mutmut_orig() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_1() -> None:
    """Log details about non-interactive detection for debugging."""
    if is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_2() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info(None)
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_3() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("XXNon-interactive mode detectedXX")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_4() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_5() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("NON-INTERACTIVE MODE DETECTED")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_6() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info(None, sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_7() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", None)
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_8() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info(sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_9() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", )
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_10() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("XX  stdin.isatty(): %sXX", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_11() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  STDIN.ISATTY(): %S", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_12() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = None
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_13() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(None)]
        if detected_ci:
            logger.info("  CI env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_14() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info(None, detected_ci)


def x_log_non_interactive_context__mutmut_15() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", None)


def x_log_non_interactive_context__mutmut_16() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info(detected_ci)


def x_log_non_interactive_context__mutmut_17() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI env vars: %s", )


def x_log_non_interactive_context__mutmut_18() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("XX  CI env vars: %sXX", detected_ci)


def x_log_non_interactive_context__mutmut_19() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  ci env vars: %s", detected_ci)


def x_log_non_interactive_context__mutmut_20() -> None:
    """Log details about non-interactive detection for debugging."""
    if not is_interactive():
        logger.info("Non-interactive mode detected")
        logger.info("  stdin.isatty(): %s", sys.stdin.isatty())
        detected_ci = [k for k in _CI_ENV_VARS if os.getenv(k)]
        if detected_ci:
            logger.info("  CI ENV VARS: %S", detected_ci)

x_log_non_interactive_context__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_log_non_interactive_context__mutmut_1': x_log_non_interactive_context__mutmut_1, 
    'x_log_non_interactive_context__mutmut_2': x_log_non_interactive_context__mutmut_2, 
    'x_log_non_interactive_context__mutmut_3': x_log_non_interactive_context__mutmut_3, 
    'x_log_non_interactive_context__mutmut_4': x_log_non_interactive_context__mutmut_4, 
    'x_log_non_interactive_context__mutmut_5': x_log_non_interactive_context__mutmut_5, 
    'x_log_non_interactive_context__mutmut_6': x_log_non_interactive_context__mutmut_6, 
    'x_log_non_interactive_context__mutmut_7': x_log_non_interactive_context__mutmut_7, 
    'x_log_non_interactive_context__mutmut_8': x_log_non_interactive_context__mutmut_8, 
    'x_log_non_interactive_context__mutmut_9': x_log_non_interactive_context__mutmut_9, 
    'x_log_non_interactive_context__mutmut_10': x_log_non_interactive_context__mutmut_10, 
    'x_log_non_interactive_context__mutmut_11': x_log_non_interactive_context__mutmut_11, 
    'x_log_non_interactive_context__mutmut_12': x_log_non_interactive_context__mutmut_12, 
    'x_log_non_interactive_context__mutmut_13': x_log_non_interactive_context__mutmut_13, 
    'x_log_non_interactive_context__mutmut_14': x_log_non_interactive_context__mutmut_14, 
    'x_log_non_interactive_context__mutmut_15': x_log_non_interactive_context__mutmut_15, 
    'x_log_non_interactive_context__mutmut_16': x_log_non_interactive_context__mutmut_16, 
    'x_log_non_interactive_context__mutmut_17': x_log_non_interactive_context__mutmut_17, 
    'x_log_non_interactive_context__mutmut_18': x_log_non_interactive_context__mutmut_18, 
    'x_log_non_interactive_context__mutmut_19': x_log_non_interactive_context__mutmut_19, 
    'x_log_non_interactive_context__mutmut_20': x_log_non_interactive_context__mutmut_20
}
x_log_non_interactive_context__mutmut_orig.__name__ = 'x_log_non_interactive_context'


def auto_defer_conflicts(
    conflicts: List[SemanticConflict],
) -> List[Tuple[SemanticConflict, PromptChoice, None]]:
    """Auto-defer all conflicts in non-interactive mode.

    Args:
        conflicts: List of semantic conflicts

    Returns:
        List of (conflict, DEFER, None) tuples for each conflict
    """
    return [(conflict, PromptChoice.DEFER, None) for conflict in conflicts]


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def prompt_conflict_resolution(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    args = [conflict]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_prompt_conflict_resolution__mutmut_orig, x_prompt_conflict_resolution__mutmut_mutants, args, kwargs, None)


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_orig(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_1(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = None

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_2(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = None
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_3(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates >= 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_4(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 1:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_5(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(None)
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_6(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append(None)
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_7(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("XX  C: Provide custom definitionXX")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_8(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  c: provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_9(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: PROVIDE CUSTOM DEFINITION")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_10(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append(None)
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_11(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("XX  D: Defer to async resolutionXX")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_12(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  d: defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_13(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: DEFER TO ASYNC RESOLUTION")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_14(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = None

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_15(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(None)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_16(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "XX\nXX".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_17(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = None

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_18(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while False:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_19(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = None

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_20(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().lower()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_21(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(None).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_22(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response != "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_23(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "XXDXX":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_24(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "d":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_25(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response != "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_26(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "XXCXX":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_27(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "c":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_28(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = None

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_29(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    None,
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_30(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=None,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_31(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_32(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_33(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "XX\nEnter custom definitionXX",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_34(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nenter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_35(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nENTER CUSTOM DEFINITION",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_36(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_37(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo(None)
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_38(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("XXError: Definition cannot be empty. Try again.XX")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_39(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("error: definition cannot be empty. try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_40(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("ERROR: DEFINITION CANNOT BE EMPTY. TRY AGAIN.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_41(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    break

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_42(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = None
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_43(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(None)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_44(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 2 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_45(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 < choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_46(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num < num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_47(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num + 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_48(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 2)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_49(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates >= 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_50(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 1:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_51(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            None
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_52(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            None
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_53(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "XXError: No candidates available. Enter C for custom or D to defer.XX"
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_54(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "error: no candidates available. enter c for custom or d to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_55(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "ERROR: NO CANDIDATES AVAILABLE. ENTER C FOR CUSTOM OR D TO DEFER."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_56(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    break

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_57(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates >= 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_58(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 1:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_59(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    None
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_60(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    None
                )

        except typer.Abort:
            typer.echo("\nAborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_61(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo(None)
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_62(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("XX\nAborted by user.XX")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_63(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\naborted by user.")
            raise


# --------------------------------------------------------------------------- #
# Interactive prompts (T026)
# --------------------------------------------------------------------------- #


def x_prompt_conflict_resolution__mutmut_64(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Prompt user to resolve a semantic conflict.

    Displays options:
    - 1-N: Select candidate sense (by number)
    - C: Provide custom sense definition
    - D: Defer to async resolution

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        Tuple of (choice type, value):
        - (SELECT_CANDIDATE, candidate_index) if user selects 1-N (0-indexed)
        - (CUSTOM_SENSE, custom_definition) if user enters C
        - (DEFER, None) if user enters D

    Raises:
        typer.Abort: If user cancels with Ctrl+C
    """
    num_candidates = len(conflict.candidate_senses)

    # Build prompt message
    options: List[str] = []
    if num_candidates > 0:
        options.append(f"  1-{num_candidates}: Choose candidate sense")
    options.append("  C: Provide custom definition")
    options.append("  D: Defer to async resolution")
    options_text = "\n".join(options)

    prompt_msg = f"\nSelect resolution:\n{options_text}\n\nYour choice"

    while True:
        try:
            response = typer.prompt(prompt_msg).strip().upper()

            # Handle defer
            if response == "D":
                return (PromptChoice.DEFER, None)

            # Handle custom sense
            if response == "C":
                custom_def = typer.prompt(
                    "\nEnter custom definition",
                    type=str,
                ).strip()

                if not custom_def:
                    typer.echo("Error: Definition cannot be empty. Try again.")
                    continue

                return (PromptChoice.CUSTOM_SENSE, custom_def)

            # Handle candidate selection
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= num_candidates:
                    # Return 0-indexed candidate index
                    return (PromptChoice.SELECT_CANDIDATE, choice_num - 1)
                else:
                    if num_candidates > 0:
                        typer.echo(
                            f"Error: Please enter a number between 1 and "
                            f"{num_candidates}, C for custom, or D to defer."
                        )
                    else:
                        typer.echo(
                            "Error: No candidates available. Enter C for custom or D to defer."
                        )
                    continue

            # Invalid input
            if num_candidates > 0:
                typer.echo(
                    f"Error: Invalid choice '{response}'. "
                    f"Enter 1-{num_candidates}, C, or D."
                )
            else:
                typer.echo(
                    f"Error: Invalid choice '{response}'. Enter C or D."
                )

        except typer.Abort:
            typer.echo("\nABORTED BY USER.")
            raise

x_prompt_conflict_resolution__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_prompt_conflict_resolution__mutmut_1': x_prompt_conflict_resolution__mutmut_1, 
    'x_prompt_conflict_resolution__mutmut_2': x_prompt_conflict_resolution__mutmut_2, 
    'x_prompt_conflict_resolution__mutmut_3': x_prompt_conflict_resolution__mutmut_3, 
    'x_prompt_conflict_resolution__mutmut_4': x_prompt_conflict_resolution__mutmut_4, 
    'x_prompt_conflict_resolution__mutmut_5': x_prompt_conflict_resolution__mutmut_5, 
    'x_prompt_conflict_resolution__mutmut_6': x_prompt_conflict_resolution__mutmut_6, 
    'x_prompt_conflict_resolution__mutmut_7': x_prompt_conflict_resolution__mutmut_7, 
    'x_prompt_conflict_resolution__mutmut_8': x_prompt_conflict_resolution__mutmut_8, 
    'x_prompt_conflict_resolution__mutmut_9': x_prompt_conflict_resolution__mutmut_9, 
    'x_prompt_conflict_resolution__mutmut_10': x_prompt_conflict_resolution__mutmut_10, 
    'x_prompt_conflict_resolution__mutmut_11': x_prompt_conflict_resolution__mutmut_11, 
    'x_prompt_conflict_resolution__mutmut_12': x_prompt_conflict_resolution__mutmut_12, 
    'x_prompt_conflict_resolution__mutmut_13': x_prompt_conflict_resolution__mutmut_13, 
    'x_prompt_conflict_resolution__mutmut_14': x_prompt_conflict_resolution__mutmut_14, 
    'x_prompt_conflict_resolution__mutmut_15': x_prompt_conflict_resolution__mutmut_15, 
    'x_prompt_conflict_resolution__mutmut_16': x_prompt_conflict_resolution__mutmut_16, 
    'x_prompt_conflict_resolution__mutmut_17': x_prompt_conflict_resolution__mutmut_17, 
    'x_prompt_conflict_resolution__mutmut_18': x_prompt_conflict_resolution__mutmut_18, 
    'x_prompt_conflict_resolution__mutmut_19': x_prompt_conflict_resolution__mutmut_19, 
    'x_prompt_conflict_resolution__mutmut_20': x_prompt_conflict_resolution__mutmut_20, 
    'x_prompt_conflict_resolution__mutmut_21': x_prompt_conflict_resolution__mutmut_21, 
    'x_prompt_conflict_resolution__mutmut_22': x_prompt_conflict_resolution__mutmut_22, 
    'x_prompt_conflict_resolution__mutmut_23': x_prompt_conflict_resolution__mutmut_23, 
    'x_prompt_conflict_resolution__mutmut_24': x_prompt_conflict_resolution__mutmut_24, 
    'x_prompt_conflict_resolution__mutmut_25': x_prompt_conflict_resolution__mutmut_25, 
    'x_prompt_conflict_resolution__mutmut_26': x_prompt_conflict_resolution__mutmut_26, 
    'x_prompt_conflict_resolution__mutmut_27': x_prompt_conflict_resolution__mutmut_27, 
    'x_prompt_conflict_resolution__mutmut_28': x_prompt_conflict_resolution__mutmut_28, 
    'x_prompt_conflict_resolution__mutmut_29': x_prompt_conflict_resolution__mutmut_29, 
    'x_prompt_conflict_resolution__mutmut_30': x_prompt_conflict_resolution__mutmut_30, 
    'x_prompt_conflict_resolution__mutmut_31': x_prompt_conflict_resolution__mutmut_31, 
    'x_prompt_conflict_resolution__mutmut_32': x_prompt_conflict_resolution__mutmut_32, 
    'x_prompt_conflict_resolution__mutmut_33': x_prompt_conflict_resolution__mutmut_33, 
    'x_prompt_conflict_resolution__mutmut_34': x_prompt_conflict_resolution__mutmut_34, 
    'x_prompt_conflict_resolution__mutmut_35': x_prompt_conflict_resolution__mutmut_35, 
    'x_prompt_conflict_resolution__mutmut_36': x_prompt_conflict_resolution__mutmut_36, 
    'x_prompt_conflict_resolution__mutmut_37': x_prompt_conflict_resolution__mutmut_37, 
    'x_prompt_conflict_resolution__mutmut_38': x_prompt_conflict_resolution__mutmut_38, 
    'x_prompt_conflict_resolution__mutmut_39': x_prompt_conflict_resolution__mutmut_39, 
    'x_prompt_conflict_resolution__mutmut_40': x_prompt_conflict_resolution__mutmut_40, 
    'x_prompt_conflict_resolution__mutmut_41': x_prompt_conflict_resolution__mutmut_41, 
    'x_prompt_conflict_resolution__mutmut_42': x_prompt_conflict_resolution__mutmut_42, 
    'x_prompt_conflict_resolution__mutmut_43': x_prompt_conflict_resolution__mutmut_43, 
    'x_prompt_conflict_resolution__mutmut_44': x_prompt_conflict_resolution__mutmut_44, 
    'x_prompt_conflict_resolution__mutmut_45': x_prompt_conflict_resolution__mutmut_45, 
    'x_prompt_conflict_resolution__mutmut_46': x_prompt_conflict_resolution__mutmut_46, 
    'x_prompt_conflict_resolution__mutmut_47': x_prompt_conflict_resolution__mutmut_47, 
    'x_prompt_conflict_resolution__mutmut_48': x_prompt_conflict_resolution__mutmut_48, 
    'x_prompt_conflict_resolution__mutmut_49': x_prompt_conflict_resolution__mutmut_49, 
    'x_prompt_conflict_resolution__mutmut_50': x_prompt_conflict_resolution__mutmut_50, 
    'x_prompt_conflict_resolution__mutmut_51': x_prompt_conflict_resolution__mutmut_51, 
    'x_prompt_conflict_resolution__mutmut_52': x_prompt_conflict_resolution__mutmut_52, 
    'x_prompt_conflict_resolution__mutmut_53': x_prompt_conflict_resolution__mutmut_53, 
    'x_prompt_conflict_resolution__mutmut_54': x_prompt_conflict_resolution__mutmut_54, 
    'x_prompt_conflict_resolution__mutmut_55': x_prompt_conflict_resolution__mutmut_55, 
    'x_prompt_conflict_resolution__mutmut_56': x_prompt_conflict_resolution__mutmut_56, 
    'x_prompt_conflict_resolution__mutmut_57': x_prompt_conflict_resolution__mutmut_57, 
    'x_prompt_conflict_resolution__mutmut_58': x_prompt_conflict_resolution__mutmut_58, 
    'x_prompt_conflict_resolution__mutmut_59': x_prompt_conflict_resolution__mutmut_59, 
    'x_prompt_conflict_resolution__mutmut_60': x_prompt_conflict_resolution__mutmut_60, 
    'x_prompt_conflict_resolution__mutmut_61': x_prompt_conflict_resolution__mutmut_61, 
    'x_prompt_conflict_resolution__mutmut_62': x_prompt_conflict_resolution__mutmut_62, 
    'x_prompt_conflict_resolution__mutmut_63': x_prompt_conflict_resolution__mutmut_63, 
    'x_prompt_conflict_resolution__mutmut_64': x_prompt_conflict_resolution__mutmut_64
}
x_prompt_conflict_resolution__mutmut_orig.__name__ = 'x_prompt_conflict_resolution'


def prompt_conflict_resolution_safe(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    args = [conflict]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_prompt_conflict_resolution_safe__mutmut_orig, x_prompt_conflict_resolution_safe__mutmut_mutants, args, kwargs, None)


def x_prompt_conflict_resolution_safe__mutmut_orig(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Safe prompt that auto-defers in non-interactive mode.

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        (DEFER, None) if non-interactive, otherwise delegates to interactive prompt
    """
    if not is_interactive():
        typer.echo(
            f"Non-interactive mode detected: "
            f"Auto-deferring conflict for '{conflict.term.surface_text}'"
        )
        return (PromptChoice.DEFER, None)

    return prompt_conflict_resolution(conflict)


def x_prompt_conflict_resolution_safe__mutmut_1(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Safe prompt that auto-defers in non-interactive mode.

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        (DEFER, None) if non-interactive, otherwise delegates to interactive prompt
    """
    if is_interactive():
        typer.echo(
            f"Non-interactive mode detected: "
            f"Auto-deferring conflict for '{conflict.term.surface_text}'"
        )
        return (PromptChoice.DEFER, None)

    return prompt_conflict_resolution(conflict)


def x_prompt_conflict_resolution_safe__mutmut_2(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Safe prompt that auto-defers in non-interactive mode.

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        (DEFER, None) if non-interactive, otherwise delegates to interactive prompt
    """
    if not is_interactive():
        typer.echo(
            None
        )
        return (PromptChoice.DEFER, None)

    return prompt_conflict_resolution(conflict)


def x_prompt_conflict_resolution_safe__mutmut_3(
    conflict: SemanticConflict,
) -> Tuple[PromptChoice, int | str | None]:
    """Safe prompt that auto-defers in non-interactive mode.

    Args:
        conflict: The semantic conflict to resolve

    Returns:
        (DEFER, None) if non-interactive, otherwise delegates to interactive prompt
    """
    if not is_interactive():
        typer.echo(
            f"Non-interactive mode detected: "
            f"Auto-deferring conflict for '{conflict.term.surface_text}'"
        )
        return (PromptChoice.DEFER, None)

    return prompt_conflict_resolution(None)

x_prompt_conflict_resolution_safe__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_prompt_conflict_resolution_safe__mutmut_1': x_prompt_conflict_resolution_safe__mutmut_1, 
    'x_prompt_conflict_resolution_safe__mutmut_2': x_prompt_conflict_resolution_safe__mutmut_2, 
    'x_prompt_conflict_resolution_safe__mutmut_3': x_prompt_conflict_resolution_safe__mutmut_3
}
x_prompt_conflict_resolution_safe__mutmut_orig.__name__ = 'x_prompt_conflict_resolution_safe'


def prompt_context_change_confirmation(
    old_hash: str,
    new_hash: str,
) -> bool:
    args = [old_hash, new_hash]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_prompt_context_change_confirmation__mutmut_orig, x_prompt_context_change_confirmation__mutmut_mutants, args, kwargs, None)


def x_prompt_context_change_confirmation__mutmut_orig(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user to confirm resumption if context has changed.

    Args:
        old_hash: Original input hash from checkpoint
        new_hash: Current input hash

    Returns:
        True if user confirms, False otherwise
    """
    typer.echo(
        f"\nWarning: Step inputs have changed since checkpoint.\n"
        f"  Original hash: {old_hash[:16]}...\n"
        f"  Current hash:  {new_hash[:16]}...\n"
    )

    return typer.confirm(
        "Context may have changed. Proceed with resolution?",
        default=False,
    )


def x_prompt_context_change_confirmation__mutmut_1(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user to confirm resumption if context has changed.

    Args:
        old_hash: Original input hash from checkpoint
        new_hash: Current input hash

    Returns:
        True if user confirms, False otherwise
    """
    typer.echo(
        None
    )

    return typer.confirm(
        "Context may have changed. Proceed with resolution?",
        default=False,
    )


def x_prompt_context_change_confirmation__mutmut_2(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user to confirm resumption if context has changed.

    Args:
        old_hash: Original input hash from checkpoint
        new_hash: Current input hash

    Returns:
        True if user confirms, False otherwise
    """
    typer.echo(
        f"\nWarning: Step inputs have changed since checkpoint.\n"
        f"  Original hash: {old_hash[:17]}...\n"
        f"  Current hash:  {new_hash[:16]}...\n"
    )

    return typer.confirm(
        "Context may have changed. Proceed with resolution?",
        default=False,
    )


def x_prompt_context_change_confirmation__mutmut_3(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user to confirm resumption if context has changed.

    Args:
        old_hash: Original input hash from checkpoint
        new_hash: Current input hash

    Returns:
        True if user confirms, False otherwise
    """
    typer.echo(
        f"\nWarning: Step inputs have changed since checkpoint.\n"
        f"  Original hash: {old_hash[:16]}...\n"
        f"  Current hash:  {new_hash[:17]}...\n"
    )

    return typer.confirm(
        "Context may have changed. Proceed with resolution?",
        default=False,
    )


def x_prompt_context_change_confirmation__mutmut_4(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user to confirm resumption if context has changed.

    Args:
        old_hash: Original input hash from checkpoint
        new_hash: Current input hash

    Returns:
        True if user confirms, False otherwise
    """
    typer.echo(
        f"\nWarning: Step inputs have changed since checkpoint.\n"
        f"  Original hash: {old_hash[:16]}...\n"
        f"  Current hash:  {new_hash[:16]}...\n"
    )

    return typer.confirm(
        None,
        default=False,
    )


def x_prompt_context_change_confirmation__mutmut_5(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user to confirm resumption if context has changed.

    Args:
        old_hash: Original input hash from checkpoint
        new_hash: Current input hash

    Returns:
        True if user confirms, False otherwise
    """
    typer.echo(
        f"\nWarning: Step inputs have changed since checkpoint.\n"
        f"  Original hash: {old_hash[:16]}...\n"
        f"  Current hash:  {new_hash[:16]}...\n"
    )

    return typer.confirm(
        "Context may have changed. Proceed with resolution?",
        default=None,
    )


def x_prompt_context_change_confirmation__mutmut_6(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user to confirm resumption if context has changed.

    Args:
        old_hash: Original input hash from checkpoint
        new_hash: Current input hash

    Returns:
        True if user confirms, False otherwise
    """
    typer.echo(
        f"\nWarning: Step inputs have changed since checkpoint.\n"
        f"  Original hash: {old_hash[:16]}...\n"
        f"  Current hash:  {new_hash[:16]}...\n"
    )

    return typer.confirm(
        default=False,
    )


def x_prompt_context_change_confirmation__mutmut_7(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user to confirm resumption if context has changed.

    Args:
        old_hash: Original input hash from checkpoint
        new_hash: Current input hash

    Returns:
        True if user confirms, False otherwise
    """
    typer.echo(
        f"\nWarning: Step inputs have changed since checkpoint.\n"
        f"  Original hash: {old_hash[:16]}...\n"
        f"  Current hash:  {new_hash[:16]}...\n"
    )

    return typer.confirm(
        "Context may have changed. Proceed with resolution?",
        )


def x_prompt_context_change_confirmation__mutmut_8(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user to confirm resumption if context has changed.

    Args:
        old_hash: Original input hash from checkpoint
        new_hash: Current input hash

    Returns:
        True if user confirms, False otherwise
    """
    typer.echo(
        f"\nWarning: Step inputs have changed since checkpoint.\n"
        f"  Original hash: {old_hash[:16]}...\n"
        f"  Current hash:  {new_hash[:16]}...\n"
    )

    return typer.confirm(
        "XXContext may have changed. Proceed with resolution?XX",
        default=False,
    )


def x_prompt_context_change_confirmation__mutmut_9(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user to confirm resumption if context has changed.

    Args:
        old_hash: Original input hash from checkpoint
        new_hash: Current input hash

    Returns:
        True if user confirms, False otherwise
    """
    typer.echo(
        f"\nWarning: Step inputs have changed since checkpoint.\n"
        f"  Original hash: {old_hash[:16]}...\n"
        f"  Current hash:  {new_hash[:16]}...\n"
    )

    return typer.confirm(
        "context may have changed. proceed with resolution?",
        default=False,
    )


def x_prompt_context_change_confirmation__mutmut_10(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user to confirm resumption if context has changed.

    Args:
        old_hash: Original input hash from checkpoint
        new_hash: Current input hash

    Returns:
        True if user confirms, False otherwise
    """
    typer.echo(
        f"\nWarning: Step inputs have changed since checkpoint.\n"
        f"  Original hash: {old_hash[:16]}...\n"
        f"  Current hash:  {new_hash[:16]}...\n"
    )

    return typer.confirm(
        "CONTEXT MAY HAVE CHANGED. PROCEED WITH RESOLUTION?",
        default=False,
    )


def x_prompt_context_change_confirmation__mutmut_11(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user to confirm resumption if context has changed.

    Args:
        old_hash: Original input hash from checkpoint
        new_hash: Current input hash

    Returns:
        True if user confirms, False otherwise
    """
    typer.echo(
        f"\nWarning: Step inputs have changed since checkpoint.\n"
        f"  Original hash: {old_hash[:16]}...\n"
        f"  Current hash:  {new_hash[:16]}...\n"
    )

    return typer.confirm(
        "Context may have changed. Proceed with resolution?",
        default=True,
    )

x_prompt_context_change_confirmation__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_prompt_context_change_confirmation__mutmut_1': x_prompt_context_change_confirmation__mutmut_1, 
    'x_prompt_context_change_confirmation__mutmut_2': x_prompt_context_change_confirmation__mutmut_2, 
    'x_prompt_context_change_confirmation__mutmut_3': x_prompt_context_change_confirmation__mutmut_3, 
    'x_prompt_context_change_confirmation__mutmut_4': x_prompt_context_change_confirmation__mutmut_4, 
    'x_prompt_context_change_confirmation__mutmut_5': x_prompt_context_change_confirmation__mutmut_5, 
    'x_prompt_context_change_confirmation__mutmut_6': x_prompt_context_change_confirmation__mutmut_6, 
    'x_prompt_context_change_confirmation__mutmut_7': x_prompt_context_change_confirmation__mutmut_7, 
    'x_prompt_context_change_confirmation__mutmut_8': x_prompt_context_change_confirmation__mutmut_8, 
    'x_prompt_context_change_confirmation__mutmut_9': x_prompt_context_change_confirmation__mutmut_9, 
    'x_prompt_context_change_confirmation__mutmut_10': x_prompt_context_change_confirmation__mutmut_10, 
    'x_prompt_context_change_confirmation__mutmut_11': x_prompt_context_change_confirmation__mutmut_11
}
x_prompt_context_change_confirmation__mutmut_orig.__name__ = 'x_prompt_context_change_confirmation'
