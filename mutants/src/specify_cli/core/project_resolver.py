"""Project path resolution helpers for Spec Kitty."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from rich.console import Console

from specify_cli.core.config import DEFAULT_MISSION_KEY

ConsoleType = Console | None
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


def _resolve_console(console: ConsoleType) -> Console:
    args = [console]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__resolve_console__mutmut_orig, x__resolve_console__mutmut_mutants, args, kwargs, None)


def x__resolve_console__mutmut_orig(console: ConsoleType) -> Console:
    return console if console is not None else Console()


def x__resolve_console__mutmut_1(console: ConsoleType) -> Console:
    return console if console is None else Console()

x__resolve_console__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__resolve_console__mutmut_1': x__resolve_console__mutmut_1
}
x__resolve_console__mutmut_orig.__name__ = 'x__resolve_console'


def locate_project_root(start: Path | None = None) -> Optional[Path]:
    args = [start]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_locate_project_root__mutmut_orig, x_locate_project_root__mutmut_mutants, args, kwargs, None)


def x_locate_project_root__mutmut_orig(start: Path | None = None) -> Optional[Path]:
    """Walk upwards from *start* (or CWD) to find the directory that owns .kittify."""
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".kittify").is_dir():
            return candidate
    return None


def x_locate_project_root__mutmut_1(start: Path | None = None) -> Optional[Path]:
    """Walk upwards from *start* (or CWD) to find the directory that owns .kittify."""
    current = None
    for candidate in [current, *current.parents]:
        if (candidate / ".kittify").is_dir():
            return candidate
    return None


def x_locate_project_root__mutmut_2(start: Path | None = None) -> Optional[Path]:
    """Walk upwards from *start* (or CWD) to find the directory that owns .kittify."""
    current = (start and Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".kittify").is_dir():
            return candidate
    return None


def x_locate_project_root__mutmut_3(start: Path | None = None) -> Optional[Path]:
    """Walk upwards from *start* (or CWD) to find the directory that owns .kittify."""
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate * ".kittify").is_dir():
            return candidate
    return None


def x_locate_project_root__mutmut_4(start: Path | None = None) -> Optional[Path]:
    """Walk upwards from *start* (or CWD) to find the directory that owns .kittify."""
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "XX.kittifyXX").is_dir():
            return candidate
    return None


def x_locate_project_root__mutmut_5(start: Path | None = None) -> Optional[Path]:
    """Walk upwards from *start* (or CWD) to find the directory that owns .kittify."""
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".KITTIFY").is_dir():
            return candidate
    return None

x_locate_project_root__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_locate_project_root__mutmut_1': x_locate_project_root__mutmut_1, 
    'x_locate_project_root__mutmut_2': x_locate_project_root__mutmut_2, 
    'x_locate_project_root__mutmut_3': x_locate_project_root__mutmut_3, 
    'x_locate_project_root__mutmut_4': x_locate_project_root__mutmut_4, 
    'x_locate_project_root__mutmut_5': x_locate_project_root__mutmut_5
}
x_locate_project_root__mutmut_orig.__name__ = 'x_locate_project_root'


def resolve_template_path(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    args = [project_root, mission_key, template_subpath]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_resolve_template_path__mutmut_orig, x_resolve_template_path__mutmut_mutants, args, kwargs, None)


def x_resolve_template_path__mutmut_orig(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_1(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = None
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_2(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(None)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_3(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = None

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_4(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" * subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_5(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key * "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_6(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" * mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_7(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" * "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_8(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root * ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_9(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / "XX.kittifyXX" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_10(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".KITTIFY" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_11(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "XXmissionsXX" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_12(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "MISSIONS" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_13(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "XXtemplatesXX" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_14(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "TEMPLATES" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_15(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" * subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_16(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" * "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_17(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root * ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_18(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / "XX.kittifyXX" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_19(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".KITTIFY" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_20(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "XXtemplatesXX" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_21(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "TEMPLATES" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_22(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = None
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_23(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(None)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_24(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" * subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_25(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key * "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_26(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" * mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_27(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home * "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_28(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "XXmissionsXX" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_29(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "MISSIONS" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_30(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "XXtemplatesXX" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_31(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "TEMPLATES" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_32(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(None)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_33(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" * subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_34(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home * "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_35(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "XXtemplatesXX" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_36(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "TEMPLATES" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_37(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(None)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_38(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "templates" * subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_39(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root * "templates" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_40(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "XXtemplatesXX" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def x_resolve_template_path__mutmut_41(project_root: Path, mission_key: str, template_subpath: str | Path) -> Optional[Path]:
    """Resolve a template path through a 5-tier precedence chain.

    Resolution order:
    1. Project mission: .kittify/missions/{key}/templates/{subpath}
    2. Project generic: .kittify/templates/{subpath}
    3. Global mission: ~/.kittify/missions/{key}/templates/{subpath}
    4. Global generic: ~/.kittify/templates/{subpath}
    5. Legacy fallback: templates/{subpath} (project root)

    Args:
        project_root: Root of the user project containing ``.kittify/``.
        mission_key: Mission key (e.g. ``"software-dev"``).
        template_subpath: Relative template path (e.g. ``"spec-template.md"``).

    Returns:
        Path to the resolved template, or None if not found at any tier.
    """
    from specify_cli.runtime.home import get_kittify_home

    subpath = Path(template_subpath)
    candidates = [
        # 1. Project mission-specific
        project_root / ".kittify" / "missions" / mission_key / "templates" / subpath,
        # 2. Project generic
        project_root / ".kittify" / "templates" / subpath,
    ]

    # 3. Global mission-specific + 4. Global generic
    try:
        global_home = get_kittify_home()
        candidates.append(global_home / "missions" / mission_key / "templates" / subpath)
        candidates.append(global_home / "templates" / subpath)
    except RuntimeError:
        pass

    # 5. Legacy project root fallback
    candidates.append(project_root / "TEMPLATES" / subpath)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None

x_resolve_template_path__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_resolve_template_path__mutmut_1': x_resolve_template_path__mutmut_1, 
    'x_resolve_template_path__mutmut_2': x_resolve_template_path__mutmut_2, 
    'x_resolve_template_path__mutmut_3': x_resolve_template_path__mutmut_3, 
    'x_resolve_template_path__mutmut_4': x_resolve_template_path__mutmut_4, 
    'x_resolve_template_path__mutmut_5': x_resolve_template_path__mutmut_5, 
    'x_resolve_template_path__mutmut_6': x_resolve_template_path__mutmut_6, 
    'x_resolve_template_path__mutmut_7': x_resolve_template_path__mutmut_7, 
    'x_resolve_template_path__mutmut_8': x_resolve_template_path__mutmut_8, 
    'x_resolve_template_path__mutmut_9': x_resolve_template_path__mutmut_9, 
    'x_resolve_template_path__mutmut_10': x_resolve_template_path__mutmut_10, 
    'x_resolve_template_path__mutmut_11': x_resolve_template_path__mutmut_11, 
    'x_resolve_template_path__mutmut_12': x_resolve_template_path__mutmut_12, 
    'x_resolve_template_path__mutmut_13': x_resolve_template_path__mutmut_13, 
    'x_resolve_template_path__mutmut_14': x_resolve_template_path__mutmut_14, 
    'x_resolve_template_path__mutmut_15': x_resolve_template_path__mutmut_15, 
    'x_resolve_template_path__mutmut_16': x_resolve_template_path__mutmut_16, 
    'x_resolve_template_path__mutmut_17': x_resolve_template_path__mutmut_17, 
    'x_resolve_template_path__mutmut_18': x_resolve_template_path__mutmut_18, 
    'x_resolve_template_path__mutmut_19': x_resolve_template_path__mutmut_19, 
    'x_resolve_template_path__mutmut_20': x_resolve_template_path__mutmut_20, 
    'x_resolve_template_path__mutmut_21': x_resolve_template_path__mutmut_21, 
    'x_resolve_template_path__mutmut_22': x_resolve_template_path__mutmut_22, 
    'x_resolve_template_path__mutmut_23': x_resolve_template_path__mutmut_23, 
    'x_resolve_template_path__mutmut_24': x_resolve_template_path__mutmut_24, 
    'x_resolve_template_path__mutmut_25': x_resolve_template_path__mutmut_25, 
    'x_resolve_template_path__mutmut_26': x_resolve_template_path__mutmut_26, 
    'x_resolve_template_path__mutmut_27': x_resolve_template_path__mutmut_27, 
    'x_resolve_template_path__mutmut_28': x_resolve_template_path__mutmut_28, 
    'x_resolve_template_path__mutmut_29': x_resolve_template_path__mutmut_29, 
    'x_resolve_template_path__mutmut_30': x_resolve_template_path__mutmut_30, 
    'x_resolve_template_path__mutmut_31': x_resolve_template_path__mutmut_31, 
    'x_resolve_template_path__mutmut_32': x_resolve_template_path__mutmut_32, 
    'x_resolve_template_path__mutmut_33': x_resolve_template_path__mutmut_33, 
    'x_resolve_template_path__mutmut_34': x_resolve_template_path__mutmut_34, 
    'x_resolve_template_path__mutmut_35': x_resolve_template_path__mutmut_35, 
    'x_resolve_template_path__mutmut_36': x_resolve_template_path__mutmut_36, 
    'x_resolve_template_path__mutmut_37': x_resolve_template_path__mutmut_37, 
    'x_resolve_template_path__mutmut_38': x_resolve_template_path__mutmut_38, 
    'x_resolve_template_path__mutmut_39': x_resolve_template_path__mutmut_39, 
    'x_resolve_template_path__mutmut_40': x_resolve_template_path__mutmut_40, 
    'x_resolve_template_path__mutmut_41': x_resolve_template_path__mutmut_41
}
x_resolve_template_path__mutmut_orig.__name__ = 'x_resolve_template_path'


def resolve_worktree_aware_feature_dir(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    args = [repo_root, feature_slug, cwd, console]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_resolve_worktree_aware_feature_dir__mutmut_orig, x_resolve_worktree_aware_feature_dir__mutmut_mutants, args, kwargs, None)


def x_resolve_worktree_aware_feature_dir__mutmut_orig(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_1(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = None
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_2(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(None)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_3(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = None

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_4(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd and Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_5(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = None
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_6(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(None):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_7(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) or parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_8(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" or idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_9(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part != ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_10(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == "XX.worktreesXX" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_11(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".WORKTREES" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_12(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx - 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_13(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 2 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_14(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 <= len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_15(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx - 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_16(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 2] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_17(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] != feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_18(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = None
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_19(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx - 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_20(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 3])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_21(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = None
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_22(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" * feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_23(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root * "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_24(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "XXkitty-specsXX" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_25(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "KITTY-SPECS" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_26(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(None)
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_27(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = None
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_28(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" * feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_29(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root * ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_30(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / "XX.worktreesXX" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_31(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".WORKTREES" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_32(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = None
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_33(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" * feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_34(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path * "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_35(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "XXkitty-specsXX" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_36(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "KITTY-SPECS" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_37(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(None)
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_38(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(None)
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_39(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = None
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_40(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" * feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_41(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root * "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_42(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "XXkitty-specsXX" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_43(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "KITTY-SPECS" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_44(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(None)
    resolved_console.print(
        f"[yellow]Tip:[/yellow] Consider creating a worktree with: git worktree add .worktrees/{feature_slug} {feature_slug}"
    )
    return feature_dir


def x_resolve_worktree_aware_feature_dir__mutmut_45(
    repo_root: Path,
    feature_slug: str,
    cwd: Path | None = None,
    console: ConsoleType = None,
) -> Path:
    """Resolve the correct feature directory, preferring worktree locations when available."""
    resolved_console = _resolve_console(console)
    current_dir = (cwd or Path.cwd()).resolve()

    parts = current_dir.parts
    for idx, part in enumerate(parts):
        if part == ".worktrees" and idx + 1 < len(parts) and parts[idx + 1] == feature_slug:
            worktree_root = Path(*parts[: idx + 2])
            feature_dir = worktree_root / "kitty-specs" / feature_slug
            resolved_console.print(f"[green]✓[/green] Using worktree location: {feature_dir}")
            return feature_dir

    worktree_path = repo_root / ".worktrees" / feature_slug
    if worktree_path.exists():
        feature_dir = worktree_path / "kitty-specs" / feature_slug
        resolved_console.print(f"[green]✓[/green] Found worktree, using: {feature_dir}")
        resolved_console.print(f"[yellow]Tip:[/yellow] Run commands from {worktree_path} for better isolation")
        return feature_dir

    feature_dir = repo_root / "kitty-specs" / feature_slug
    resolved_console.print(f"[yellow]⚠[/yellow] No worktree found, using root location: {feature_dir}")
    resolved_console.print(
        None
    )
    return feature_dir

x_resolve_worktree_aware_feature_dir__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_resolve_worktree_aware_feature_dir__mutmut_1': x_resolve_worktree_aware_feature_dir__mutmut_1, 
    'x_resolve_worktree_aware_feature_dir__mutmut_2': x_resolve_worktree_aware_feature_dir__mutmut_2, 
    'x_resolve_worktree_aware_feature_dir__mutmut_3': x_resolve_worktree_aware_feature_dir__mutmut_3, 
    'x_resolve_worktree_aware_feature_dir__mutmut_4': x_resolve_worktree_aware_feature_dir__mutmut_4, 
    'x_resolve_worktree_aware_feature_dir__mutmut_5': x_resolve_worktree_aware_feature_dir__mutmut_5, 
    'x_resolve_worktree_aware_feature_dir__mutmut_6': x_resolve_worktree_aware_feature_dir__mutmut_6, 
    'x_resolve_worktree_aware_feature_dir__mutmut_7': x_resolve_worktree_aware_feature_dir__mutmut_7, 
    'x_resolve_worktree_aware_feature_dir__mutmut_8': x_resolve_worktree_aware_feature_dir__mutmut_8, 
    'x_resolve_worktree_aware_feature_dir__mutmut_9': x_resolve_worktree_aware_feature_dir__mutmut_9, 
    'x_resolve_worktree_aware_feature_dir__mutmut_10': x_resolve_worktree_aware_feature_dir__mutmut_10, 
    'x_resolve_worktree_aware_feature_dir__mutmut_11': x_resolve_worktree_aware_feature_dir__mutmut_11, 
    'x_resolve_worktree_aware_feature_dir__mutmut_12': x_resolve_worktree_aware_feature_dir__mutmut_12, 
    'x_resolve_worktree_aware_feature_dir__mutmut_13': x_resolve_worktree_aware_feature_dir__mutmut_13, 
    'x_resolve_worktree_aware_feature_dir__mutmut_14': x_resolve_worktree_aware_feature_dir__mutmut_14, 
    'x_resolve_worktree_aware_feature_dir__mutmut_15': x_resolve_worktree_aware_feature_dir__mutmut_15, 
    'x_resolve_worktree_aware_feature_dir__mutmut_16': x_resolve_worktree_aware_feature_dir__mutmut_16, 
    'x_resolve_worktree_aware_feature_dir__mutmut_17': x_resolve_worktree_aware_feature_dir__mutmut_17, 
    'x_resolve_worktree_aware_feature_dir__mutmut_18': x_resolve_worktree_aware_feature_dir__mutmut_18, 
    'x_resolve_worktree_aware_feature_dir__mutmut_19': x_resolve_worktree_aware_feature_dir__mutmut_19, 
    'x_resolve_worktree_aware_feature_dir__mutmut_20': x_resolve_worktree_aware_feature_dir__mutmut_20, 
    'x_resolve_worktree_aware_feature_dir__mutmut_21': x_resolve_worktree_aware_feature_dir__mutmut_21, 
    'x_resolve_worktree_aware_feature_dir__mutmut_22': x_resolve_worktree_aware_feature_dir__mutmut_22, 
    'x_resolve_worktree_aware_feature_dir__mutmut_23': x_resolve_worktree_aware_feature_dir__mutmut_23, 
    'x_resolve_worktree_aware_feature_dir__mutmut_24': x_resolve_worktree_aware_feature_dir__mutmut_24, 
    'x_resolve_worktree_aware_feature_dir__mutmut_25': x_resolve_worktree_aware_feature_dir__mutmut_25, 
    'x_resolve_worktree_aware_feature_dir__mutmut_26': x_resolve_worktree_aware_feature_dir__mutmut_26, 
    'x_resolve_worktree_aware_feature_dir__mutmut_27': x_resolve_worktree_aware_feature_dir__mutmut_27, 
    'x_resolve_worktree_aware_feature_dir__mutmut_28': x_resolve_worktree_aware_feature_dir__mutmut_28, 
    'x_resolve_worktree_aware_feature_dir__mutmut_29': x_resolve_worktree_aware_feature_dir__mutmut_29, 
    'x_resolve_worktree_aware_feature_dir__mutmut_30': x_resolve_worktree_aware_feature_dir__mutmut_30, 
    'x_resolve_worktree_aware_feature_dir__mutmut_31': x_resolve_worktree_aware_feature_dir__mutmut_31, 
    'x_resolve_worktree_aware_feature_dir__mutmut_32': x_resolve_worktree_aware_feature_dir__mutmut_32, 
    'x_resolve_worktree_aware_feature_dir__mutmut_33': x_resolve_worktree_aware_feature_dir__mutmut_33, 
    'x_resolve_worktree_aware_feature_dir__mutmut_34': x_resolve_worktree_aware_feature_dir__mutmut_34, 
    'x_resolve_worktree_aware_feature_dir__mutmut_35': x_resolve_worktree_aware_feature_dir__mutmut_35, 
    'x_resolve_worktree_aware_feature_dir__mutmut_36': x_resolve_worktree_aware_feature_dir__mutmut_36, 
    'x_resolve_worktree_aware_feature_dir__mutmut_37': x_resolve_worktree_aware_feature_dir__mutmut_37, 
    'x_resolve_worktree_aware_feature_dir__mutmut_38': x_resolve_worktree_aware_feature_dir__mutmut_38, 
    'x_resolve_worktree_aware_feature_dir__mutmut_39': x_resolve_worktree_aware_feature_dir__mutmut_39, 
    'x_resolve_worktree_aware_feature_dir__mutmut_40': x_resolve_worktree_aware_feature_dir__mutmut_40, 
    'x_resolve_worktree_aware_feature_dir__mutmut_41': x_resolve_worktree_aware_feature_dir__mutmut_41, 
    'x_resolve_worktree_aware_feature_dir__mutmut_42': x_resolve_worktree_aware_feature_dir__mutmut_42, 
    'x_resolve_worktree_aware_feature_dir__mutmut_43': x_resolve_worktree_aware_feature_dir__mutmut_43, 
    'x_resolve_worktree_aware_feature_dir__mutmut_44': x_resolve_worktree_aware_feature_dir__mutmut_44, 
    'x_resolve_worktree_aware_feature_dir__mutmut_45': x_resolve_worktree_aware_feature_dir__mutmut_45
}
x_resolve_worktree_aware_feature_dir__mutmut_orig.__name__ = 'x_resolve_worktree_aware_feature_dir'


def get_active_mission_key(project_path: Path) -> str:
    args = [project_path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_active_mission_key__mutmut_orig, x_get_active_mission_key__mutmut_mutants, args, kwargs, None)


def x_get_active_mission_key__mutmut_orig(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_1(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = None
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_2(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" * "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_3(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path * ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_4(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / "XX.kittifyXX" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_5(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".KITTIFY" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_6(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "XXactive-missionXX"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_7(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "ACTIVE-MISSION"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_8(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_9(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = None
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_10(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(None)
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_11(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(None))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_12(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = None
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_13(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = None
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_14(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name != "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_15(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "XXmissionsXX":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_16(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "MISSIONS":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_17(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = None
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_18(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding=None).strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_19(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="XXutf-8-sigXX").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY


def x_get_active_mission_key__mutmut_20(project_path: Path) -> str:
    """Return the mission key stored in .kittify/active-mission, falling back to default."""
    active_path = project_path / ".kittify" / "active-mission"
    if not active_path.exists():
        return DEFAULT_MISSION_KEY

    if active_path.is_symlink():
        try:
            target = Path(os.readlink(active_path))
            key = target.name
            if key:
                return key
        except OSError:
            pass
        resolved = active_path.resolve()
        if resolved.parent.name == "missions":
            return resolved.name

    if active_path.is_file():
        try:
            key = active_path.read_text(encoding="UTF-8-SIG").strip()
            if key:
                return key
        except OSError:
            pass

    return DEFAULT_MISSION_KEY

x_get_active_mission_key__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_active_mission_key__mutmut_1': x_get_active_mission_key__mutmut_1, 
    'x_get_active_mission_key__mutmut_2': x_get_active_mission_key__mutmut_2, 
    'x_get_active_mission_key__mutmut_3': x_get_active_mission_key__mutmut_3, 
    'x_get_active_mission_key__mutmut_4': x_get_active_mission_key__mutmut_4, 
    'x_get_active_mission_key__mutmut_5': x_get_active_mission_key__mutmut_5, 
    'x_get_active_mission_key__mutmut_6': x_get_active_mission_key__mutmut_6, 
    'x_get_active_mission_key__mutmut_7': x_get_active_mission_key__mutmut_7, 
    'x_get_active_mission_key__mutmut_8': x_get_active_mission_key__mutmut_8, 
    'x_get_active_mission_key__mutmut_9': x_get_active_mission_key__mutmut_9, 
    'x_get_active_mission_key__mutmut_10': x_get_active_mission_key__mutmut_10, 
    'x_get_active_mission_key__mutmut_11': x_get_active_mission_key__mutmut_11, 
    'x_get_active_mission_key__mutmut_12': x_get_active_mission_key__mutmut_12, 
    'x_get_active_mission_key__mutmut_13': x_get_active_mission_key__mutmut_13, 
    'x_get_active_mission_key__mutmut_14': x_get_active_mission_key__mutmut_14, 
    'x_get_active_mission_key__mutmut_15': x_get_active_mission_key__mutmut_15, 
    'x_get_active_mission_key__mutmut_16': x_get_active_mission_key__mutmut_16, 
    'x_get_active_mission_key__mutmut_17': x_get_active_mission_key__mutmut_17, 
    'x_get_active_mission_key__mutmut_18': x_get_active_mission_key__mutmut_18, 
    'x_get_active_mission_key__mutmut_19': x_get_active_mission_key__mutmut_19, 
    'x_get_active_mission_key__mutmut_20': x_get_active_mission_key__mutmut_20
}
x_get_active_mission_key__mutmut_orig.__name__ = 'x_get_active_mission_key'


__all__ = [
    "get_active_mission_key",
    "locate_project_root",
    "resolve_template_path",
    "resolve_worktree_aware_feature_dir",
]
