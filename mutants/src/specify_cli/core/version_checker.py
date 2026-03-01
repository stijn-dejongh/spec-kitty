"""Version compatibility checking for spec-kitty CLI and projects."""

from __future__ import annotations

from pathlib import Path
from typing import Literal, Optional

from packaging.version import Version, InvalidVersion

from specify_cli.upgrade.metadata import ProjectMetadata


MismatchType = Literal["cli_newer", "project_newer", "match", "unknown"]
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


def get_cli_version() -> str:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_cli_version__mutmut_orig, x_get_cli_version__mutmut_mutants, args, kwargs, None)


def x_get_cli_version__mutmut_orig() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_1() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get(None) == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_2() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("XXSPEC_KITTY_TEST_MODEXX") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_3() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("spec_kitty_test_mode") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_4() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") != "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_5() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "XX1XX":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_6() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = None
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_7() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get(None)
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_8() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("XXSPEC_KITTY_CLI_VERSIONXX")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_9() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("spec_kitty_cli_version")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_10() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_11() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                None
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_12() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "XXSPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. XX"
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_13() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "spec_kitty_test_mode=1 requires spec_kitty_cli_version to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_14() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 REQUIRES SPEC_KITTY_CLI_VERSION TO BE SET. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_15() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "XXThis is a bug in the test fixtures. Tests must use the isolated_env XX"
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_16() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "this is a bug in the test fixtures. tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_17() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "THIS IS A BUG IN THE TEST FIXTURES. TESTS MUST USE THE ISOLATED_ENV "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_18() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "XXfixture to ensure proper version isolation.XX"
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_19() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "FIXTURE TO ENSURE PROPER VERSION ISOLATION."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_20() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = None
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_21() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get(None)
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_22() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("XXSPEC_KITTY_CLI_VERSIONXX")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_23() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("spec_kitty_cli_version")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_24() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version(None)
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_25() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("XXspec-kitty-cliXX")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_26() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("SPEC-KITTY-CLI")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"


def x_get_cli_version__mutmut_27() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "XXunknownXX"


def x_get_cli_version__mutmut_28() -> str:
    """Get the installed spec-kitty-cli version.

    Returns:
        Version string (e.g., "0.9.0" or "0.5.0-dev")

    Raises:
        RuntimeError: If test mode is enabled but no version override is set
    """
    import os

    # Test mode: MUST use override, never fall back to installed version
    # This ensures tests always use source code version, not pip-installed package
    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        override = os.environ.get("SPEC_KITTY_CLI_VERSION")
        if not override:
            raise RuntimeError(
                "SPEC_KITTY_TEST_MODE=1 requires SPEC_KITTY_CLI_VERSION to be set. "
                "This is a bug in the test fixtures. Tests must use the isolated_env "
                "fixture to ensure proper version isolation."
            )
        return override

    # Production mode: allow override, then try installed, then module __version__
    override_version = os.environ.get("SPEC_KITTY_CLI_VERSION")
    if override_version:
        return override_version

    try:
        from importlib.metadata import PackageNotFoundError, version as get_version
        return get_version("spec-kitty-cli")
    except PackageNotFoundError:
        # Fall back to __version__ from __init__.py
        try:
            from specify_cli import __version__
            return __version__
        except (ImportError, AttributeError):
            return "UNKNOWN"

