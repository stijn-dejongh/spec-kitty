"""Strictness policy system for glossary enforcement.

This module implements the strictness policy system with three enforcement modes
(off/medium/max) and four-tier precedence resolution (global → mission → step → runtime).
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING

import ruamel.yaml

if TYPE_CHECKING:
    from .models import SemanticConflict, Severity
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


class Strictness(StrEnum):
    """Glossary enforcement strictness levels.

    - OFF: No enforcement, generation always proceeds
    - MEDIUM: Warn broadly, block only high-severity conflicts
    - MAX: Block any unresolved conflict regardless of severity
    """

    OFF = "off"
    MEDIUM = "medium"
    MAX = "max"


def resolve_strictness(
    global_default: Strictness = Strictness.MEDIUM,
    mission_override: Strictness | None = None,
    step_override: Strictness | None = None,
    runtime_override: Strictness | None = None,
) -> Strictness:
    args = [global_default, mission_override, step_override, runtime_override]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_resolve_strictness__mutmut_orig, x_resolve_strictness__mutmut_mutants, args, kwargs, None)


def x_resolve_strictness__mutmut_orig(
    global_default: Strictness = Strictness.MEDIUM,
    mission_override: Strictness | None = None,
    step_override: Strictness | None = None,
    runtime_override: Strictness | None = None,
) -> Strictness:
    """Resolve effective strictness using precedence chain.

    Precedence (highest to lowest):
    1. Runtime override (CLI --strictness flag)
    2. Step metadata (glossary_check_strictness in step definition)
    3. Mission config (mission.yaml default)
    4. Global default (Strictness.MEDIUM)

    Args:
        global_default: Global default strictness (typically from config.yaml)
        mission_override: Mission-level strictness (from mission.yaml)
        step_override: Step-level strictness (from step metadata)
        runtime_override: Runtime override (from CLI flag)

    Returns:
        The effective strictness mode to apply.

    Examples:
        >>> resolve_strictness()  # All None
        <Strictness.MEDIUM: 'medium'>

        >>> resolve_strictness(runtime_override=Strictness.OFF)
        <Strictness.OFF: 'off'>

        >>> resolve_strictness(
        ...     mission_override=Strictness.MAX,
        ...     step_override=Strictness.OFF,
        ... )
        <Strictness.OFF: 'off'>  # Step wins over mission
    """
    # Apply precedence: most specific wins
    if runtime_override is not None:
        return runtime_override
    if step_override is not None:
        return step_override
    if mission_override is not None:
        return mission_override
    return global_default


def x_resolve_strictness__mutmut_1(
    global_default: Strictness = Strictness.MEDIUM,
    mission_override: Strictness | None = None,
    step_override: Strictness | None = None,
    runtime_override: Strictness | None = None,
) -> Strictness:
    """Resolve effective strictness using precedence chain.

    Precedence (highest to lowest):
    1. Runtime override (CLI --strictness flag)
    2. Step metadata (glossary_check_strictness in step definition)
    3. Mission config (mission.yaml default)
    4. Global default (Strictness.MEDIUM)

    Args:
        global_default: Global default strictness (typically from config.yaml)
        mission_override: Mission-level strictness (from mission.yaml)
        step_override: Step-level strictness (from step metadata)
        runtime_override: Runtime override (from CLI flag)

    Returns:
        The effective strictness mode to apply.

    Examples:
        >>> resolve_strictness()  # All None
        <Strictness.MEDIUM: 'medium'>

        >>> resolve_strictness(runtime_override=Strictness.OFF)
        <Strictness.OFF: 'off'>

        >>> resolve_strictness(
        ...     mission_override=Strictness.MAX,
        ...     step_override=Strictness.OFF,
        ... )
        <Strictness.OFF: 'off'>  # Step wins over mission
    """
    # Apply precedence: most specific wins
    if runtime_override is None:
        return runtime_override
    if step_override is not None:
        return step_override
    if mission_override is not None:
        return mission_override
    return global_default


def x_resolve_strictness__mutmut_2(
    global_default: Strictness = Strictness.MEDIUM,
    mission_override: Strictness | None = None,
    step_override: Strictness | None = None,
    runtime_override: Strictness | None = None,
) -> Strictness:
    """Resolve effective strictness using precedence chain.

    Precedence (highest to lowest):
    1. Runtime override (CLI --strictness flag)
    2. Step metadata (glossary_check_strictness in step definition)
    3. Mission config (mission.yaml default)
    4. Global default (Strictness.MEDIUM)

    Args:
        global_default: Global default strictness (typically from config.yaml)
        mission_override: Mission-level strictness (from mission.yaml)
        step_override: Step-level strictness (from step metadata)
        runtime_override: Runtime override (from CLI flag)

    Returns:
        The effective strictness mode to apply.

    Examples:
        >>> resolve_strictness()  # All None
        <Strictness.MEDIUM: 'medium'>

        >>> resolve_strictness(runtime_override=Strictness.OFF)
        <Strictness.OFF: 'off'>

        >>> resolve_strictness(
        ...     mission_override=Strictness.MAX,
        ...     step_override=Strictness.OFF,
        ... )
        <Strictness.OFF: 'off'>  # Step wins over mission
    """
    # Apply precedence: most specific wins
    if runtime_override is not None:
        return runtime_override
    if step_override is None:
        return step_override
    if mission_override is not None:
        return mission_override
    return global_default


def x_resolve_strictness__mutmut_3(
    global_default: Strictness = Strictness.MEDIUM,
    mission_override: Strictness | None = None,
    step_override: Strictness | None = None,
    runtime_override: Strictness | None = None,
) -> Strictness:
    """Resolve effective strictness using precedence chain.

    Precedence (highest to lowest):
    1. Runtime override (CLI --strictness flag)
    2. Step metadata (glossary_check_strictness in step definition)
    3. Mission config (mission.yaml default)
    4. Global default (Strictness.MEDIUM)

    Args:
        global_default: Global default strictness (typically from config.yaml)
        mission_override: Mission-level strictness (from mission.yaml)
        step_override: Step-level strictness (from step metadata)
        runtime_override: Runtime override (from CLI flag)

    Returns:
        The effective strictness mode to apply.

    Examples:
        >>> resolve_strictness()  # All None
        <Strictness.MEDIUM: 'medium'>

        >>> resolve_strictness(runtime_override=Strictness.OFF)
        <Strictness.OFF: 'off'>

        >>> resolve_strictness(
        ...     mission_override=Strictness.MAX,
        ...     step_override=Strictness.OFF,
        ... )
        <Strictness.OFF: 'off'>  # Step wins over mission
    """
    # Apply precedence: most specific wins
    if runtime_override is not None:
        return runtime_override
    if step_override is not None:
        return step_override
    if mission_override is None:
        return mission_override
    return global_default

x_resolve_strictness__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_resolve_strictness__mutmut_1': x_resolve_strictness__mutmut_1, 
    'x_resolve_strictness__mutmut_2': x_resolve_strictness__mutmut_2, 
    'x_resolve_strictness__mutmut_3': x_resolve_strictness__mutmut_3
}
x_resolve_strictness__mutmut_orig.__name__ = 'x_resolve_strictness'


def load_global_strictness(repo_root: Path) -> Strictness:
    args = [repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_load_global_strictness__mutmut_orig, x_load_global_strictness__mutmut_mutants, args, kwargs, None)


def x_load_global_strictness__mutmut_orig(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_1(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = None
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_2(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" * "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_3(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root * ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_4(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / "XX.kittifyXX" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_5(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".KITTIFY" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_6(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "XXconfig.yamlXX"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_7(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "CONFIG.YAML"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_8(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_9(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = None
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_10(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ=None)
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_11(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="XXsafeXX")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_12(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="SAFE")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_13(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = None

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_14(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(None)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_15(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config or "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_16(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config or "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_17(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "XXglossaryXX" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_18(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "GLOSSARY" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_19(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" not in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_20(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "XXstrictnessXX" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_21(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "STRICTNESS" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_22(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" not in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_23(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["XXglossaryXX"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_24(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["GLOSSARY"]:
            value = config["glossary"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_25(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = None
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_26(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["XXglossaryXX"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_27(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["GLOSSARY"]["strictness"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_28(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["XXstrictnessXX"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_29(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["STRICTNESS"]
            return Strictness(value)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM


def x_load_global_strictness__mutmut_30(repo_root: Path) -> Strictness:
    """Load global strictness from .kittify/config.yaml.

    This function reads the global strictness setting from the project config.
    If the config file doesn't exist, is malformed, or has no strictness setting,
    returns the safe default (Strictness.MEDIUM).

    Args:
        repo_root: Path to repository root

    Returns:
        Global strictness setting, or Strictness.MEDIUM if not configured

    Examples:
        >>> from pathlib import Path
        >>> load_global_strictness(Path("/nonexistent"))
        <Strictness.MEDIUM: 'medium'>
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return Strictness.MEDIUM

    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        with config_path.open() as f:
            config = yaml.load(f)

        if config and "glossary" in config and "strictness" in config["glossary"]:
            value = config["glossary"]["strictness"]
            return Strictness(None)
    except Exception:
        # Invalid config (malformed YAML, invalid enum value, etc.)
        # Return safe default rather than crashing
        pass

    return Strictness.MEDIUM

