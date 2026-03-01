"""Shared utility helpers used across Spec Kitty modules."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
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


def format_path(path: Path, relative_to: Path | None = None) -> str:
    args = [path, relative_to]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_format_path__mutmut_orig, x_format_path__mutmut_mutants, args, kwargs, None)


def x_format_path__mutmut_orig(path: Path, relative_to: Path | None = None) -> str:
    """Return a string path, optionally relative to another directory."""
    target = path
    if relative_to is not None:
        try:
            target = path.relative_to(relative_to)
        except ValueError:
            target = path
    return str(target)


def x_format_path__mutmut_1(path: Path, relative_to: Path | None = None) -> str:
    """Return a string path, optionally relative to another directory."""
    target = None
    if relative_to is not None:
        try:
            target = path.relative_to(relative_to)
        except ValueError:
            target = path
    return str(target)


def x_format_path__mutmut_2(path: Path, relative_to: Path | None = None) -> str:
    """Return a string path, optionally relative to another directory."""
    target = path
    if relative_to is None:
        try:
            target = path.relative_to(relative_to)
        except ValueError:
            target = path
    return str(target)


def x_format_path__mutmut_3(path: Path, relative_to: Path | None = None) -> str:
    """Return a string path, optionally relative to another directory."""
    target = path
    if relative_to is not None:
        try:
            target = None
        except ValueError:
            target = path
    return str(target)


def x_format_path__mutmut_4(path: Path, relative_to: Path | None = None) -> str:
    """Return a string path, optionally relative to another directory."""
    target = path
    if relative_to is not None:
        try:
            target = path.relative_to(None)
        except ValueError:
            target = path
    return str(target)


def x_format_path__mutmut_5(path: Path, relative_to: Path | None = None) -> str:
    """Return a string path, optionally relative to another directory."""
    target = path
    if relative_to is not None:
        try:
            target = path.relative_to(relative_to)
        except ValueError:
            target = None
    return str(target)


def x_format_path__mutmut_6(path: Path, relative_to: Path | None = None) -> str:
    """Return a string path, optionally relative to another directory."""
    target = path
    if relative_to is not None:
        try:
            target = path.relative_to(relative_to)
        except ValueError:
            target = path
    return str(None)

x_format_path__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_format_path__mutmut_1': x_format_path__mutmut_1, 
    'x_format_path__mutmut_2': x_format_path__mutmut_2, 
    'x_format_path__mutmut_3': x_format_path__mutmut_3, 
    'x_format_path__mutmut_4': x_format_path__mutmut_4, 
    'x_format_path__mutmut_5': x_format_path__mutmut_5, 
    'x_format_path__mutmut_6': x_format_path__mutmut_6
}
x_format_path__mutmut_orig.__name__ = 'x_format_path'


def ensure_directory(path: Path) -> Path:
    args = [path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_ensure_directory__mutmut_orig, x_ensure_directory__mutmut_mutants, args, kwargs, None)


def x_ensure_directory__mutmut_orig(path: Path) -> Path:
    """Create a directory (and parents) if it does not exist and return the Path."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def x_ensure_directory__mutmut_1(path: Path) -> Path:
    """Create a directory (and parents) if it does not exist and return the Path."""
    path.mkdir(parents=None, exist_ok=True)
    return path


def x_ensure_directory__mutmut_2(path: Path) -> Path:
    """Create a directory (and parents) if it does not exist and return the Path."""
    path.mkdir(parents=True, exist_ok=None)
    return path


def x_ensure_directory__mutmut_3(path: Path) -> Path:
    """Create a directory (and parents) if it does not exist and return the Path."""
    path.mkdir(exist_ok=True)
    return path


def x_ensure_directory__mutmut_4(path: Path) -> Path:
    """Create a directory (and parents) if it does not exist and return the Path."""
    path.mkdir(parents=True, )
    return path


def x_ensure_directory__mutmut_5(path: Path) -> Path:
    """Create a directory (and parents) if it does not exist and return the Path."""
    path.mkdir(parents=False, exist_ok=True)
    return path


def x_ensure_directory__mutmut_6(path: Path) -> Path:
    """Create a directory (and parents) if it does not exist and return the Path."""
    path.mkdir(parents=True, exist_ok=False)
    return path

x_ensure_directory__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_ensure_directory__mutmut_1': x_ensure_directory__mutmut_1, 
    'x_ensure_directory__mutmut_2': x_ensure_directory__mutmut_2, 
    'x_ensure_directory__mutmut_3': x_ensure_directory__mutmut_3, 
    'x_ensure_directory__mutmut_4': x_ensure_directory__mutmut_4, 
    'x_ensure_directory__mutmut_5': x_ensure_directory__mutmut_5, 
    'x_ensure_directory__mutmut_6': x_ensure_directory__mutmut_6
}
x_ensure_directory__mutmut_orig.__name__ = 'x_ensure_directory'


def safe_remove(path: Path) -> bool:
    args = [path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_safe_remove__mutmut_orig, x_safe_remove__mutmut_mutants, args, kwargs, None)


def x_safe_remove__mutmut_orig(path: Path) -> bool:
    """Remove a file or directory tree if it exists, returning True when something was removed."""
    if not path.exists():
        return False
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()
    return True


def x_safe_remove__mutmut_1(path: Path) -> bool:
    """Remove a file or directory tree if it exists, returning True when something was removed."""
    if path.exists():
        return False
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()
    return True


def x_safe_remove__mutmut_2(path: Path) -> bool:
    """Remove a file or directory tree if it exists, returning True when something was removed."""
    if not path.exists():
        return True
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()
    return True


def x_safe_remove__mutmut_3(path: Path) -> bool:
    """Remove a file or directory tree if it exists, returning True when something was removed."""
    if not path.exists():
        return False
    if path.is_dir() or not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()
    return True


def x_safe_remove__mutmut_4(path: Path) -> bool:
    """Remove a file or directory tree if it exists, returning True when something was removed."""
    if not path.exists():
        return False
    if path.is_dir() and path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()
    return True


def x_safe_remove__mutmut_5(path: Path) -> bool:
    """Remove a file or directory tree if it exists, returning True when something was removed."""
    if not path.exists():
        return False
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(None)
    else:
        path.unlink()
    return True


def x_safe_remove__mutmut_6(path: Path) -> bool:
    """Remove a file or directory tree if it exists, returning True when something was removed."""
    if not path.exists():
        return False
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()
    return False

x_safe_remove__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_safe_remove__mutmut_1': x_safe_remove__mutmut_1, 
    'x_safe_remove__mutmut_2': x_safe_remove__mutmut_2, 
    'x_safe_remove__mutmut_3': x_safe_remove__mutmut_3, 
    'x_safe_remove__mutmut_4': x_safe_remove__mutmut_4, 
    'x_safe_remove__mutmut_5': x_safe_remove__mutmut_5, 
    'x_safe_remove__mutmut_6': x_safe_remove__mutmut_6
}
x_safe_remove__mutmut_orig.__name__ = 'x_safe_remove'


def get_platform() -> str:
    """Return the current platform identifier (linux/darwin/win32)."""
    return sys.platform


__all__ = ["format_path", "ensure_directory", "safe_remove", "get_platform"]