x_get_cli_version__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_cli_version__mutmut_1': x_get_cli_version__mutmut_1, 
    'x_get_cli_version__mutmut_2': x_get_cli_version__mutmut_2, 
    'x_get_cli_version__mutmut_3': x_get_cli_version__mutmut_3, 
    'x_get_cli_version__mutmut_4': x_get_cli_version__mutmut_4, 
    'x_get_cli_version__mutmut_5': x_get_cli_version__mutmut_5, 
    'x_get_cli_version__mutmut_6': x_get_cli_version__mutmut_6, 
    'x_get_cli_version__mutmut_7': x_get_cli_version__mutmut_7, 
    'x_get_cli_version__mutmut_8': x_get_cli_version__mutmut_8, 
    'x_get_cli_version__mutmut_9': x_get_cli_version__mutmut_9, 
    'x_get_cli_version__mutmut_10': x_get_cli_version__mutmut_10, 
    'x_get_cli_version__mutmut_11': x_get_cli_version__mutmut_11, 
    'x_get_cli_version__mutmut_12': x_get_cli_version__mutmut_12, 
    'x_get_cli_version__mutmut_13': x_get_cli_version__mutmut_13, 
    'x_get_cli_version__mutmut_14': x_get_cli_version__mutmut_14, 
    'x_get_cli_version__mutmut_15': x_get_cli_version__mutmut_15, 
    'x_get_cli_version__mutmut_16': x_get_cli_version__mutmut_16, 
    'x_get_cli_version__mutmut_17': x_get_cli_version__mutmut_17, 
    'x_get_cli_version__mutmut_18': x_get_cli_version__mutmut_18, 
    'x_get_cli_version__mutmut_19': x_get_cli_version__mutmut_19, 
    'x_get_cli_version__mutmut_20': x_get_cli_version__mutmut_20, 
    'x_get_cli_version__mutmut_21': x_get_cli_version__mutmut_21, 
    'x_get_cli_version__mutmut_22': x_get_cli_version__mutmut_22, 
    'x_get_cli_version__mutmut_23': x_get_cli_version__mutmut_23, 
    'x_get_cli_version__mutmut_24': x_get_cli_version__mutmut_24, 
    'x_get_cli_version__mutmut_25': x_get_cli_version__mutmut_25, 
    'x_get_cli_version__mutmut_26': x_get_cli_version__mutmut_26, 
    'x_get_cli_version__mutmut_27': x_get_cli_version__mutmut_27, 
    'x_get_cli_version__mutmut_28': x_get_cli_version__mutmut_28
}
x_get_cli_version__mutmut_orig.__name__ = 'x_get_cli_version'


def get_project_version(project_root: Path) -> Optional[str]:
    args = [project_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_project_version__mutmut_orig, x_get_project_version__mutmut_mutants, args, kwargs, None)


def x_get_project_version__mutmut_orig(project_root: Path) -> Optional[str]:
    """Get the project's spec-kitty version from metadata.

    Args:
        project_root: Path to project root (parent of .kittify)

    Returns:
        Version string if metadata exists, None for legacy projects
    """
    kittify_dir = project_root / ".kittify"
    if not kittify_dir.exists():
        return None

    metadata = ProjectMetadata.load(kittify_dir)
    if metadata is None:
        return None

    return metadata.version


def x_get_project_version__mutmut_1(project_root: Path) -> Optional[str]:
    """Get the project's spec-kitty version from metadata.

    Args:
        project_root: Path to project root (parent of .kittify)

    Returns:
        Version string if metadata exists, None for legacy projects
    """
    kittify_dir = None
    if not kittify_dir.exists():
        return None

    metadata = ProjectMetadata.load(kittify_dir)
    if metadata is None:
        return None

    return metadata.version


def x_get_project_version__mutmut_2(project_root: Path) -> Optional[str]:
    """Get the project's spec-kitty version from metadata.

    Args:
        project_root: Path to project root (parent of .kittify)

    Returns:
        Version string if metadata exists, None for legacy projects
    """
    kittify_dir = project_root * ".kittify"
    if not kittify_dir.exists():
        return None

    metadata = ProjectMetadata.load(kittify_dir)
    if metadata is None:
        return None

    return metadata.version


def x_get_project_version__mutmut_3(project_root: Path) -> Optional[str]:
    """Get the project's spec-kitty version from metadata.

    Args:
        project_root: Path to project root (parent of .kittify)

    Returns:
        Version string if metadata exists, None for legacy projects
    """
    kittify_dir = project_root / "XX.kittifyXX"
    if not kittify_dir.exists():
        return None

    metadata = ProjectMetadata.load(kittify_dir)
    if metadata is None:
        return None

    return metadata.version