x_load_global_strictness__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_load_global_strictness__mutmut_1': x_load_global_strictness__mutmut_1, 
    'x_load_global_strictness__mutmut_2': x_load_global_strictness__mutmut_2, 
    'x_load_global_strictness__mutmut_3': x_load_global_strictness__mutmut_3, 
    'x_load_global_strictness__mutmut_4': x_load_global_strictness__mutmut_4, 
    'x_load_global_strictness__mutmut_5': x_load_global_strictness__mutmut_5, 
    'x_load_global_strictness__mutmut_6': x_load_global_strictness__mutmut_6, 
    'x_load_global_strictness__mutmut_7': x_load_global_strictness__mutmut_7, 
    'x_load_global_strictness__mutmut_8': x_load_global_strictness__mutmut_8, 
    'x_load_global_strictness__mutmut_9': x_load_global_strictness__mutmut_9, 
    'x_load_global_strictness__mutmut_10': x_load_global_strictness__mutmut_10, 
    'x_load_global_strictness__mutmut_11': x_load_global_strictness__mutmut_11, 
    'x_load_global_strictness__mutmut_12': x_load_global_strictness__mutmut_12, 
    'x_load_global_strictness__mutmut_13': x_load_global_strictness__mutmut_13, 
    'x_load_global_strictness__mutmut_14': x_load_global_strictness__mutmut_14, 
    'x_load_global_strictness__mutmut_15': x_load_global_strictness__mutmut_15, 
    'x_load_global_strictness__mutmut_16': x_load_global_strictness__mutmut_16, 
    'x_load_global_strictness__mutmut_17': x_load_global_strictness__mutmut_17, 
    'x_load_global_strictness__mutmut_18': x_load_global_strictness__mutmut_18, 
    'x_load_global_strictness__mutmut_19': x_load_global_strictness__mutmut_19, 
    'x_load_global_strictness__mutmut_20': x_load_global_strictness__mutmut_20, 
    'x_load_global_strictness__mutmut_21': x_load_global_strictness__mutmut_21, 
    'x_load_global_strictness__mutmut_22': x_load_global_strictness__mutmut_22, 
    'x_load_global_strictness__mutmut_23': x_load_global_strictness__mutmut_23, 
    'x_load_global_strictness__mutmut_24': x_load_global_strictness__mutmut_24, 
    'x_load_global_strictness__mutmut_25': x_load_global_strictness__mutmut_25, 
    'x_load_global_strictness__mutmut_26': x_load_global_strictness__mutmut_26, 
    'x_load_global_strictness__mutmut_27': x_load_global_strictness__mutmut_27, 
    'x_load_global_strictness__mutmut_28': x_load_global_strictness__mutmut_28, 
    'x_load_global_strictness__mutmut_29': x_load_global_strictness__mutmut_29, 
    'x_load_global_strictness__mutmut_30': x_load_global_strictness__mutmut_30
}
x_load_global_strictness__mutmut_orig.__name__ = 'x_load_global_strictness'


