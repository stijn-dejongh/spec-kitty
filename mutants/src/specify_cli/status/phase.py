from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

VALID_PHASES = (0, 1, 2)
DEFAULT_PHASE = 1
DEFAULT_PHASE_SOURCE = "built-in default (Phase 1: dual-write)"
MAX_PHASE_01X = 2
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


def resolve_phase(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    args = [repo_root, feature_slug]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_resolve_phase__mutmut_orig, x_resolve_phase__mutmut_mutants, args, kwargs, None)


def x_resolve_phase__mutmut_orig(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_1(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = None
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_2(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(None, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_3(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, None)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_4(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_5(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, )
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_6(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_7(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = None
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_8(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = None
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_9(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = None
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_10(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(None)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_11(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_12(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = None
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_13(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = None
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_14(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "XXglobal default from .kittify/config.yamlXX"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_15(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "GLOBAL DEFAULT FROM .KITTIFY/CONFIG.YAML"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_16(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = None
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_17(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = None

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_18(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) or phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_19(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(None) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_20(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase >= MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_21(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info(None, phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_22(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", None, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_23(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, None)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_24(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info(phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_25(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_26(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, )
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_27(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("XXPhase %d capped to %d on 0.1x branchXX", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_28(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_29(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("PHASE %D CAPPED TO %D ON 0.1X BRANCH", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_30(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = None
        source = f"{source} (capped to {MAX_PHASE_01X} on 0.1x)"

    return phase, source


def x_resolve_phase__mutmut_31(repo_root: Path, feature_slug: str) -> tuple[int, str]:
    """Resolve active status phase. Precedence: meta.json > config.yaml > default.

    On 0.1x branch, caps at MAX_PHASE_01X. Returns (phase, source_description).
    """
    meta_phase = _read_meta_phase(repo_root, feature_slug)
    if meta_phase is not None:
        phase = meta_phase
        source = f"meta.json override for {feature_slug}"
    else:
        config_phase = _read_config_phase(repo_root)
        if config_phase is not None:
            phase = config_phase
            source = "global default from .kittify/config.yaml"
        else:
            phase = DEFAULT_PHASE
            source = DEFAULT_PHASE_SOURCE

    if is_01x_branch(repo_root) and phase > MAX_PHASE_01X:
        logger.info("Phase %d capped to %d on 0.1x branch", phase, MAX_PHASE_01X)
        phase = MAX_PHASE_01X
        source = None

    return phase, source

x_resolve_phase__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_resolve_phase__mutmut_1': x_resolve_phase__mutmut_1, 
    'x_resolve_phase__mutmut_2': x_resolve_phase__mutmut_2, 
    'x_resolve_phase__mutmut_3': x_resolve_phase__mutmut_3, 
    'x_resolve_phase__mutmut_4': x_resolve_phase__mutmut_4, 
    'x_resolve_phase__mutmut_5': x_resolve_phase__mutmut_5, 
    'x_resolve_phase__mutmut_6': x_resolve_phase__mutmut_6, 
    'x_resolve_phase__mutmut_7': x_resolve_phase__mutmut_7, 
    'x_resolve_phase__mutmut_8': x_resolve_phase__mutmut_8, 
    'x_resolve_phase__mutmut_9': x_resolve_phase__mutmut_9, 
    'x_resolve_phase__mutmut_10': x_resolve_phase__mutmut_10, 
    'x_resolve_phase__mutmut_11': x_resolve_phase__mutmut_11, 
    'x_resolve_phase__mutmut_12': x_resolve_phase__mutmut_12, 
    'x_resolve_phase__mutmut_13': x_resolve_phase__mutmut_13, 
    'x_resolve_phase__mutmut_14': x_resolve_phase__mutmut_14, 
    'x_resolve_phase__mutmut_15': x_resolve_phase__mutmut_15, 
    'x_resolve_phase__mutmut_16': x_resolve_phase__mutmut_16, 
    'x_resolve_phase__mutmut_17': x_resolve_phase__mutmut_17, 
    'x_resolve_phase__mutmut_18': x_resolve_phase__mutmut_18, 
    'x_resolve_phase__mutmut_19': x_resolve_phase__mutmut_19, 
    'x_resolve_phase__mutmut_20': x_resolve_phase__mutmut_20, 
    'x_resolve_phase__mutmut_21': x_resolve_phase__mutmut_21, 
    'x_resolve_phase__mutmut_22': x_resolve_phase__mutmut_22, 
    'x_resolve_phase__mutmut_23': x_resolve_phase__mutmut_23, 
    'x_resolve_phase__mutmut_24': x_resolve_phase__mutmut_24, 
    'x_resolve_phase__mutmut_25': x_resolve_phase__mutmut_25, 
    'x_resolve_phase__mutmut_26': x_resolve_phase__mutmut_26, 
    'x_resolve_phase__mutmut_27': x_resolve_phase__mutmut_27, 
    'x_resolve_phase__mutmut_28': x_resolve_phase__mutmut_28, 
    'x_resolve_phase__mutmut_29': x_resolve_phase__mutmut_29, 
    'x_resolve_phase__mutmut_30': x_resolve_phase__mutmut_30, 
    'x_resolve_phase__mutmut_31': x_resolve_phase__mutmut_31
}
x_resolve_phase__mutmut_orig.__name__ = 'x_resolve_phase'


def _read_meta_phase(repo_root: Path, feature_slug: str) -> int | None:
    args = [repo_root, feature_slug]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__read_meta_phase__mutmut_orig, x__read_meta_phase__mutmut_mutants, args, kwargs, None)


def x__read_meta_phase__mutmut_orig(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_1(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = None
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_2(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug * "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_3(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" * feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_4(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root * "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_5(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "XXkitty-specsXX" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_6(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "KITTY-SPECS" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_7(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "XXmeta.jsonXX"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_8(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "META.JSON"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_9(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_10(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = None
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_11(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(None)
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_12(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding=None))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_13(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="XXutf-8XX"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_14(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="UTF-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_15(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = None
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_16(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get(None)
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_17(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("XXstatus_phaseXX")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_18(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("STATUS_PHASE")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_19(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is not None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_20(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = None
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_21(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(None)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_22(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_23(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(None, phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_24(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", None, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_25(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, None)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_26(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_27(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_28(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, )
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_29(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("XXInvalid status_phase %d in %s, ignoringXX", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_30(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_31(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("INVALID STATUS_PHASE %D IN %S, IGNORING", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_32(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning(None, meta_path, exc)
        return None


def x__read_meta_phase__mutmut_33(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", None, exc)
        return None


def x__read_meta_phase__mutmut_34(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, None)
        return None


def x__read_meta_phase__mutmut_35(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning(meta_path, exc)
        return None


def x__read_meta_phase__mutmut_36(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", exc)
        return None


def x__read_meta_phase__mutmut_37(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to read status_phase from %s: %s", meta_path, )
        return None


def x__read_meta_phase__mutmut_38(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("XXFailed to read status_phase from %s: %sXX", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_39(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("failed to read status_phase from %s: %s", meta_path, exc)
        return None


def x__read_meta_phase__mutmut_40(repo_root: Path, feature_slug: str) -> int | None:
    """Read status_phase from feature meta.json. Returns None if not set or invalid."""
    meta_path = repo_root / "kitty-specs" / feature_slug / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = data.get("status_phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning("Invalid status_phase %d in %s, ignoring", phase, meta_path)
            return None
        return phase
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("FAILED TO READ STATUS_PHASE FROM %S: %S", meta_path, exc)
        return None

x__read_meta_phase__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__read_meta_phase__mutmut_1': x__read_meta_phase__mutmut_1, 
    'x__read_meta_phase__mutmut_2': x__read_meta_phase__mutmut_2, 
    'x__read_meta_phase__mutmut_3': x__read_meta_phase__mutmut_3, 
    'x__read_meta_phase__mutmut_4': x__read_meta_phase__mutmut_4, 
    'x__read_meta_phase__mutmut_5': x__read_meta_phase__mutmut_5, 
    'x__read_meta_phase__mutmut_6': x__read_meta_phase__mutmut_6, 
    'x__read_meta_phase__mutmut_7': x__read_meta_phase__mutmut_7, 
    'x__read_meta_phase__mutmut_8': x__read_meta_phase__mutmut_8, 
    'x__read_meta_phase__mutmut_9': x__read_meta_phase__mutmut_9, 
    'x__read_meta_phase__mutmut_10': x__read_meta_phase__mutmut_10, 
    'x__read_meta_phase__mutmut_11': x__read_meta_phase__mutmut_11, 
    'x__read_meta_phase__mutmut_12': x__read_meta_phase__mutmut_12, 
    'x__read_meta_phase__mutmut_13': x__read_meta_phase__mutmut_13, 
    'x__read_meta_phase__mutmut_14': x__read_meta_phase__mutmut_14, 
    'x__read_meta_phase__mutmut_15': x__read_meta_phase__mutmut_15, 
    'x__read_meta_phase__mutmut_16': x__read_meta_phase__mutmut_16, 
    'x__read_meta_phase__mutmut_17': x__read_meta_phase__mutmut_17, 
    'x__read_meta_phase__mutmut_18': x__read_meta_phase__mutmut_18, 
    'x__read_meta_phase__mutmut_19': x__read_meta_phase__mutmut_19, 
    'x__read_meta_phase__mutmut_20': x__read_meta_phase__mutmut_20, 
    'x__read_meta_phase__mutmut_21': x__read_meta_phase__mutmut_21, 
    'x__read_meta_phase__mutmut_22': x__read_meta_phase__mutmut_22, 
    'x__read_meta_phase__mutmut_23': x__read_meta_phase__mutmut_23, 
    'x__read_meta_phase__mutmut_24': x__read_meta_phase__mutmut_24, 
    'x__read_meta_phase__mutmut_25': x__read_meta_phase__mutmut_25, 
    'x__read_meta_phase__mutmut_26': x__read_meta_phase__mutmut_26, 
    'x__read_meta_phase__mutmut_27': x__read_meta_phase__mutmut_27, 
    'x__read_meta_phase__mutmut_28': x__read_meta_phase__mutmut_28, 
    'x__read_meta_phase__mutmut_29': x__read_meta_phase__mutmut_29, 
    'x__read_meta_phase__mutmut_30': x__read_meta_phase__mutmut_30, 
    'x__read_meta_phase__mutmut_31': x__read_meta_phase__mutmut_31, 
    'x__read_meta_phase__mutmut_32': x__read_meta_phase__mutmut_32, 
    'x__read_meta_phase__mutmut_33': x__read_meta_phase__mutmut_33, 
    'x__read_meta_phase__mutmut_34': x__read_meta_phase__mutmut_34, 
    'x__read_meta_phase__mutmut_35': x__read_meta_phase__mutmut_35, 
    'x__read_meta_phase__mutmut_36': x__read_meta_phase__mutmut_36, 
    'x__read_meta_phase__mutmut_37': x__read_meta_phase__mutmut_37, 
    'x__read_meta_phase__mutmut_38': x__read_meta_phase__mutmut_38, 
    'x__read_meta_phase__mutmut_39': x__read_meta_phase__mutmut_39, 
    'x__read_meta_phase__mutmut_40': x__read_meta_phase__mutmut_40
}
x__read_meta_phase__mutmut_orig.__name__ = 'x__read_meta_phase'


def _read_config_phase(repo_root: Path) -> int | None:
    args = [repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__read_config_phase__mutmut_orig, x__read_config_phase__mutmut_mutants, args, kwargs, None)


def x__read_config_phase__mutmut_orig(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_1(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = None
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_2(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" * "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_3(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root * ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_4(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / "XX.kittifyXX" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_5(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".KITTIFY" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_6(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "XXconfig.yamlXX"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_7(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "CONFIG.YAML"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_8(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_9(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = None
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_10(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = None
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_11(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(None)
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_12(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding=None))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_13(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="XXutf-8XX"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_14(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="UTF-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_15(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_16(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = None
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_17(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get(None)
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_18(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("XXstatusXX")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_19(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("STATUS")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_20(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_21(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = None
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_22(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get(None)
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_23(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("XXphaseXX")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_24(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("PHASE")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_25(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is not None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_26(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = None
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_27(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(None)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_28(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_29(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                None, phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_30(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", None, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_31(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, None
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_32(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_33(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_34(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_35(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "XXInvalid status.phase %d in %s, ignoringXX", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_36(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_37(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "INVALID STATUS.PHASE %D IN %S, IGNORING", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_38(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning(None, config_path, exc)
        return None


def x__read_config_phase__mutmut_39(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", None, exc)
        return None


def x__read_config_phase__mutmut_40(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, None)
        return None


def x__read_config_phase__mutmut_41(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning(config_path, exc)
        return None


def x__read_config_phase__mutmut_42(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", exc)
        return None


def x__read_config_phase__mutmut_43(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("Failed to read status.phase from %s: %s", config_path, )
        return None


def x__read_config_phase__mutmut_44(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("XXFailed to read status.phase from %s: %sXX", config_path, exc)
        return None


def x__read_config_phase__mutmut_45(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("failed to read status.phase from %s: %s", config_path, exc)
        return None


def x__read_config_phase__mutmut_46(repo_root: Path) -> int | None:
    """Read status.phase from .kittify/config.yaml. Returns None if not set."""
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        status_section = data.get("status")
        if not isinstance(status_section, dict):
            return None
        raw = status_section.get("phase")
        if raw is None:
            return None
        phase = int(raw)
        if phase not in VALID_PHASES:
            logger.warning(
                "Invalid status.phase %d in %s, ignoring", phase, config_path
            )
            return None
        return phase
    except Exception as exc:
        logger.warning("FAILED TO READ STATUS.PHASE FROM %S: %S", config_path, exc)
        return None

x__read_config_phase__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__read_config_phase__mutmut_1': x__read_config_phase__mutmut_1, 
    'x__read_config_phase__mutmut_2': x__read_config_phase__mutmut_2, 
    'x__read_config_phase__mutmut_3': x__read_config_phase__mutmut_3, 
    'x__read_config_phase__mutmut_4': x__read_config_phase__mutmut_4, 
    'x__read_config_phase__mutmut_5': x__read_config_phase__mutmut_5, 
    'x__read_config_phase__mutmut_6': x__read_config_phase__mutmut_6, 
    'x__read_config_phase__mutmut_7': x__read_config_phase__mutmut_7, 
    'x__read_config_phase__mutmut_8': x__read_config_phase__mutmut_8, 
    'x__read_config_phase__mutmut_9': x__read_config_phase__mutmut_9, 
    'x__read_config_phase__mutmut_10': x__read_config_phase__mutmut_10, 
    'x__read_config_phase__mutmut_11': x__read_config_phase__mutmut_11, 
    'x__read_config_phase__mutmut_12': x__read_config_phase__mutmut_12, 
    'x__read_config_phase__mutmut_13': x__read_config_phase__mutmut_13, 
    'x__read_config_phase__mutmut_14': x__read_config_phase__mutmut_14, 
    'x__read_config_phase__mutmut_15': x__read_config_phase__mutmut_15, 
    'x__read_config_phase__mutmut_16': x__read_config_phase__mutmut_16, 
    'x__read_config_phase__mutmut_17': x__read_config_phase__mutmut_17, 
    'x__read_config_phase__mutmut_18': x__read_config_phase__mutmut_18, 
    'x__read_config_phase__mutmut_19': x__read_config_phase__mutmut_19, 
    'x__read_config_phase__mutmut_20': x__read_config_phase__mutmut_20, 
    'x__read_config_phase__mutmut_21': x__read_config_phase__mutmut_21, 
    'x__read_config_phase__mutmut_22': x__read_config_phase__mutmut_22, 
    'x__read_config_phase__mutmut_23': x__read_config_phase__mutmut_23, 
    'x__read_config_phase__mutmut_24': x__read_config_phase__mutmut_24, 
    'x__read_config_phase__mutmut_25': x__read_config_phase__mutmut_25, 
    'x__read_config_phase__mutmut_26': x__read_config_phase__mutmut_26, 
    'x__read_config_phase__mutmut_27': x__read_config_phase__mutmut_27, 
    'x__read_config_phase__mutmut_28': x__read_config_phase__mutmut_28, 
    'x__read_config_phase__mutmut_29': x__read_config_phase__mutmut_29, 
    'x__read_config_phase__mutmut_30': x__read_config_phase__mutmut_30, 
    'x__read_config_phase__mutmut_31': x__read_config_phase__mutmut_31, 
    'x__read_config_phase__mutmut_32': x__read_config_phase__mutmut_32, 
    'x__read_config_phase__mutmut_33': x__read_config_phase__mutmut_33, 
    'x__read_config_phase__mutmut_34': x__read_config_phase__mutmut_34, 
    'x__read_config_phase__mutmut_35': x__read_config_phase__mutmut_35, 
    'x__read_config_phase__mutmut_36': x__read_config_phase__mutmut_36, 
    'x__read_config_phase__mutmut_37': x__read_config_phase__mutmut_37, 
    'x__read_config_phase__mutmut_38': x__read_config_phase__mutmut_38, 
    'x__read_config_phase__mutmut_39': x__read_config_phase__mutmut_39, 
    'x__read_config_phase__mutmut_40': x__read_config_phase__mutmut_40, 
    'x__read_config_phase__mutmut_41': x__read_config_phase__mutmut_41, 
    'x__read_config_phase__mutmut_42': x__read_config_phase__mutmut_42, 
    'x__read_config_phase__mutmut_43': x__read_config_phase__mutmut_43, 
    'x__read_config_phase__mutmut_44': x__read_config_phase__mutmut_44, 
    'x__read_config_phase__mutmut_45': x__read_config_phase__mutmut_45, 
    'x__read_config_phase__mutmut_46': x__read_config_phase__mutmut_46
}
x__read_config_phase__mutmut_orig.__name__ = 'x__read_config_phase'


def is_01x_branch(repo_root: Path) -> bool:
    args = [repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_is_01x_branch__mutmut_orig, x_is_01x_branch__mutmut_mutants, args, kwargs, None)


def x_is_01x_branch__mutmut_orig(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_1(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = None
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_2(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            None,
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_3(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_4(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_5(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=None,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_6(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding=None,
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_7(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors=None,
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_8(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=None,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_9(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_10(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_11(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_12(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_13(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_14(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_15(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_16(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["XXgitXX", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_17(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["GIT", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_18(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "XXrev-parseXX", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_19(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "REV-PARSE", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_20(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "XX--abbrev-refXX", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_21(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--ABBREV-REF", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_22(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "XXHEADXX"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_23(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "head"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_24(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_25(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=False,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_26(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_27(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="UTF-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_28(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_29(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_30(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=6,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_31(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode == 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_32(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 1:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_33(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return True
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_34(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = None
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_35(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") and branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_36(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith(None) or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_37(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("XX2.XX") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_38(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch != "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_39(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "XX2.xXX":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_40(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.X":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_41(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return True
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_42(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith(None):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_43(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("XX034-XX"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_44(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return True
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_45(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return False
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def x_is_01x_branch__mutmut_46(repo_root: Path) -> bool:
    """Check if current git branch is on the 0.1x line (main, release/*, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return False
        branch = result.stdout.strip()
        if branch.startswith("2.") or branch == "2.x":
            return False
        if branch.startswith("034-"):
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return True

x_is_01x_branch__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_is_01x_branch__mutmut_1': x_is_01x_branch__mutmut_1, 
    'x_is_01x_branch__mutmut_2': x_is_01x_branch__mutmut_2, 
    'x_is_01x_branch__mutmut_3': x_is_01x_branch__mutmut_3, 
    'x_is_01x_branch__mutmut_4': x_is_01x_branch__mutmut_4, 
    'x_is_01x_branch__mutmut_5': x_is_01x_branch__mutmut_5, 
    'x_is_01x_branch__mutmut_6': x_is_01x_branch__mutmut_6, 
    'x_is_01x_branch__mutmut_7': x_is_01x_branch__mutmut_7, 
    'x_is_01x_branch__mutmut_8': x_is_01x_branch__mutmut_8, 
    'x_is_01x_branch__mutmut_9': x_is_01x_branch__mutmut_9, 
    'x_is_01x_branch__mutmut_10': x_is_01x_branch__mutmut_10, 
    'x_is_01x_branch__mutmut_11': x_is_01x_branch__mutmut_11, 
    'x_is_01x_branch__mutmut_12': x_is_01x_branch__mutmut_12, 
    'x_is_01x_branch__mutmut_13': x_is_01x_branch__mutmut_13, 
    'x_is_01x_branch__mutmut_14': x_is_01x_branch__mutmut_14, 
    'x_is_01x_branch__mutmut_15': x_is_01x_branch__mutmut_15, 
    'x_is_01x_branch__mutmut_16': x_is_01x_branch__mutmut_16, 
    'x_is_01x_branch__mutmut_17': x_is_01x_branch__mutmut_17, 
    'x_is_01x_branch__mutmut_18': x_is_01x_branch__mutmut_18, 
    'x_is_01x_branch__mutmut_19': x_is_01x_branch__mutmut_19, 
    'x_is_01x_branch__mutmut_20': x_is_01x_branch__mutmut_20, 
    'x_is_01x_branch__mutmut_21': x_is_01x_branch__mutmut_21, 
    'x_is_01x_branch__mutmut_22': x_is_01x_branch__mutmut_22, 
    'x_is_01x_branch__mutmut_23': x_is_01x_branch__mutmut_23, 
    'x_is_01x_branch__mutmut_24': x_is_01x_branch__mutmut_24, 
    'x_is_01x_branch__mutmut_25': x_is_01x_branch__mutmut_25, 
    'x_is_01x_branch__mutmut_26': x_is_01x_branch__mutmut_26, 
    'x_is_01x_branch__mutmut_27': x_is_01x_branch__mutmut_27, 
    'x_is_01x_branch__mutmut_28': x_is_01x_branch__mutmut_28, 
    'x_is_01x_branch__mutmut_29': x_is_01x_branch__mutmut_29, 
    'x_is_01x_branch__mutmut_30': x_is_01x_branch__mutmut_30, 
    'x_is_01x_branch__mutmut_31': x_is_01x_branch__mutmut_31, 
    'x_is_01x_branch__mutmut_32': x_is_01x_branch__mutmut_32, 
    'x_is_01x_branch__mutmut_33': x_is_01x_branch__mutmut_33, 
    'x_is_01x_branch__mutmut_34': x_is_01x_branch__mutmut_34, 
    'x_is_01x_branch__mutmut_35': x_is_01x_branch__mutmut_35, 
    'x_is_01x_branch__mutmut_36': x_is_01x_branch__mutmut_36, 
    'x_is_01x_branch__mutmut_37': x_is_01x_branch__mutmut_37, 
    'x_is_01x_branch__mutmut_38': x_is_01x_branch__mutmut_38, 
    'x_is_01x_branch__mutmut_39': x_is_01x_branch__mutmut_39, 
    'x_is_01x_branch__mutmut_40': x_is_01x_branch__mutmut_40, 
    'x_is_01x_branch__mutmut_41': x_is_01x_branch__mutmut_41, 
    'x_is_01x_branch__mutmut_42': x_is_01x_branch__mutmut_42, 
    'x_is_01x_branch__mutmut_43': x_is_01x_branch__mutmut_43, 
    'x_is_01x_branch__mutmut_44': x_is_01x_branch__mutmut_44, 
    'x_is_01x_branch__mutmut_45': x_is_01x_branch__mutmut_45, 
    'x_is_01x_branch__mutmut_46': x_is_01x_branch__mutmut_46
}
x_is_01x_branch__mutmut_orig.__name__ = 'x_is_01x_branch'