def x_get_project_version__mutmut_4(project_root: Path) -> Optional[str]:
    """Get the project's spec-kitty version from metadata.

    Args:
        project_root: Path to project root (parent of .kittify)

    Returns:
        Version string if metadata exists, None for legacy projects
    """
    kittify_dir = project_root / ".KITTIFY"
    if not kittify_dir.exists():
        return None

    metadata = ProjectMetadata.load(kittify_dir)
    if metadata is None:
        return None

    return metadata.version


def x_get_project_version__mutmut_5(project_root: Path) -> Optional[str]:
    """Get the project's spec-kitty version from metadata.

    Args:
        project_root: Path to project root (parent of .kittify)

    Returns:
        Version string if metadata exists, None for legacy projects
    """
    kittify_dir = project_root / ".kittify"
    if kittify_dir.exists():
        return None

    metadata = ProjectMetadata.load(kittify_dir)
    if metadata is None:
        return None

    return metadata.version


def x_get_project_version__mutmut_6(project_root: Path) -> Optional[str]:
    """Get the project's spec-kitty version from metadata.

    Args:
        project_root: Path to project root (parent of .kittify)

    Returns:
        Version string if metadata exists, None for legacy projects
    """
    kittify_dir = project_root / ".kittify"
    if not kittify_dir.exists():
        return None

    metadata = None
    if metadata is None:
        return None

    return metadata.version


def x_get_project_version__mutmut_7(project_root: Path) -> Optional[str]:
    """Get the project's spec-kitty version from metadata.

    Args:
        project_root: Path to project root (parent of .kittify)

    Returns:
        Version string if metadata exists, None for legacy projects
    """
    kittify_dir = project_root / ".kittify"
    if not kittify_dir.exists():
        return None

    metadata = ProjectMetadata.load(None)
    if metadata is None:
        return None

    return metadata.version


def x_get_project_version__mutmut_8(project_root: Path) -> Optional[str]:
    """Get the project's spec-kitty version from metadata.

    Args:
        project_root: Path to project root (parent of .kittify)

    Returns:
        Version string if metadata exists, None for legacy projects
    """
    kittify_dir = project_root / ".kittify"
    if not kittify_dir.exists():
        return None

    metadata = ProjectMetadata.load(kittify_dir)
    if metadata is not None:
        return None

    return metadata.version

x_get_project_version__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_project_version__mutmut_1': x_get_project_version__mutmut_1, 
    'x_get_project_version__mutmut_2': x_get_project_version__mutmut_2, 
    'x_get_project_version__mutmut_3': x_get_project_version__mutmut_3, 
    'x_get_project_version__mutmut_4': x_get_project_version__mutmut_4, 
    'x_get_project_version__mutmut_5': x_get_project_version__mutmut_5, 
    'x_get_project_version__mutmut_6': x_get_project_version__mutmut_6, 
    'x_get_project_version__mutmut_7': x_get_project_version__mutmut_7, 
    'x_get_project_version__mutmut_8': x_get_project_version__mutmut_8
}
x_get_project_version__mutmut_orig.__name__ = 'x_get_project_version'


def compare_versions(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    args = [cli_version, project_version]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_compare_versions__mutmut_orig, x_compare_versions__mutmut_mutants, args, kwargs, None)