def should_block(
    strictness: Strictness,
    conflicts: list["SemanticConflict"],
) -> bool:
    args = [strictness, conflicts]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_should_block__mutmut_orig, x_should_block__mutmut_mutants, args, kwargs, None)


def x_should_block__mutmut_orig(
    strictness: Strictness,
    conflicts: list["SemanticConflict"],
) -> bool:
    """Determine if generation should be blocked.

    Blocking rules:
    - OFF: Never block (return False regardless of conflicts)
    - MEDIUM: Block only if ANY high-severity conflict exists
    - MAX: Block if ANY conflict exists (regardless of severity)

    Args:
        strictness: The effective strictness mode
        conflicts: List of detected semantic conflicts

    Returns:
        True if generation should be blocked, False otherwise

    Examples:
        >>> from specify_cli.glossary.models import SemanticConflict, Severity, TermSurface, ConflictType
        >>> high_conflict = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.AMBIGUOUS,
        ...     severity=Severity.HIGH,
        ...     confidence=0.9,
        ...     candidate_senses=[],
        ...     context="test",
        ... )

        >>> should_block(Strictness.OFF, [high_conflict])
        False

        >>> should_block(Strictness.MEDIUM, [high_conflict])
        True

        >>> should_block(Strictness.MAX, [high_conflict])
        True
    """
    if strictness == Strictness.OFF:
        return False

    if strictness == Strictness.MAX:
        return len(conflicts) > 0

    # MEDIUM mode: block only on high-severity.
    # Unknown/invalid severities are treated as HIGH for safety --
    # an unrecognised severity must not silently pass through.
    # Import inside function to avoid circular dependency
    from .models import Severity

    _known_severities = set(Severity)
    return any(
        c.severity == Severity.HIGH or c.severity not in _known_severities
        for c in conflicts
    )


def x_should_block__mutmut_1(
    strictness: Strictness,
    conflicts: list["SemanticConflict"],
) -> bool:
    """Determine if generation should be blocked.

    Blocking rules:
    - OFF: Never block (return False regardless of conflicts)
    - MEDIUM: Block only if ANY high-severity conflict exists
    - MAX: Block if ANY conflict exists (regardless of severity)

    Args:
        strictness: The effective strictness mode
        conflicts: List of detected semantic conflicts

    Returns:
        True if generation should be blocked, False otherwise

    Examples:
        >>> from specify_cli.glossary.models import SemanticConflict, Severity, TermSurface, ConflictType
        >>> high_conflict = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.AMBIGUOUS,
        ...     severity=Severity.HIGH,
        ...     confidence=0.9,
        ...     candidate_senses=[],
        ...     context="test",
        ... )

        >>> should_block(Strictness.OFF, [high_conflict])
        False

        >>> should_block(Strictness.MEDIUM, [high_conflict])
        True

        >>> should_block(Strictness.MAX, [high_conflict])
        True
    """
    if strictness != Strictness.OFF:
        return False

    if strictness == Strictness.MAX:
        return len(conflicts) > 0

    # MEDIUM mode: block only on high-severity.
    # Unknown/invalid severities are treated as HIGH for safety --
    # an unrecognised severity must not silently pass through.
    # Import inside function to avoid circular dependency
    from .models import Severity

    _known_severities = set(Severity)
    return any(
        c.severity == Severity.HIGH or c.severity not in _known_severities
        for c in conflicts
    )


def x_should_block__mutmut_2(
    strictness: Strictness,
    conflicts: list["SemanticConflict"],
) -> bool:
    """Determine if generation should be blocked.

    Blocking rules:
    - OFF: Never block (return False regardless of conflicts)
    - MEDIUM: Block only if ANY high-severity conflict exists
    - MAX: Block if ANY conflict exists (regardless of severity)

    Args:
        strictness: The effective strictness mode
        conflicts: List of detected semantic conflicts

    Returns:
        True if generation should be blocked, False otherwise

    Examples:
        >>> from specify_cli.glossary.models import SemanticConflict, Severity, TermSurface, ConflictType
        >>> high_conflict = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.AMBIGUOUS,
        ...     severity=Severity.HIGH,
        ...     confidence=0.9,
        ...     candidate_senses=[],
        ...     context="test",
        ... )

        >>> should_block(Strictness.OFF, [high_conflict])
        False

        >>> should_block(Strictness.MEDIUM, [high_conflict])
        True

        >>> should_block(Strictness.MAX, [high_conflict])
        True
    """
    if strictness == Strictness.OFF:
        return True

    if strictness == Strictness.MAX:
        return len(conflicts) > 0

    # MEDIUM mode: block only on high-severity.
    # Unknown/invalid severities are treated as HIGH for safety --
    # an unrecognised severity must not silently pass through.
    # Import inside function to avoid circular dependency
    from .models import Severity

    _known_severities = set(Severity)
    return any(
        c.severity == Severity.HIGH or c.severity not in _known_severities
        for c in conflicts
    )


def x_should_block__mutmut_3(
    strictness: Strictness,
    conflicts: list["SemanticConflict"],
) -> bool:
    """Determine if generation should be blocked.

    Blocking rules:
    - OFF: Never block (return False regardless of conflicts)
    - MEDIUM: Block only if ANY high-severity conflict exists
    - MAX: Block if ANY conflict exists (regardless of severity)

    Args:
        strictness: The effective strictness mode
        conflicts: List of detected semantic conflicts

    Returns:
        True if generation should be blocked, False otherwise

    Examples:
        >>> from specify_cli.glossary.models import SemanticConflict, Severity, TermSurface, ConflictType
        >>> high_conflict = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.AMBIGUOUS,
        ...     severity=Severity.HIGH,
        ...     confidence=0.9,
        ...     candidate_senses=[],
        ...     context="test",
        ... )

        >>> should_block(Strictness.OFF, [high_conflict])
        False

        >>> should_block(Strictness.MEDIUM, [high_conflict])
        True

        >>> should_block(Strictness.MAX, [high_conflict])
        True
    """
    if strictness == Strictness.OFF:
        return False

    if strictness != Strictness.MAX:
        return len(conflicts) > 0

    # MEDIUM mode: block only on high-severity.
    # Unknown/invalid severities are treated as HIGH for safety --
    # an unrecognised severity must not silently pass through.
    # Import inside function to avoid circular dependency
    from .models import Severity

    _known_severities = set(Severity)
    return any(
        c.severity == Severity.HIGH or c.severity not in _known_severities
        for c in conflicts
    )


def x_should_block__mutmut_4(
    strictness: Strictness,
    conflicts: list["SemanticConflict"],
) -> bool:
    """Determine if generation should be blocked.

    Blocking rules:
    - OFF: Never block (return False regardless of conflicts)
    - MEDIUM: Block only if ANY high-severity conflict exists
    - MAX: Block if ANY conflict exists (regardless of severity)

    Args:
        strictness: The effective strictness mode
        conflicts: List of detected semantic conflicts

    Returns:
        True if generation should be blocked, False otherwise

    Examples:
        >>> from specify_cli.glossary.models import SemanticConflict, Severity, TermSurface, ConflictType
        >>> high_conflict = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.AMBIGUOUS,
        ...     severity=Severity.HIGH,
        ...     confidence=0.9,
        ...     candidate_senses=[],
        ...     context="test",
        ... )

        >>> should_block(Strictness.OFF, [high_conflict])
        False

        >>> should_block(Strictness.MEDIUM, [high_conflict])
        True

        >>> should_block(Strictness.MAX, [high_conflict])
        True
    """
    if strictness == Strictness.OFF:
        return False

    if strictness == Strictness.MAX:
        return len(conflicts) >= 0

    # MEDIUM mode: block only on high-severity.
    # Unknown/invalid severities are treated as HIGH for safety --
    # an unrecognised severity must not silently pass through.
    # Import inside function to avoid circular dependency
    from .models import Severity

    _known_severities = set(Severity)
    return any(
        c.severity == Severity.HIGH or c.severity not in _known_severities
        for c in conflicts
    )