def x_compare_versions__mutmut_orig(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_1(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" and project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_2(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version != "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_3(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "XXunknownXX" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_4(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "UNKNOWN" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_5(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version != "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_6(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "XXunknownXX":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_7(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "UNKNOWN":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_8(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (1, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_9(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "XXunknownXX")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_10(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "UNKNOWN")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_11(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = None
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_12(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(None)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_13(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = None

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_14(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(None)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_15(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver >= proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_16(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (2, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_17(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "XXcli_newerXX")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_18(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "CLI_NEWER")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_19(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver <= proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_20(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (+1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_21(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-2, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_22(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "XXproject_newerXX")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_23(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "PROJECT_NEWER")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_24(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (1, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_25(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "XXmatchXX")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_26(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "MATCH")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "unknown")


def x_compare_versions__mutmut_27(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (1, "unknown")


def x_compare_versions__mutmut_28(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "XXunknownXX")


def x_compare_versions__mutmut_29(cli_version: str, project_version: str) -> tuple[int, MismatchType]:
    """Compare CLI and project versions using semantic versioning.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version

    Returns:
        Tuple of (comparison_result, mismatch_type):
        - comparison_result: -1 (CLI older), 0 (equal), 1 (CLI newer)
        - mismatch_type: Type of mismatch or "match"
    """
    # Handle unknown versions
    if cli_version == "unknown" or project_version == "unknown":
        return (0, "unknown")

    try:
        cli_ver = Version(cli_version)
        proj_ver = Version(project_version)

        if cli_ver > proj_ver:
            return (1, "cli_newer")
        elif cli_ver < proj_ver:
            return (-1, "project_newer")
        else:
            return (0, "match")

    except InvalidVersion:
        # If version parsing fails, treat as unknown
        return (0, "UNKNOWN")

x_compare_versions__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_compare_versions__mutmut_1': x_compare_versions__mutmut_1, 
    'x_compare_versions__mutmut_2': x_compare_versions__mutmut_2, 
    'x_compare_versions__mutmut_3': x_compare_versions__mutmut_3, 
    'x_compare_versions__mutmut_4': x_compare_versions__mutmut_4, 
    'x_compare_versions__mutmut_5': x_compare_versions__mutmut_5, 
    'x_compare_versions__mutmut_6': x_compare_versions__mutmut_6, 
    'x_compare_versions__mutmut_7': x_compare_versions__mutmut_7, 
    'x_compare_versions__mutmut_8': x_compare_versions__mutmut_8, 
    'x_compare_versions__mutmut_9': x_compare_versions__mutmut_9, 
    'x_compare_versions__mutmut_10': x_compare_versions__mutmut_10, 
    'x_compare_versions__mutmut_11': x_compare_versions__mutmut_11, 
    'x_compare_versions__mutmut_12': x_compare_versions__mutmut_12, 
    'x_compare_versions__mutmut_13': x_compare_versions__mutmut_13, 
    'x_compare_versions__mutmut_14': x_compare_versions__mutmut_14, 
    'x_compare_versions__mutmut_15': x_compare_versions__mutmut_15, 
    'x_compare_versions__mutmut_16': x_compare_versions__mutmut_16, 
    'x_compare_versions__mutmut_17': x_compare_versions__mutmut_17, 
    'x_compare_versions__mutmut_18': x_compare_versions__mutmut_18, 
    'x_compare_versions__mutmut_19': x_compare_versions__mutmut_19, 
    'x_compare_versions__mutmut_20': x_compare_versions__mutmut_20, 
    'x_compare_versions__mutmut_21': x_compare_versions__mutmut_21, 
    'x_compare_versions__mutmut_22': x_compare_versions__mutmut_22, 
    'x_compare_versions__mutmut_23': x_compare_versions__mutmut_23, 
    'x_compare_versions__mutmut_24': x_compare_versions__mutmut_24, 
    'x_compare_versions__mutmut_25': x_compare_versions__mutmut_25, 
    'x_compare_versions__mutmut_26': x_compare_versions__mutmut_26, 
    'x_compare_versions__mutmut_27': x_compare_versions__mutmut_27, 
    'x_compare_versions__mutmut_28': x_compare_versions__mutmut_28, 
    'x_compare_versions__mutmut_29': x_compare_versions__mutmut_29
}
x_compare_versions__mutmut_orig.__name__ = 'x_compare_versions'


def format_version_error(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    args = [cli_version, project_version, mismatch_type]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_format_version_error__mutmut_orig, x_format_version_error__mutmut_mutants, args, kwargs, None)


def x_format_version_error__mutmut_orig(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_1(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = None

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_2(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" / 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_3(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "XX━XX" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_4(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 81

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_5(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type != "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_6(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "XXcli_newerXX":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_7(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "CLI_NEWER":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_8(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = None
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_9(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(None)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_10(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = None
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_11(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(None)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_12(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = None
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_13(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") or proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_14(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver > Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_15(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version(None) and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_16(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("XX0.9.0XX") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_17(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver <= Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_18(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version(None)
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_19(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("XX0.9.0XX")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_20(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = None

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_21(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = True

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_22(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type != "project_newer":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_23(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "XXproject_newerXX":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"


def x_format_version_error__mutmut_24(
    cli_version: str,
    project_version: str,
    mismatch_type: MismatchType
) -> str:
    """Format a user-facing error message for version mismatch.

    Args:
        cli_version: Installed CLI version
        project_version: Project's spec-kitty version
        mismatch_type: Type of mismatch

    Returns:
        Formatted error message with resolution instructions
    """
    border = "━" * 80

    if mismatch_type == "cli_newer":
        # Check if this is the critical 0.8.x -> 0.9.x upgrade
        try:
            from packaging.version import Version
            cli_ver = Version(cli_version)
            proj_ver = Version(project_version)
            is_090_upgrade = cli_ver >= Version("0.9.0") and proj_ver < Version("0.9.0")
        except (InvalidVersion, TypeError):
            is_090_upgrade = False

        if is_090_upgrade:
            return f"""
{border}
🚨 CRITICAL: BREAKING CHANGES - Version Mismatch Detected 🚨
{border}

CLI version:     {cli_version}  ← NEWER (v0.9.0+ has BREAKING CHANGES)
Project version: {project_version}  ← OLDER (pre-0.9.0 format)

⚠️  YOU CANNOT USE v0.9.0+ CLI WITH PRE-0.9.0 PROJECTS! ⚠️

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔴 CRITICAL BREAKING CHANGE IN v0.9.0: LANE SYSTEM REDESIGNED 🔴          ║
╚════════════════════════════════════════════════════════════════════════════╝

📂 OLD STRUCTURE (pre-0.9.0):
   kitty-specs/<feature>/tasks/
   ├── planned/WP01.md
   ├── doing/WP02.md
   ├── for_review/WP03.md
   └── done/WP04.md

📂 NEW STRUCTURE (v0.9.0+):
   kitty-specs/<feature>/tasks/
   ├── WP01.md  (with "lane: planned" in frontmatter)
   ├── WP02.md  (with "lane: doing" in frontmatter)
   ├── WP03.md  (with "lane: for_review" in frontmatter)
   └── WP04.md  (with "lane: done" in frontmatter)

⚠️  THIS AFFECTS ALL YOUR HISTORICAL WORK IN kitty-specs/ ⚠️

🔧 REQUIRED ACTION - You MUST upgrade your project:

  spec-kitty upgrade

This will:
  ✅ Migrate ALL features from directory-based to frontmatter-only lanes
  ✅ Move all WP files from subdirectories to flat tasks/ directory
  ✅ Add "lane:" field to frontmatter in all WP files
  ✅ Update .kittify/metadata.yaml to v{cli_version}
  ✅ Remove empty lane subdirectories

🛡️  SAFETY: The upgrade is idempotent and safe to run multiple times.

❌ Commands are BLOCKED until you upgrade to prevent data corruption.

{border}
""".strip()
        else:
            return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your CLI is NEWER than your project.

This means your project templates and scripts are out of date.
Please upgrade your project to match:

  spec-kitty upgrade

This will update your project templates and configuration
to match the installed CLI version.

{border}
""".strip()

    elif mismatch_type == "PROJECT_NEWER":
        return f"""
{border}
❌ ERROR: Version Mismatch Detected
{border}

CLI version:     {cli_version}
Project version: {project_version}

Your project is NEWER than your CLI.

This project was created or upgraded with a newer version
of spec-kitty-cli. Please upgrade your CLI:

  pip install --upgrade spec-kitty-cli

After upgrading, run:

  spec-kitty --version

to verify the update.

{border}
""".strip()

    else:
        return f"Version mismatch: CLI={cli_version}, Project={project_version}"

x_format_version_error__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_format_version_error__mutmut_1': x_format_version_error__mutmut_1, 
    'x_format_version_error__mutmut_2': x_format_version_error__mutmut_2, 
    'x_format_version_error__mutmut_3': x_format_version_error__mutmut_3, 
    'x_format_version_error__mutmut_4': x_format_version_error__mutmut_4, 
    'x_format_version_error__mutmut_5': x_format_version_error__mutmut_5, 
    'x_format_version_error__mutmut_6': x_format_version_error__mutmut_6, 
    'x_format_version_error__mutmut_7': x_format_version_error__mutmut_7, 
    'x_format_version_error__mutmut_8': x_format_version_error__mutmut_8, 
    'x_format_version_error__mutmut_9': x_format_version_error__mutmut_9, 
    'x_format_version_error__mutmut_10': x_format_version_error__mutmut_10, 
    'x_format_version_error__mutmut_11': x_format_version_error__mutmut_11, 
    'x_format_version_error__mutmut_12': x_format_version_error__mutmut_12, 
    'x_format_version_error__mutmut_13': x_format_version_error__mutmut_13, 
    'x_format_version_error__mutmut_14': x_format_version_error__mutmut_14, 
    'x_format_version_error__mutmut_15': x_format_version_error__mutmut_15, 
    'x_format_version_error__mutmut_16': x_format_version_error__mutmut_16, 
    'x_format_version_error__mutmut_17': x_format_version_error__mutmut_17, 
    'x_format_version_error__mutmut_18': x_format_version_error__mutmut_18, 
    'x_format_version_error__mutmut_19': x_format_version_error__mutmut_19, 
    'x_format_version_error__mutmut_20': x_format_version_error__mutmut_20, 
    'x_format_version_error__mutmut_21': x_format_version_error__mutmut_21, 
    'x_format_version_error__mutmut_22': x_format_version_error__mutmut_22, 
    'x_format_version_error__mutmut_23': x_format_version_error__mutmut_23, 
    'x_format_version_error__mutmut_24': x_format_version_error__mutmut_24
}
x_format_version_error__mutmut_orig.__name__ = 'x_format_version_error'


def should_check_version(command_name: str) -> bool:
    args = [command_name]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_should_check_version__mutmut_orig, x_should_check_version__mutmut_mutants, args, kwargs, None)


def x_should_check_version__mutmut_orig(command_name: str) -> bool:
    """Determine if version check is required for a command.

    Args:
        command_name: Name of the command being executed

    Returns:
        True if version check required, False if should skip
    """
    # Commands that skip version check (they create or fix version issues)
    skip_commands = {
        "init",
        "upgrade",
        "version",  # --version flag
        "help",     # --help flag
    }

    return command_name not in skip_commands


def x_should_check_version__mutmut_1(command_name: str) -> bool:
    """Determine if version check is required for a command.

    Args:
        command_name: Name of the command being executed

    Returns:
        True if version check required, False if should skip
    """
    # Commands that skip version check (they create or fix version issues)
    skip_commands = None

    return command_name not in skip_commands


def x_should_check_version__mutmut_2(command_name: str) -> bool:
    """Determine if version check is required for a command.

    Args:
        command_name: Name of the command being executed

    Returns:
        True if version check required, False if should skip
    """
    # Commands that skip version check (they create or fix version issues)
    skip_commands = {
        "XXinitXX",
        "upgrade",
        "version",  # --version flag
        "help",     # --help flag
    }

    return command_name not in skip_commands


def x_should_check_version__mutmut_3(command_name: str) -> bool:
    """Determine if version check is required for a command.

    Args:
        command_name: Name of the command being executed

    Returns:
        True if version check required, False if should skip
    """
    # Commands that skip version check (they create or fix version issues)
    skip_commands = {
        "INIT",
        "upgrade",
        "version",  # --version flag
        "help",     # --help flag
    }

    return command_name not in skip_commands


def x_should_check_version__mutmut_4(command_name: str) -> bool:
    """Determine if version check is required for a command.

    Args:
        command_name: Name of the command being executed

    Returns:
        True if version check required, False if should skip
    """
    # Commands that skip version check (they create or fix version issues)
    skip_commands = {
        "init",
        "XXupgradeXX",
        "version",  # --version flag
        "help",     # --help flag
    }

    return command_name not in skip_commands


def x_should_check_version__mutmut_5(command_name: str) -> bool:
    """Determine if version check is required for a command.

    Args:
        command_name: Name of the command being executed

    Returns:
        True if version check required, False if should skip
    """
    # Commands that skip version check (they create or fix version issues)
    skip_commands = {
        "init",
        "UPGRADE",
        "version",  # --version flag
        "help",     # --help flag
    }

    return command_name not in skip_commands


def x_should_check_version__mutmut_6(command_name: str) -> bool:
    """Determine if version check is required for a command.

    Args:
        command_name: Name of the command being executed

    Returns:
        True if version check required, False if should skip
    """
    # Commands that skip version check (they create or fix version issues)
    skip_commands = {
        "init",
        "upgrade",
        "XXversionXX",  # --version flag
        "help",     # --help flag
    }

    return command_name not in skip_commands


def x_should_check_version__mutmut_7(command_name: str) -> bool:
    """Determine if version check is required for a command.

    Args:
        command_name: Name of the command being executed

    Returns:
        True if version check required, False if should skip
    """
    # Commands that skip version check (they create or fix version issues)
    skip_commands = {
        "init",
        "upgrade",
        "VERSION",  # --version flag
        "help",     # --help flag
    }

    return command_name not in skip_commands


def x_should_check_version__mutmut_8(command_name: str) -> bool:
    """Determine if version check is required for a command.

    Args:
        command_name: Name of the command being executed

    Returns:
        True if version check required, False if should skip
    """
    # Commands that skip version check (they create or fix version issues)
    skip_commands = {
        "init",
        "upgrade",
        "version",  # --version flag
        "XXhelpXX",     # --help flag
    }

    return command_name not in skip_commands


def x_should_check_version__mutmut_9(command_name: str) -> bool:
    """Determine if version check is required for a command.

    Args:
        command_name: Name of the command being executed

    Returns:
        True if version check required, False if should skip
    """
    # Commands that skip version check (they create or fix version issues)
    skip_commands = {
        "init",
        "upgrade",
        "version",  # --version flag
        "HELP",     # --help flag
    }

    return command_name not in skip_commands


def x_should_check_version__mutmut_10(command_name: str) -> bool:
    """Determine if version check is required for a command.

    Args:
        command_name: Name of the command being executed

    Returns:
        True if version check required, False if should skip
    """
    # Commands that skip version check (they create or fix version issues)
    skip_commands = {
        "init",
        "upgrade",
        "version",  # --version flag
        "help",     # --help flag
    }

    return command_name in skip_commands

x_should_check_version__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_should_check_version__mutmut_1': x_should_check_version__mutmut_1, 
    'x_should_check_version__mutmut_2': x_should_check_version__mutmut_2, 
    'x_should_check_version__mutmut_3': x_should_check_version__mutmut_3, 
    'x_should_check_version__mutmut_4': x_should_check_version__mutmut_4, 
    'x_should_check_version__mutmut_5': x_should_check_version__mutmut_5, 
    'x_should_check_version__mutmut_6': x_should_check_version__mutmut_6, 
    'x_should_check_version__mutmut_7': x_should_check_version__mutmut_7, 
    'x_should_check_version__mutmut_8': x_should_check_version__mutmut_8, 
    'x_should_check_version__mutmut_9': x_should_check_version__mutmut_9, 
    'x_should_check_version__mutmut_10': x_should_check_version__mutmut_10
}
x_should_check_version__mutmut_orig.__name__ = 'x_should_check_version'


__all__ = [
    "get_cli_version",
    "get_project_version",
    "compare_versions",
    "format_version_error",
    "should_check_version",
    "MismatchType",
]