def x_should_block__mutmut_5(
    strictness: Strictness,
    conflicts: list["SemanticConflict"],
) -> bool:
    """Determine if generation should be blocked.

    Blocking rules:
    - OFF: Never block (return False regardless of conflicts)
    - MEDIUM: Block only if ANY high-severity conflict exists
    - MAX: Block if ANY conflict exists (regardless of severity)

    Args:
        strictness: The effective strictness mode
        conflicts: List of detected semantic conflicts

    Returns:
        True if generation should be blocked, False otherwise

    Examples:
        >>> from specify_cli.glossary.models import SemanticConflict, Severity, TermSurface, ConflictType
        >>> high_conflict = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.AMBIGUOUS,
        ...     severity=Severity.HIGH,
        ...     confidence=0.9,
        ...     candidate_senses=[],
        ...     context="test",
        ... )

        >>> should_block(Strictness.OFF, [high_conflict])
        False

        >>> should_block(Strictness.MEDIUM, [high_conflict])
        True

        >>> should_block(Strictness.MAX, [high_conflict])
        True
    """
    if strictness == Strictness.OFF:
        return False

    if strictness == Strictness.MAX:
        return len(conflicts) > 1

    # MEDIUM mode: block only on high-severity.
    # Unknown/invalid severities are treated as HIGH for safety --
    # an unrecognised severity must not silently pass through.
    # Import inside function to avoid circular dependency
    from .models import Severity

    _known_severities = set(Severity)
    return any(
        c.severity == Severity.HIGH or c.severity not in _known_severities
        for c in conflicts
    )


def x_should_block__mutmut_6(
    strictness: Strictness,
    conflicts: list["SemanticConflict"],
) -> bool:
    """Determine if generation should be blocked.

    Blocking rules:
    - OFF: Never block (return False regardless of conflicts)
    - MEDIUM: Block only if ANY high-severity conflict exists
    - MAX: Block if ANY conflict exists (regardless of severity)

    Args:
        strictness: The effective strictness mode
        conflicts: List of detected semantic conflicts

    Returns:
        True if generation should be blocked, False otherwise

    Examples:
        >>> from specify_cli.glossary.models import SemanticConflict, Severity, TermSurface, ConflictType
        >>> high_conflict = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.AMBIGUOUS,
        ...     severity=Severity.HIGH,
        ...     confidence=0.9,
        ...     candidate_senses=[],
        ...     context="test",
        ... )

        >>> should_block(Strictness.OFF, [high_conflict])
        False

        >>> should_block(Strictness.MEDIUM, [high_conflict])
        True

        >>> should_block(Strictness.MAX, [high_conflict])
        True
    """
    if strictness == Strictness.OFF:
        return False

    if strictness == Strictness.MAX:
        return len(conflicts) > 0

    # MEDIUM mode: block only on high-severity.
    # Unknown/invalid severities are treated as HIGH for safety --
    # an unrecognised severity must not silently pass through.
    # Import inside function to avoid circular dependency
    from .models import Severity

    _known_severities = None
    return any(
        c.severity == Severity.HIGH or c.severity not in _known_severities
        for c in conflicts
    )


def x_should_block__mutmut_7(
    strictness: Strictness,
    conflicts: list["SemanticConflict"],
) -> bool:
    """Determine if generation should be blocked.

    Blocking rules:
    - OFF: Never block (return False regardless of conflicts)
    - MEDIUM: Block only if ANY high-severity conflict exists
    - MAX: Block if ANY conflict exists (regardless of severity)

    Args:
        strictness: The effective strictness mode
        conflicts: List of detected semantic conflicts

    Returns:
        True if generation should be blocked, False otherwise

    Examples:
        >>> from specify_cli.glossary.models import SemanticConflict, Severity, TermSurface, ConflictType
        >>> high_conflict = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.AMBIGUOUS,
        ...     severity=Severity.HIGH,
        ...     confidence=0.9,
        ...     candidate_senses=[],
        ...     context="test",
        ... )

        >>> should_block(Strictness.OFF, [high_conflict])
        False

        >>> should_block(Strictness.MEDIUM, [high_conflict])
        True

        >>> should_block(Strictness.MAX, [high_conflict])
        True
    """
    if strictness == Strictness.OFF:
        return False

    if strictness == Strictness.MAX:
        return len(conflicts) > 0

    # MEDIUM mode: block only on high-severity.
    # Unknown/invalid severities are treated as HIGH for safety --
    # an unrecognised severity must not silently pass through.
    # Import inside function to avoid circular dependency
    from .models import Severity

    _known_severities = set(None)
    return any(
        c.severity == Severity.HIGH or c.severity not in _known_severities
        for c in conflicts
    )


def x_should_block__mutmut_8(
    strictness: Strictness,
    conflicts: list["SemanticConflict"],
) -> bool:
    """Determine if generation should be blocked.

    Blocking rules:
    - OFF: Never block (return False regardless of conflicts)
    - MEDIUM: Block only if ANY high-severity conflict exists
    - MAX: Block if ANY conflict exists (regardless of severity)

    Args:
        strictness: The effective strictness mode
        conflicts: List of detected semantic conflicts

    Returns:
        True if generation should be blocked, False otherwise

    Examples:
        >>> from specify_cli.glossary.models import SemanticConflict, Severity, TermSurface, ConflictType
        >>> high_conflict = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.AMBIGUOUS,
        ...     severity=Severity.HIGH,
        ...     confidence=0.9,
        ...     candidate_senses=[],
        ...     context="test",
        ... )

        >>> should_block(Strictness.OFF, [high_conflict])
        False

        >>> should_block(Strictness.MEDIUM, [high_conflict])
        True

        >>> should_block(Strictness.MAX, [high_conflict])
        True
    """
    if strictness == Strictness.OFF:
        return False

    if strictness == Strictness.MAX:
        return len(conflicts) > 0

    # MEDIUM mode: block only on high-severity.
    # Unknown/invalid severities are treated as HIGH for safety --
    # an unrecognised severity must not silently pass through.
    # Import inside function to avoid circular dependency
    from .models import Severity

    _known_severities = set(Severity)
    return any(
        None
    )


def x_should_block__mutmut_9(
    strictness: Strictness,
    conflicts: list["SemanticConflict"],
) -> bool:
    """Determine if generation should be blocked.

    Blocking rules:
    - OFF: Never block (return False regardless of conflicts)
    - MEDIUM: Block only if ANY high-severity conflict exists
    - MAX: Block if ANY conflict exists (regardless of severity)

    Args:
        strictness: The effective strictness mode
        conflicts: List of detected semantic conflicts

    Returns:
        True if generation should be blocked, False otherwise

    Examples:
        >>> from specify_cli.glossary.models import SemanticConflict, Severity, TermSurface, ConflictType
        >>> high_conflict = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.AMBIGUOUS,
        ...     severity=Severity.HIGH,
        ...     confidence=0.9,
        ...     candidate_senses=[],
        ...     context="test",
        ... )

        >>> should_block(Strictness.OFF, [high_conflict])
        False

        >>> should_block(Strictness.MEDIUM, [high_conflict])
        True

        >>> should_block(Strictness.MAX, [high_conflict])
        True
    """
    if strictness == Strictness.OFF:
        return False

    if strictness == Strictness.MAX:
        return len(conflicts) > 0

    # MEDIUM mode: block only on high-severity.
    # Unknown/invalid severities are treated as HIGH for safety --
    # an unrecognised severity must not silently pass through.
    # Import inside function to avoid circular dependency
    from .models import Severity

    _known_severities = set(Severity)
    return any(
        c.severity == Severity.HIGH and c.severity not in _known_severities
        for c in conflicts
    )


def x_should_block__mutmut_10(
    strictness: Strictness,
    conflicts: list["SemanticConflict"],
) -> bool:
    """Determine if generation should be blocked.

    Blocking rules:
    - OFF: Never block (return False regardless of conflicts)
    - MEDIUM: Block only if ANY high-severity conflict exists
    - MAX: Block if ANY conflict exists (regardless of severity)

    Args:
        strictness: The effective strictness mode
        conflicts: List of detected semantic conflicts

    Returns:
        True if generation should be blocked, False otherwise

    Examples:
        >>> from specify_cli.glossary.models import SemanticConflict, Severity, TermSurface, ConflictType
        >>> high_conflict = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.AMBIGUOUS,
        ...     severity=Severity.HIGH,
        ...     confidence=0.9,
        ...     candidate_senses=[],
        ...     context="test",
        ... )

        >>> should_block(Strictness.OFF, [high_conflict])
        False

        >>> should_block(Strictness.MEDIUM, [high_conflict])
        True

        >>> should_block(Strictness.MAX, [high_conflict])
        True
    """
    if strictness == Strictness.OFF:
        return False

    if strictness == Strictness.MAX:
        return len(conflicts) > 0

    # MEDIUM mode: block only on high-severity.
    # Unknown/invalid severities are treated as HIGH for safety --
    # an unrecognised severity must not silently pass through.
    # Import inside function to avoid circular dependency
    from .models import Severity

    _known_severities = set(Severity)
    return any(
        c.severity != Severity.HIGH or c.severity not in _known_severities
        for c in conflicts
    )


def x_should_block__mutmut_11(
    strictness: Strictness,
    conflicts: list["SemanticConflict"],
) -> bool:
    """Determine if generation should be blocked.

    Blocking rules:
    - OFF: Never block (return False regardless of conflicts)
    - MEDIUM: Block only if ANY high-severity conflict exists
    - MAX: Block if ANY conflict exists (regardless of severity)

    Args:
        strictness: The effective strictness mode
        conflicts: List of detected semantic conflicts

    Returns:
        True if generation should be blocked, False otherwise

    Examples:
        >>> from specify_cli.glossary.models import SemanticConflict, Severity, TermSurface, ConflictType
        >>> high_conflict = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.AMBIGUOUS,
        ...     severity=Severity.HIGH,
        ...     confidence=0.9,
        ...     candidate_senses=[],
        ...     context="test",
        ... )

        >>> should_block(Strictness.OFF, [high_conflict])
        False

        >>> should_block(Strictness.MEDIUM, [high_conflict])
        True

        >>> should_block(Strictness.MAX, [high_conflict])
        True
    """
    if strictness == Strictness.OFF:
        return False

    if strictness == Strictness.MAX:
        return len(conflicts) > 0

    # MEDIUM mode: block only on high-severity.
    # Unknown/invalid severities are treated as HIGH for safety --
    # an unrecognised severity must not silently pass through.
    # Import inside function to avoid circular dependency
    from .models import Severity

    _known_severities = set(Severity)
    return any(
        c.severity == Severity.HIGH or c.severity in _known_severities
        for c in conflicts
    )

x_should_block__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_should_block__mutmut_1': x_should_block__mutmut_1, 
    'x_should_block__mutmut_2': x_should_block__mutmut_2, 
    'x_should_block__mutmut_3': x_should_block__mutmut_3, 
    'x_should_block__mutmut_4': x_should_block__mutmut_4, 
    'x_should_block__mutmut_5': x_should_block__mutmut_5, 
    'x_should_block__mutmut_6': x_should_block__mutmut_6, 
    'x_should_block__mutmut_7': x_should_block__mutmut_7, 
    'x_should_block__mutmut_8': x_should_block__mutmut_8, 
    'x_should_block__mutmut_9': x_should_block__mutmut_9, 
    'x_should_block__mutmut_10': x_should_block__mutmut_10, 
    'x_should_block__mutmut_11': x_should_block__mutmut_11
}
x_should_block__mutmut_orig.__name__ = 'x_should_block'


def categorize_conflicts(
    conflicts: list["SemanticConflict"],
) -> dict["Severity", list["SemanticConflict"]]:
    args = [conflicts]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_categorize_conflicts__mutmut_orig, x_categorize_conflicts__mutmut_mutants, args, kwargs, None)


def x_categorize_conflicts__mutmut_orig(
    conflicts: list["SemanticConflict"],
) -> dict["Severity", list["SemanticConflict"]]:
    """Group conflicts by severity level for reporting.

    This helper function organizes conflicts into severity buckets,
    making it easier to generate reports and determine blocking behavior.

    Args:
        conflicts: List of detected semantic conflicts

    Returns:
        Dict mapping severity to list of conflicts at that level.
        All three severity levels (LOW, MEDIUM, HIGH) are present as keys,
        even if some have empty lists.

    Examples:
        >>> from specify_cli.glossary.models import (
        ...     SemanticConflict, Severity, TermSurface, ConflictType
        ... )
        >>> low = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.UNKNOWN,
        ...     severity=Severity.LOW,
        ...     confidence=0.3,
        ...     candidate_senses=[],
        ...     context="test",
        ... )
        >>> categorized = categorize_conflicts([low])
        >>> list(categorized.keys())
        [<Severity.LOW: 'low'>, <Severity.MEDIUM: 'medium'>, <Severity.HIGH: 'high'>]
        >>> len(categorized[Severity.LOW])
        1
    """
    # Import inside function to avoid circular dependency
    from .models import Severity

    categorized: dict[Severity, list["SemanticConflict"]] = {
        Severity.LOW: [],
        Severity.MEDIUM: [],
        Severity.HIGH: [],
    }

    for conflict in conflicts:
        # Unknown/invalid severities are bucketed as HIGH for safety.
        # This prevents KeyError and ensures unrecognised severities
        # never silently pass through as non-blocking.
        bucket = conflict.severity if conflict.severity in categorized else Severity.HIGH
        categorized[bucket].append(conflict)

    return categorized


def x_categorize_conflicts__mutmut_1(
    conflicts: list["SemanticConflict"],
) -> dict["Severity", list["SemanticConflict"]]:
    """Group conflicts by severity level for reporting.

    This helper function organizes conflicts into severity buckets,
    making it easier to generate reports and determine blocking behavior.

    Args:
        conflicts: List of detected semantic conflicts

    Returns:
        Dict mapping severity to list of conflicts at that level.
        All three severity levels (LOW, MEDIUM, HIGH) are present as keys,
        even if some have empty lists.

    Examples:
        >>> from specify_cli.glossary.models import (
        ...     SemanticConflict, Severity, TermSurface, ConflictType
        ... )
        >>> low = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.UNKNOWN,
        ...     severity=Severity.LOW,
        ...     confidence=0.3,
        ...     candidate_senses=[],
        ...     context="test",
        ... )
        >>> categorized = categorize_conflicts([low])
        >>> list(categorized.keys())
        [<Severity.LOW: 'low'>, <Severity.MEDIUM: 'medium'>, <Severity.HIGH: 'high'>]
        >>> len(categorized[Severity.LOW])
        1
    """
    # Import inside function to avoid circular dependency
    from .models import Severity

    categorized: dict[Severity, list["SemanticConflict"]] = None

    for conflict in conflicts:
        # Unknown/invalid severities are bucketed as HIGH for safety.
        # This prevents KeyError and ensures unrecognised severities
        # never silently pass through as non-blocking.
        bucket = conflict.severity if conflict.severity in categorized else Severity.HIGH
        categorized[bucket].append(conflict)

    return categorized


def x_categorize_conflicts__mutmut_2(
    conflicts: list["SemanticConflict"],
) -> dict["Severity", list["SemanticConflict"]]:
    """Group conflicts by severity level for reporting.

    This helper function organizes conflicts into severity buckets,
    making it easier to generate reports and determine blocking behavior.

    Args:
        conflicts: List of detected semantic conflicts

    Returns:
        Dict mapping severity to list of conflicts at that level.
        All three severity levels (LOW, MEDIUM, HIGH) are present as keys,
        even if some have empty lists.

    Examples:
        >>> from specify_cli.glossary.models import (
        ...     SemanticConflict, Severity, TermSurface, ConflictType
        ... )
        >>> low = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.UNKNOWN,
        ...     severity=Severity.LOW,
        ...     confidence=0.3,
        ...     candidate_senses=[],
        ...     context="test",
        ... )
        >>> categorized = categorize_conflicts([low])
        >>> list(categorized.keys())
        [<Severity.LOW: 'low'>, <Severity.MEDIUM: 'medium'>, <Severity.HIGH: 'high'>]
        >>> len(categorized[Severity.LOW])
        1
    """
    # Import inside function to avoid circular dependency
    from .models import Severity

    categorized: dict[Severity, list["SemanticConflict"]] = {
        Severity.LOW: [],
        Severity.MEDIUM: [],
        Severity.HIGH: [],
    }

    for conflict in conflicts:
        # Unknown/invalid severities are bucketed as HIGH for safety.
        # This prevents KeyError and ensures unrecognised severities
        # never silently pass through as non-blocking.
        bucket = None
        categorized[bucket].append(conflict)

    return categorized


def x_categorize_conflicts__mutmut_3(
    conflicts: list["SemanticConflict"],
) -> dict["Severity", list["SemanticConflict"]]:
    """Group conflicts by severity level for reporting.

    This helper function organizes conflicts into severity buckets,
    making it easier to generate reports and determine blocking behavior.

    Args:
        conflicts: List of detected semantic conflicts

    Returns:
        Dict mapping severity to list of conflicts at that level.
        All three severity levels (LOW, MEDIUM, HIGH) are present as keys,
        even if some have empty lists.

    Examples:
        >>> from specify_cli.glossary.models import (
        ...     SemanticConflict, Severity, TermSurface, ConflictType
        ... )
        >>> low = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.UNKNOWN,
        ...     severity=Severity.LOW,
        ...     confidence=0.3,
        ...     candidate_senses=[],
        ...     context="test",
        ... )
        >>> categorized = categorize_conflicts([low])
        >>> list(categorized.keys())
        [<Severity.LOW: 'low'>, <Severity.MEDIUM: 'medium'>, <Severity.HIGH: 'high'>]
        >>> len(categorized[Severity.LOW])
        1
    """
    # Import inside function to avoid circular dependency
    from .models import Severity

    categorized: dict[Severity, list["SemanticConflict"]] = {
        Severity.LOW: [],
        Severity.MEDIUM: [],
        Severity.HIGH: [],
    }

    for conflict in conflicts:
        # Unknown/invalid severities are bucketed as HIGH for safety.
        # This prevents KeyError and ensures unrecognised severities
        # never silently pass through as non-blocking.
        bucket = conflict.severity if conflict.severity not in categorized else Severity.HIGH
        categorized[bucket].append(conflict)

    return categorized


def x_categorize_conflicts__mutmut_4(
    conflicts: list["SemanticConflict"],
) -> dict["Severity", list["SemanticConflict"]]:
    """Group conflicts by severity level for reporting.

    This helper function organizes conflicts into severity buckets,
    making it easier to generate reports and determine blocking behavior.

    Args:
        conflicts: List of detected semantic conflicts

    Returns:
        Dict mapping severity to list of conflicts at that level.
        All three severity levels (LOW, MEDIUM, HIGH) are present as keys,
        even if some have empty lists.

    Examples:
        >>> from specify_cli.glossary.models import (
        ...     SemanticConflict, Severity, TermSurface, ConflictType
        ... )
        >>> low = SemanticConflict(
        ...     term=TermSurface(surface_text="test"),
        ...     conflict_type=ConflictType.UNKNOWN,
        ...     severity=Severity.LOW,
        ...     confidence=0.3,
        ...     candidate_senses=[],
        ...     context="test",
        ... )
        >>> categorized = categorize_conflicts([low])
        >>> list(categorized.keys())
        [<Severity.LOW: 'low'>, <Severity.MEDIUM: 'medium'>, <Severity.HIGH: 'high'>]
        >>> len(categorized[Severity.LOW])
        1
    """
    # Import inside function to avoid circular dependency
    from .models import Severity

    categorized: dict[Severity, list["SemanticConflict"]] = {
        Severity.LOW: [],
        Severity.MEDIUM: [],
        Severity.HIGH: [],
    }

    for conflict in conflicts:
        # Unknown/invalid severities are bucketed as HIGH for safety.
        # This prevents KeyError and ensures unrecognised severities
        # never silently pass through as non-blocking.
        bucket = conflict.severity if conflict.severity in categorized else Severity.HIGH
        categorized[bucket].append(None)

    return categorized

x_categorize_conflicts__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_categorize_conflicts__mutmut_1': x_categorize_conflicts__mutmut_1, 
    'x_categorize_conflicts__mutmut_2': x_categorize_conflicts__mutmut_2, 
    'x_categorize_conflicts__mutmut_3': x_categorize_conflicts__mutmut_3, 
    'x_categorize_conflicts__mutmut_4': x_categorize_conflicts__mutmut_4
}
x_categorize_conflicts__mutmut_orig.__name__ = 'x_categorize_conflicts'
