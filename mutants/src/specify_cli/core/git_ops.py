"""Git and subprocess helpers for the Spec Kitty CLI."""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from rich.console import Console

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


@dataclass
class BranchResolution:
    """Result of branch resolution for feature operations.

    Attributes:
        target: Target branch from meta.json
        current: User's current branch
        should_notify: True if current != target (informational notification needed)
        action: "proceed" (branches match) or "stay_on_current" (respect user's branch)
    """

    target: str
    current: str
    should_notify: bool
    action: str


def _resolve_console(console: ConsoleType) -> Console:
    args = [console]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__resolve_console__mutmut_orig, x__resolve_console__mutmut_mutants, args, kwargs, None)


def x__resolve_console__mutmut_orig(console: ConsoleType) -> Console:
    """Return the provided console or lazily create one."""
    return console if console is not None else Console()


def x__resolve_console__mutmut_1(console: ConsoleType) -> Console:
    """Return the provided console or lazily create one."""
    return console if console is None else Console()

x__resolve_console__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__resolve_console__mutmut_1': x__resolve_console__mutmut_1
}
x__resolve_console__mutmut_orig.__name__ = 'x__resolve_console'


def run_command(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    args = [cmd]# type: ignore
    kwargs = {'check_return': check_return, 'capture': capture, 'shell': shell, 'console': console, 'cwd': cwd}# type: ignore
    return _mutmut_trampoline(x_run_command__mutmut_orig, x_run_command__mutmut_mutants, args, kwargs, None)


def x_run_command__mutmut_orig(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_1(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = False,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_2(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = True,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_3(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = True,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_4(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = None
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_5(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            None,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_6(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=None,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_7(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_8(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=None,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_9(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding=None,
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_10(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors=None,
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_11(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=None,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_12(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_13(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_14(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_15(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_16(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_17(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_18(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_19(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_20(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_21(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=False,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_22(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_23(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="UTF-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_24(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_25(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_26(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(None) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_27(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = None
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_28(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout and "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_29(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "XXXX").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_30(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else "XXXX"
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_31(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = None
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_32(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr and "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_33(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "XXXX").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_34(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else "XXXX"
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_35(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = None
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_36(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(None)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_37(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(None)
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_38(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(None)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_39(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else 'XX XX'.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_40(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(None)
            if exc.stderr:
                resolved_console.print(f"[red]Error output:[/red] {exc.stderr.strip()}")
        raise


def x_run_command__mutmut_41(
    cmd: Sequence[str] | str,
    *,
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: ConsoleType = None,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr).

    Args:
        cmd: Command to run
        check_return: If True, raise on non-zero exit
        capture: If True, capture stdout/stderr
        shell: If True, run through shell
        console: Rich console for output
        cwd: Working directory for command execution

    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            check=check_return,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
            cwd=str(cwd) if cwd else None,
        )
        stdout = (result.stdout or "").strip() if capture else ""
        stderr = (result.stderr or "").strip() if capture else ""
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as exc:
        if check_return:
            resolved_console = _resolve_console(console)
            resolved_console.print(f"[red]Error running command:[/red] {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            resolved_console.print(f"[red]Exit code:[/red] {exc.returncode}")
            if exc.stderr:
                resolved_console.print(None)
        raise

x_run_command__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_run_command__mutmut_1': x_run_command__mutmut_1, 
    'x_run_command__mutmut_2': x_run_command__mutmut_2, 
    'x_run_command__mutmut_3': x_run_command__mutmut_3, 
    'x_run_command__mutmut_4': x_run_command__mutmut_4, 
    'x_run_command__mutmut_5': x_run_command__mutmut_5, 
    'x_run_command__mutmut_6': x_run_command__mutmut_6, 
    'x_run_command__mutmut_7': x_run_command__mutmut_7, 
    'x_run_command__mutmut_8': x_run_command__mutmut_8, 
    'x_run_command__mutmut_9': x_run_command__mutmut_9, 
    'x_run_command__mutmut_10': x_run_command__mutmut_10, 
    'x_run_command__mutmut_11': x_run_command__mutmut_11, 
    'x_run_command__mutmut_12': x_run_command__mutmut_12, 
    'x_run_command__mutmut_13': x_run_command__mutmut_13, 
    'x_run_command__mutmut_14': x_run_command__mutmut_14, 
    'x_run_command__mutmut_15': x_run_command__mutmut_15, 
    'x_run_command__mutmut_16': x_run_command__mutmut_16, 
    'x_run_command__mutmut_17': x_run_command__mutmut_17, 
    'x_run_command__mutmut_18': x_run_command__mutmut_18, 
    'x_run_command__mutmut_19': x_run_command__mutmut_19, 
    'x_run_command__mutmut_20': x_run_command__mutmut_20, 
    'x_run_command__mutmut_21': x_run_command__mutmut_21, 
    'x_run_command__mutmut_22': x_run_command__mutmut_22, 
    'x_run_command__mutmut_23': x_run_command__mutmut_23, 
    'x_run_command__mutmut_24': x_run_command__mutmut_24, 
    'x_run_command__mutmut_25': x_run_command__mutmut_25, 
    'x_run_command__mutmut_26': x_run_command__mutmut_26, 
    'x_run_command__mutmut_27': x_run_command__mutmut_27, 
    'x_run_command__mutmut_28': x_run_command__mutmut_28, 
    'x_run_command__mutmut_29': x_run_command__mutmut_29, 
    'x_run_command__mutmut_30': x_run_command__mutmut_30, 
    'x_run_command__mutmut_31': x_run_command__mutmut_31, 
    'x_run_command__mutmut_32': x_run_command__mutmut_32, 
    'x_run_command__mutmut_33': x_run_command__mutmut_33, 
    'x_run_command__mutmut_34': x_run_command__mutmut_34, 
    'x_run_command__mutmut_35': x_run_command__mutmut_35, 
    'x_run_command__mutmut_36': x_run_command__mutmut_36, 
    'x_run_command__mutmut_37': x_run_command__mutmut_37, 
    'x_run_command__mutmut_38': x_run_command__mutmut_38, 
    'x_run_command__mutmut_39': x_run_command__mutmut_39, 
    'x_run_command__mutmut_40': x_run_command__mutmut_40, 
    'x_run_command__mutmut_41': x_run_command__mutmut_41
}
x_run_command__mutmut_orig.__name__ = 'x_run_command'


def is_git_repo(path: Path | None = None) -> bool:
    args = [path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_is_git_repo__mutmut_orig, x_is_git_repo__mutmut_mutants, args, kwargs, None)


def x_is_git_repo__mutmut_orig(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_1(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = None
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_2(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path and Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_3(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_4(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return True
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_5(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            None,
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_6(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=None,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_7(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=None,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_8(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=None,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_9(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_10(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_11(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_12(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_13(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["XXgitXX", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_14(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["GIT", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_15(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "XXrev-parseXX", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_16(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "REV-PARSE", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_17(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "XX--is-inside-work-treeXX"],
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_18(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--IS-INSIDE-WORK-TREE"],
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_19(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=False,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_20(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=False,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_21(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=target,
        )
        return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_is_git_repo__mutmut_22(path: Path | None = None) -> bool:
    """Return True when the provided path lives inside a git repository."""
    target = (path or Path.cwd()).resolve()
    if not target.is_dir():
        return False
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=target,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return True

x_is_git_repo__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_is_git_repo__mutmut_1': x_is_git_repo__mutmut_1, 
    'x_is_git_repo__mutmut_2': x_is_git_repo__mutmut_2, 
    'x_is_git_repo__mutmut_3': x_is_git_repo__mutmut_3, 
    'x_is_git_repo__mutmut_4': x_is_git_repo__mutmut_4, 
    'x_is_git_repo__mutmut_5': x_is_git_repo__mutmut_5, 
    'x_is_git_repo__mutmut_6': x_is_git_repo__mutmut_6, 
    'x_is_git_repo__mutmut_7': x_is_git_repo__mutmut_7, 
    'x_is_git_repo__mutmut_8': x_is_git_repo__mutmut_8, 
    'x_is_git_repo__mutmut_9': x_is_git_repo__mutmut_9, 
    'x_is_git_repo__mutmut_10': x_is_git_repo__mutmut_10, 
    'x_is_git_repo__mutmut_11': x_is_git_repo__mutmut_11, 
    'x_is_git_repo__mutmut_12': x_is_git_repo__mutmut_12, 
    'x_is_git_repo__mutmut_13': x_is_git_repo__mutmut_13, 
    'x_is_git_repo__mutmut_14': x_is_git_repo__mutmut_14, 
    'x_is_git_repo__mutmut_15': x_is_git_repo__mutmut_15, 
    'x_is_git_repo__mutmut_16': x_is_git_repo__mutmut_16, 
    'x_is_git_repo__mutmut_17': x_is_git_repo__mutmut_17, 
    'x_is_git_repo__mutmut_18': x_is_git_repo__mutmut_18, 
    'x_is_git_repo__mutmut_19': x_is_git_repo__mutmut_19, 
    'x_is_git_repo__mutmut_20': x_is_git_repo__mutmut_20, 
    'x_is_git_repo__mutmut_21': x_is_git_repo__mutmut_21, 
    'x_is_git_repo__mutmut_22': x_is_git_repo__mutmut_22
}
x_is_git_repo__mutmut_orig.__name__ = 'x_is_git_repo'


def init_git_repo(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    args = [project_path, quiet, console]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_init_git_repo__mutmut_orig, x_init_git_repo__mutmut_mutants, args, kwargs, None)


def x_init_git_repo__mutmut_orig(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_1(project_path: Path, quiet: bool = True, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_2(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = None
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_3(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(None)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_4(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = None
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_5(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(None)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_6(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_7(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print(None)
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_8(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("XX[cyan]Initializing git repository...[/cyan]XX")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_9(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_10(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[CYAN]INITIALIZING GIT REPOSITORY...[/CYAN]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_11(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(None, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_12(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=None, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_13(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=None)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_14(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_15(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_16(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, )
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_17(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["XXgitXX", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_18(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["GIT", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_19(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "XXinitXX"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_20(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "INIT"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_21(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=False, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_22(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=False)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_23(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(None, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_24(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=None, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_25(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=None)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_26(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_27(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_28(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_29(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["XXgitXX", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_30(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["GIT", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_31(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "XXaddXX", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_32(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "ADD", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_33(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "XX.XX"], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_34(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=False, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_35(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=False)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_36(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            None,
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_37(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=None,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_38(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=None,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_39(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_40(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_41(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_42(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["XXgitXX", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_43(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["GIT", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_44(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "XXcommitXX", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_45(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "COMMIT", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_46(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "XX-mXX", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_47(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-M", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_48(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "XXInitial commit from Specify templateXX"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_49(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "initial commit from specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_50(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "INITIAL COMMIT FROM SPECIFY TEMPLATE"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_51(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=False,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_52(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=False,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_53(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_54(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print(None)
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_55(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("XX[green]✓[/green] Git repository initializedXX")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_56(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_57(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[GREEN]✓[/GREEN] GIT REPOSITORY INITIALIZED")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_58(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return False
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_59(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_60(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(None)
        return False
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_61(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return True
    finally:
        os.chdir(original_cwd)


def x_init_git_repo__mutmut_62(project_path: Path, quiet: bool = False, console: ConsoleType = None) -> bool:
    """Initialize a git repository with an initial commit."""
    resolved_console = _resolve_console(console)
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            resolved_console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
        )
        if not quiet:
            resolved_console.print("[green]✓[/green] Git repository initialized")
        return True
    except subprocess.CalledProcessError as exc:
        if not quiet:
            resolved_console.print(f"[red]Error initializing git repository:[/red] {exc}")
        return False
    finally:
        os.chdir(None)

x_init_git_repo__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_init_git_repo__mutmut_1': x_init_git_repo__mutmut_1, 
    'x_init_git_repo__mutmut_2': x_init_git_repo__mutmut_2, 
    'x_init_git_repo__mutmut_3': x_init_git_repo__mutmut_3, 
    'x_init_git_repo__mutmut_4': x_init_git_repo__mutmut_4, 
    'x_init_git_repo__mutmut_5': x_init_git_repo__mutmut_5, 
    'x_init_git_repo__mutmut_6': x_init_git_repo__mutmut_6, 
    'x_init_git_repo__mutmut_7': x_init_git_repo__mutmut_7, 
    'x_init_git_repo__mutmut_8': x_init_git_repo__mutmut_8, 
    'x_init_git_repo__mutmut_9': x_init_git_repo__mutmut_9, 
    'x_init_git_repo__mutmut_10': x_init_git_repo__mutmut_10, 
    'x_init_git_repo__mutmut_11': x_init_git_repo__mutmut_11, 
    'x_init_git_repo__mutmut_12': x_init_git_repo__mutmut_12, 
    'x_init_git_repo__mutmut_13': x_init_git_repo__mutmut_13, 
    'x_init_git_repo__mutmut_14': x_init_git_repo__mutmut_14, 
    'x_init_git_repo__mutmut_15': x_init_git_repo__mutmut_15, 
    'x_init_git_repo__mutmut_16': x_init_git_repo__mutmut_16, 
    'x_init_git_repo__mutmut_17': x_init_git_repo__mutmut_17, 
    'x_init_git_repo__mutmut_18': x_init_git_repo__mutmut_18, 
    'x_init_git_repo__mutmut_19': x_init_git_repo__mutmut_19, 
    'x_init_git_repo__mutmut_20': x_init_git_repo__mutmut_20, 
    'x_init_git_repo__mutmut_21': x_init_git_repo__mutmut_21, 
    'x_init_git_repo__mutmut_22': x_init_git_repo__mutmut_22, 
    'x_init_git_repo__mutmut_23': x_init_git_repo__mutmut_23, 
    'x_init_git_repo__mutmut_24': x_init_git_repo__mutmut_24, 
    'x_init_git_repo__mutmut_25': x_init_git_repo__mutmut_25, 
    'x_init_git_repo__mutmut_26': x_init_git_repo__mutmut_26, 
    'x_init_git_repo__mutmut_27': x_init_git_repo__mutmut_27, 
    'x_init_git_repo__mutmut_28': x_init_git_repo__mutmut_28, 
    'x_init_git_repo__mutmut_29': x_init_git_repo__mutmut_29, 
    'x_init_git_repo__mutmut_30': x_init_git_repo__mutmut_30, 
    'x_init_git_repo__mutmut_31': x_init_git_repo__mutmut_31, 
    'x_init_git_repo__mutmut_32': x_init_git_repo__mutmut_32, 
    'x_init_git_repo__mutmut_33': x_init_git_repo__mutmut_33, 
    'x_init_git_repo__mutmut_34': x_init_git_repo__mutmut_34, 
    'x_init_git_repo__mutmut_35': x_init_git_repo__mutmut_35, 
    'x_init_git_repo__mutmut_36': x_init_git_repo__mutmut_36, 
    'x_init_git_repo__mutmut_37': x_init_git_repo__mutmut_37, 
    'x_init_git_repo__mutmut_38': x_init_git_repo__mutmut_38, 
    'x_init_git_repo__mutmut_39': x_init_git_repo__mutmut_39, 
    'x_init_git_repo__mutmut_40': x_init_git_repo__mutmut_40, 
    'x_init_git_repo__mutmut_41': x_init_git_repo__mutmut_41, 
    'x_init_git_repo__mutmut_42': x_init_git_repo__mutmut_42, 
    'x_init_git_repo__mutmut_43': x_init_git_repo__mutmut_43, 
    'x_init_git_repo__mutmut_44': x_init_git_repo__mutmut_44, 
    'x_init_git_repo__mutmut_45': x_init_git_repo__mutmut_45, 
    'x_init_git_repo__mutmut_46': x_init_git_repo__mutmut_46, 
    'x_init_git_repo__mutmut_47': x_init_git_repo__mutmut_47, 
    'x_init_git_repo__mutmut_48': x_init_git_repo__mutmut_48, 
    'x_init_git_repo__mutmut_49': x_init_git_repo__mutmut_49, 
    'x_init_git_repo__mutmut_50': x_init_git_repo__mutmut_50, 
    'x_init_git_repo__mutmut_51': x_init_git_repo__mutmut_51, 
    'x_init_git_repo__mutmut_52': x_init_git_repo__mutmut_52, 
    'x_init_git_repo__mutmut_53': x_init_git_repo__mutmut_53, 
    'x_init_git_repo__mutmut_54': x_init_git_repo__mutmut_54, 
    'x_init_git_repo__mutmut_55': x_init_git_repo__mutmut_55, 
    'x_init_git_repo__mutmut_56': x_init_git_repo__mutmut_56, 
    'x_init_git_repo__mutmut_57': x_init_git_repo__mutmut_57, 
    'x_init_git_repo__mutmut_58': x_init_git_repo__mutmut_58, 
    'x_init_git_repo__mutmut_59': x_init_git_repo__mutmut_59, 
    'x_init_git_repo__mutmut_60': x_init_git_repo__mutmut_60, 
    'x_init_git_repo__mutmut_61': x_init_git_repo__mutmut_61, 
    'x_init_git_repo__mutmut_62': x_init_git_repo__mutmut_62
}
x_init_git_repo__mutmut_orig.__name__ = 'x_init_git_repo'


def get_current_branch(path: Path | None = None) -> str | None:
    args = [path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_current_branch__mutmut_orig, x_get_current_branch__mutmut_mutants, args, kwargs, None)


def x_get_current_branch__mutmut_orig(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_1(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = None

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_2(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path and Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_3(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = None
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_4(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            None,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_5(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_6(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_7(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=None,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_8(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding=None,
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_9(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors=None,
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_10(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=None,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_11(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_12(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_13(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_14(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_15(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_16(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_17(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_18(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["XXgitXX", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_19(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["GIT", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_20(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "XXbranchXX", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_21(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "BRANCH", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_22(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "XX--show-currentXX"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_23(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--SHOW-CURRENT"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_24(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_25(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_26(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=False,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_27(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_28(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="UTF-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_29(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_30(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_31(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = None
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_32(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch and None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_33(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = None
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_34(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            None,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_35(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_36(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_37(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=None,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_38(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding=None,
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_39(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors=None,
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_40(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=None,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_41(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_42(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_43(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_44(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_45(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_46(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_47(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_48(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["XXgitXX", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_49(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["GIT", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_50(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "XXrev-parseXX", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_51(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "REV-PARSE", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_52(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "XX--abbrev-refXX", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_53(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--ABBREV-REF", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_54(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "XXHEADXX"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_55(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "head"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_56(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_57(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_58(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=False,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_59(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_60(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="UTF-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_61(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_62(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_63(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = None
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_64(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch != "HEAD":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_65(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "XXHEADXX":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_66(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "head":
            return None  # Detached HEAD
        return branch or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def x_get_current_branch__mutmut_67(path: Path | None = None) -> str | None:
    """Return the current git branch name for the provided repository path.

    Tries ``git branch --show-current`` first (Git 2.22+, correctly handles
    unborn branches).  Falls back to ``git rev-parse --abbrev-ref HEAD`` for
    older Git versions.  Returns ``None`` for detached HEAD or when not
    inside a git repository.
    """
    repo_path = (path or Path.cwd()).resolve()

    # Primary: git branch --show-current (Git 2.22+)
    # Handles unborn branches correctly and returns empty string for detached HEAD.
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        return branch or None
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        return None

    # Fallback: git rev-parse --abbrev-ref HEAD (Git < 2.22)
    # Returns "HEAD" for detached HEAD; fails on unborn branches.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
        )
        branch = result.stdout.strip()
        if branch == "HEAD":
            return None  # Detached HEAD
        return branch and None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

x_get_current_branch__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_current_branch__mutmut_1': x_get_current_branch__mutmut_1, 
    'x_get_current_branch__mutmut_2': x_get_current_branch__mutmut_2, 
    'x_get_current_branch__mutmut_3': x_get_current_branch__mutmut_3, 
    'x_get_current_branch__mutmut_4': x_get_current_branch__mutmut_4, 
    'x_get_current_branch__mutmut_5': x_get_current_branch__mutmut_5, 
    'x_get_current_branch__mutmut_6': x_get_current_branch__mutmut_6, 
    'x_get_current_branch__mutmut_7': x_get_current_branch__mutmut_7, 
    'x_get_current_branch__mutmut_8': x_get_current_branch__mutmut_8, 
    'x_get_current_branch__mutmut_9': x_get_current_branch__mutmut_9, 
    'x_get_current_branch__mutmut_10': x_get_current_branch__mutmut_10, 
    'x_get_current_branch__mutmut_11': x_get_current_branch__mutmut_11, 
    'x_get_current_branch__mutmut_12': x_get_current_branch__mutmut_12, 
    'x_get_current_branch__mutmut_13': x_get_current_branch__mutmut_13, 
    'x_get_current_branch__mutmut_14': x_get_current_branch__mutmut_14, 
    'x_get_current_branch__mutmut_15': x_get_current_branch__mutmut_15, 
    'x_get_current_branch__mutmut_16': x_get_current_branch__mutmut_16, 
    'x_get_current_branch__mutmut_17': x_get_current_branch__mutmut_17, 
    'x_get_current_branch__mutmut_18': x_get_current_branch__mutmut_18, 
    'x_get_current_branch__mutmut_19': x_get_current_branch__mutmut_19, 
    'x_get_current_branch__mutmut_20': x_get_current_branch__mutmut_20, 
    'x_get_current_branch__mutmut_21': x_get_current_branch__mutmut_21, 
    'x_get_current_branch__mutmut_22': x_get_current_branch__mutmut_22, 
    'x_get_current_branch__mutmut_23': x_get_current_branch__mutmut_23, 
    'x_get_current_branch__mutmut_24': x_get_current_branch__mutmut_24, 
    'x_get_current_branch__mutmut_25': x_get_current_branch__mutmut_25, 
    'x_get_current_branch__mutmut_26': x_get_current_branch__mutmut_26, 
    'x_get_current_branch__mutmut_27': x_get_current_branch__mutmut_27, 
    'x_get_current_branch__mutmut_28': x_get_current_branch__mutmut_28, 
    'x_get_current_branch__mutmut_29': x_get_current_branch__mutmut_29, 
    'x_get_current_branch__mutmut_30': x_get_current_branch__mutmut_30, 
    'x_get_current_branch__mutmut_31': x_get_current_branch__mutmut_31, 
    'x_get_current_branch__mutmut_32': x_get_current_branch__mutmut_32, 
    'x_get_current_branch__mutmut_33': x_get_current_branch__mutmut_33, 
    'x_get_current_branch__mutmut_34': x_get_current_branch__mutmut_34, 
    'x_get_current_branch__mutmut_35': x_get_current_branch__mutmut_35, 
    'x_get_current_branch__mutmut_36': x_get_current_branch__mutmut_36, 
    'x_get_current_branch__mutmut_37': x_get_current_branch__mutmut_37, 
    'x_get_current_branch__mutmut_38': x_get_current_branch__mutmut_38, 
    'x_get_current_branch__mutmut_39': x_get_current_branch__mutmut_39, 
    'x_get_current_branch__mutmut_40': x_get_current_branch__mutmut_40, 
    'x_get_current_branch__mutmut_41': x_get_current_branch__mutmut_41, 
    'x_get_current_branch__mutmut_42': x_get_current_branch__mutmut_42, 
    'x_get_current_branch__mutmut_43': x_get_current_branch__mutmut_43, 
    'x_get_current_branch__mutmut_44': x_get_current_branch__mutmut_44, 
    'x_get_current_branch__mutmut_45': x_get_current_branch__mutmut_45, 
    'x_get_current_branch__mutmut_46': x_get_current_branch__mutmut_46, 
    'x_get_current_branch__mutmut_47': x_get_current_branch__mutmut_47, 
    'x_get_current_branch__mutmut_48': x_get_current_branch__mutmut_48, 
    'x_get_current_branch__mutmut_49': x_get_current_branch__mutmut_49, 
    'x_get_current_branch__mutmut_50': x_get_current_branch__mutmut_50, 
    'x_get_current_branch__mutmut_51': x_get_current_branch__mutmut_51, 
    'x_get_current_branch__mutmut_52': x_get_current_branch__mutmut_52, 
    'x_get_current_branch__mutmut_53': x_get_current_branch__mutmut_53, 
    'x_get_current_branch__mutmut_54': x_get_current_branch__mutmut_54, 
    'x_get_current_branch__mutmut_55': x_get_current_branch__mutmut_55, 
    'x_get_current_branch__mutmut_56': x_get_current_branch__mutmut_56, 
    'x_get_current_branch__mutmut_57': x_get_current_branch__mutmut_57, 
    'x_get_current_branch__mutmut_58': x_get_current_branch__mutmut_58, 
    'x_get_current_branch__mutmut_59': x_get_current_branch__mutmut_59, 
    'x_get_current_branch__mutmut_60': x_get_current_branch__mutmut_60, 
    'x_get_current_branch__mutmut_61': x_get_current_branch__mutmut_61, 
    'x_get_current_branch__mutmut_62': x_get_current_branch__mutmut_62, 
    'x_get_current_branch__mutmut_63': x_get_current_branch__mutmut_63, 
    'x_get_current_branch__mutmut_64': x_get_current_branch__mutmut_64, 
    'x_get_current_branch__mutmut_65': x_get_current_branch__mutmut_65, 
    'x_get_current_branch__mutmut_66': x_get_current_branch__mutmut_66, 
    'x_get_current_branch__mutmut_67': x_get_current_branch__mutmut_67
}
x_get_current_branch__mutmut_orig.__name__ = 'x_get_current_branch'


def has_remote(repo_path: Path, remote_name: str = "origin") -> bool:
    args = [repo_path, remote_name]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_has_remote__mutmut_orig, x_has_remote__mutmut_mutants, args, kwargs, None)


def x_has_remote__mutmut_orig(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_1(repo_path: Path, remote_name: str = "XXoriginXX") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_2(repo_path: Path, remote_name: str = "ORIGIN") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_3(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = None
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_4(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_5(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_6(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=None,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_7(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding=None,
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_8(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors=None,
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_9(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=None,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_10(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=None,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_11(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_12(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_13(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_14(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_15(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_16(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_17(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_18(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["XXgitXX", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_19(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["GIT", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_20(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "XXremoteXX", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_21(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "REMOTE", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_22(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "XXget-urlXX", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_23(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "GET-URL", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_24(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_25(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=False,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_26(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_27(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="UTF-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_28(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_29(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_30(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=True,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_31(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode != 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_32(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 1
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_remote__mutmut_33(repo_path: Path, remote_name: str = "origin") -> bool:
    """Check if repository has a configured remote.

    Args:
        repo_path: Repository root path
        remote_name: Remote name to check (default: "origin")

    Returns:
        True if remote exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return True

x_has_remote__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_has_remote__mutmut_1': x_has_remote__mutmut_1, 
    'x_has_remote__mutmut_2': x_has_remote__mutmut_2, 
    'x_has_remote__mutmut_3': x_has_remote__mutmut_3, 
    'x_has_remote__mutmut_4': x_has_remote__mutmut_4, 
    'x_has_remote__mutmut_5': x_has_remote__mutmut_5, 
    'x_has_remote__mutmut_6': x_has_remote__mutmut_6, 
    'x_has_remote__mutmut_7': x_has_remote__mutmut_7, 
    'x_has_remote__mutmut_8': x_has_remote__mutmut_8, 
    'x_has_remote__mutmut_9': x_has_remote__mutmut_9, 
    'x_has_remote__mutmut_10': x_has_remote__mutmut_10, 
    'x_has_remote__mutmut_11': x_has_remote__mutmut_11, 
    'x_has_remote__mutmut_12': x_has_remote__mutmut_12, 
    'x_has_remote__mutmut_13': x_has_remote__mutmut_13, 
    'x_has_remote__mutmut_14': x_has_remote__mutmut_14, 
    'x_has_remote__mutmut_15': x_has_remote__mutmut_15, 
    'x_has_remote__mutmut_16': x_has_remote__mutmut_16, 
    'x_has_remote__mutmut_17': x_has_remote__mutmut_17, 
    'x_has_remote__mutmut_18': x_has_remote__mutmut_18, 
    'x_has_remote__mutmut_19': x_has_remote__mutmut_19, 
    'x_has_remote__mutmut_20': x_has_remote__mutmut_20, 
    'x_has_remote__mutmut_21': x_has_remote__mutmut_21, 
    'x_has_remote__mutmut_22': x_has_remote__mutmut_22, 
    'x_has_remote__mutmut_23': x_has_remote__mutmut_23, 
    'x_has_remote__mutmut_24': x_has_remote__mutmut_24, 
    'x_has_remote__mutmut_25': x_has_remote__mutmut_25, 
    'x_has_remote__mutmut_26': x_has_remote__mutmut_26, 
    'x_has_remote__mutmut_27': x_has_remote__mutmut_27, 
    'x_has_remote__mutmut_28': x_has_remote__mutmut_28, 
    'x_has_remote__mutmut_29': x_has_remote__mutmut_29, 
    'x_has_remote__mutmut_30': x_has_remote__mutmut_30, 
    'x_has_remote__mutmut_31': x_has_remote__mutmut_31, 
    'x_has_remote__mutmut_32': x_has_remote__mutmut_32, 
    'x_has_remote__mutmut_33': x_has_remote__mutmut_33
}
x_has_remote__mutmut_orig.__name__ = 'x_has_remote'


def has_tracking_branch(repo_path: Path) -> bool:
    args = [repo_path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_has_tracking_branch__mutmut_orig, x_has_tracking_branch__mutmut_mutants, args, kwargs, None)


def x_has_tracking_branch__mutmut_orig(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_1(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = None
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_2(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_3(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_4(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=None,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_5(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding=None,
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_6(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors=None,
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_7(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=None,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_8(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=None,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_9(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_10(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_11(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_12(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_13(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_14(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_15(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_16(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["XXgitXX", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_17(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["GIT", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_18(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "XXrev-parseXX", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_19(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "REV-PARSE", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_20(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "XX--abbrev-refXX", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_21(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--ABBREV-REF", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_22(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "XX--symbolic-full-nameXX", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_23(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--SYMBOLIC-FULL-NAME", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_24(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "XX@{u}XX"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_25(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{U}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_26(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_27(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=False,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_28(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_29(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="UTF-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_30(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_31(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_32(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=True,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_33(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 or result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_34(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode != 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_35(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 1 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_36(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() == ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_37(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != "XXXX"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def x_has_tracking_branch__mutmut_38(repo_path: Path) -> bool:
    """Check if current branch has upstream tracking configured.

    Args:
        repo_path: Repository root path

    Returns:
        True if current branch tracks a remote branch, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=repo_path,
            check=False,
        )
        # Returns 0 with output like "origin/main" if tracking exists
        # Returns 128 with error if no tracking configured
        return result.returncode == 0 and result.stdout.strip() != ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return True

x_has_tracking_branch__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_has_tracking_branch__mutmut_1': x_has_tracking_branch__mutmut_1, 
    'x_has_tracking_branch__mutmut_2': x_has_tracking_branch__mutmut_2, 
    'x_has_tracking_branch__mutmut_3': x_has_tracking_branch__mutmut_3, 
    'x_has_tracking_branch__mutmut_4': x_has_tracking_branch__mutmut_4, 
    'x_has_tracking_branch__mutmut_5': x_has_tracking_branch__mutmut_5, 
    'x_has_tracking_branch__mutmut_6': x_has_tracking_branch__mutmut_6, 
    'x_has_tracking_branch__mutmut_7': x_has_tracking_branch__mutmut_7, 
    'x_has_tracking_branch__mutmut_8': x_has_tracking_branch__mutmut_8, 
    'x_has_tracking_branch__mutmut_9': x_has_tracking_branch__mutmut_9, 
    'x_has_tracking_branch__mutmut_10': x_has_tracking_branch__mutmut_10, 
    'x_has_tracking_branch__mutmut_11': x_has_tracking_branch__mutmut_11, 
    'x_has_tracking_branch__mutmut_12': x_has_tracking_branch__mutmut_12, 
    'x_has_tracking_branch__mutmut_13': x_has_tracking_branch__mutmut_13, 
    'x_has_tracking_branch__mutmut_14': x_has_tracking_branch__mutmut_14, 
    'x_has_tracking_branch__mutmut_15': x_has_tracking_branch__mutmut_15, 
    'x_has_tracking_branch__mutmut_16': x_has_tracking_branch__mutmut_16, 
    'x_has_tracking_branch__mutmut_17': x_has_tracking_branch__mutmut_17, 
    'x_has_tracking_branch__mutmut_18': x_has_tracking_branch__mutmut_18, 
    'x_has_tracking_branch__mutmut_19': x_has_tracking_branch__mutmut_19, 
    'x_has_tracking_branch__mutmut_20': x_has_tracking_branch__mutmut_20, 
    'x_has_tracking_branch__mutmut_21': x_has_tracking_branch__mutmut_21, 
    'x_has_tracking_branch__mutmut_22': x_has_tracking_branch__mutmut_22, 
    'x_has_tracking_branch__mutmut_23': x_has_tracking_branch__mutmut_23, 
    'x_has_tracking_branch__mutmut_24': x_has_tracking_branch__mutmut_24, 
    'x_has_tracking_branch__mutmut_25': x_has_tracking_branch__mutmut_25, 
    'x_has_tracking_branch__mutmut_26': x_has_tracking_branch__mutmut_26, 
    'x_has_tracking_branch__mutmut_27': x_has_tracking_branch__mutmut_27, 
    'x_has_tracking_branch__mutmut_28': x_has_tracking_branch__mutmut_28, 
    'x_has_tracking_branch__mutmut_29': x_has_tracking_branch__mutmut_29, 
    'x_has_tracking_branch__mutmut_30': x_has_tracking_branch__mutmut_30, 
    'x_has_tracking_branch__mutmut_31': x_has_tracking_branch__mutmut_31, 
    'x_has_tracking_branch__mutmut_32': x_has_tracking_branch__mutmut_32, 
    'x_has_tracking_branch__mutmut_33': x_has_tracking_branch__mutmut_33, 
    'x_has_tracking_branch__mutmut_34': x_has_tracking_branch__mutmut_34, 
    'x_has_tracking_branch__mutmut_35': x_has_tracking_branch__mutmut_35, 
    'x_has_tracking_branch__mutmut_36': x_has_tracking_branch__mutmut_36, 
    'x_has_tracking_branch__mutmut_37': x_has_tracking_branch__mutmut_37, 
    'x_has_tracking_branch__mutmut_38': x_has_tracking_branch__mutmut_38
}
x_has_tracking_branch__mutmut_orig.__name__ = 'x_has_tracking_branch'


def exclude_from_git_index(repo_path: Path, patterns: list[str]) -> None:
    args = [repo_path, patterns]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_exclude_from_git_index__mutmut_orig, x_exclude_from_git_index__mutmut_mutants, args, kwargs, None)


def x_exclude_from_git_index__mutmut_orig(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_1(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = None
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_2(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" * "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_3(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" * "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_4(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path * ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_5(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / "XX.gitXX" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_6(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".GIT" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_7(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "XXinfoXX" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_8(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "INFO" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_9(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "XXexcludeXX"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_10(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "EXCLUDE"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_11(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_12(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = None
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_13(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(None)
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_14(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = None

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_15(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = None
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_16(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_17(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open(None) as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_18(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("XXaXX") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_19(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("A") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_20(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = None
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_21(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "XX# Added by spec-kitty (local exclusions)XX"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_22(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_23(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# ADDED BY SPEC-KITTY (LOCAL EXCLUSIONS)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_24(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_25(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(None)
                for pattern in new_patterns:
                    f.write(f"{pattern}\n")
        except OSError:
            pass  # Non-critical, continue silently


def x_exclude_from_git_index__mutmut_26(repo_path: Path, patterns: list[str]) -> None:
    """Add patterns to .git/info/exclude to prevent git tracking.

    This is a local-only exclusion (never committed, unlike .gitignore).
    Useful for build artifacts, worktrees, and other local-only files.

    Args:
        repo_path: Repository root path
        patterns: List of patterns to exclude (e.g., [".worktrees/"])
    """
    exclude_file = repo_path / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return

    # Read existing exclusions
    try:
        existing = set(exclude_file.read_text().splitlines())
    except OSError:
        existing = set()

    # Add new patterns
    new_patterns = [p for p in patterns if p not in existing]
    if new_patterns:
        try:
            with exclude_file.open("a") as f:
                marker = "# Added by spec-kitty (local exclusions)"
                if marker not in existing:
                    f.write(f"\n{marker}\n")
                for pattern in new_patterns:
                    f.write(None)
        except OSError:
            pass  # Non-critical, continue silently

x_exclude_from_git_index__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_exclude_from_git_index__mutmut_1': x_exclude_from_git_index__mutmut_1, 
    'x_exclude_from_git_index__mutmut_2': x_exclude_from_git_index__mutmut_2, 
    'x_exclude_from_git_index__mutmut_3': x_exclude_from_git_index__mutmut_3, 
    'x_exclude_from_git_index__mutmut_4': x_exclude_from_git_index__mutmut_4, 
    'x_exclude_from_git_index__mutmut_5': x_exclude_from_git_index__mutmut_5, 
    'x_exclude_from_git_index__mutmut_6': x_exclude_from_git_index__mutmut_6, 
    'x_exclude_from_git_index__mutmut_7': x_exclude_from_git_index__mutmut_7, 
    'x_exclude_from_git_index__mutmut_8': x_exclude_from_git_index__mutmut_8, 
    'x_exclude_from_git_index__mutmut_9': x_exclude_from_git_index__mutmut_9, 
    'x_exclude_from_git_index__mutmut_10': x_exclude_from_git_index__mutmut_10, 
    'x_exclude_from_git_index__mutmut_11': x_exclude_from_git_index__mutmut_11, 
    'x_exclude_from_git_index__mutmut_12': x_exclude_from_git_index__mutmut_12, 
    'x_exclude_from_git_index__mutmut_13': x_exclude_from_git_index__mutmut_13, 
    'x_exclude_from_git_index__mutmut_14': x_exclude_from_git_index__mutmut_14, 
    'x_exclude_from_git_index__mutmut_15': x_exclude_from_git_index__mutmut_15, 
    'x_exclude_from_git_index__mutmut_16': x_exclude_from_git_index__mutmut_16, 
    'x_exclude_from_git_index__mutmut_17': x_exclude_from_git_index__mutmut_17, 
    'x_exclude_from_git_index__mutmut_18': x_exclude_from_git_index__mutmut_18, 
    'x_exclude_from_git_index__mutmut_19': x_exclude_from_git_index__mutmut_19, 
    'x_exclude_from_git_index__mutmut_20': x_exclude_from_git_index__mutmut_20, 
    'x_exclude_from_git_index__mutmut_21': x_exclude_from_git_index__mutmut_21, 
    'x_exclude_from_git_index__mutmut_22': x_exclude_from_git_index__mutmut_22, 
    'x_exclude_from_git_index__mutmut_23': x_exclude_from_git_index__mutmut_23, 
    'x_exclude_from_git_index__mutmut_24': x_exclude_from_git_index__mutmut_24, 
    'x_exclude_from_git_index__mutmut_25': x_exclude_from_git_index__mutmut_25, 
    'x_exclude_from_git_index__mutmut_26': x_exclude_from_git_index__mutmut_26
}
x_exclude_from_git_index__mutmut_orig.__name__ = 'x_exclude_from_git_index'


def resolve_primary_branch(repo_root: Path) -> str:
    args = [repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_resolve_primary_branch__mutmut_orig, x_resolve_primary_branch__mutmut_mutants, args, kwargs, None)


def x_resolve_primary_branch__mutmut_orig(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_1(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = None
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_2(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            None,
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_3(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_4(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_5(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=None,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_6(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding=None,
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_7(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors=None,
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_8(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=None,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_9(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=None,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_10(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_11(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_12(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_13(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_14(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_15(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_16(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_17(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_18(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["XXgitXX", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_19(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["GIT", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_20(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "XXsymbolic-refXX", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_21(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "SYMBOLIC-REF", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_22(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "XXrefs/remotes/origin/HEADXX"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_23(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/head"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_24(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "REFS/REMOTES/ORIGIN/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_25(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_26(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=False,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_27(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_28(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="UTF-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_29(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_30(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_31(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=6,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_32(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=True,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_33(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode != 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_34(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 1:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_35(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = None
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_36(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = None
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_37(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split(None)[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_38(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("XX/XX")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_39(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[+1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_40(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-2]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_41(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = None
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_42(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(None)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_43(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current or current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_44(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current == "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_45(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "XXHEADXX":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_46(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "head":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_47(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["XXmainXX", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_48(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["MAIN", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_49(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "XXmasterXX", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_50(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "MASTER", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_51(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "XXdevelopXX"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_52(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "DEVELOP"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_53(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = None
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_54(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                None,
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_55(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=None,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_56(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=None,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_57(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=None,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_58(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=None,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_59(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_60(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_61(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_62(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_63(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_64(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["XXgitXX", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_65(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["GIT", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_66(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "XXrev-parseXX", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_67(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "REV-PARSE", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_68(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "XX--verifyXX", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_69(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--VERIFY", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_70(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=False,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_71(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=6,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_72(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=True,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_73(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode != 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_74(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 1:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_75(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            break

    # Method 4: Fallback
    return "main"


def x_resolve_primary_branch__mutmut_76(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "XXmainXX"


def x_resolve_primary_branch__mutmut_77(repo_root: Path) -> str:
    """Detect the primary branch name for the repository.

    Tries multiple methods in order:
    1. origin/HEAD symbolic ref (most reliable for cloned repos)
    2. Current branch (the user is standing on it for a reason)
    3. Check which common branch exists (main, master, develop)
    4. Fallback to "main"

    Args:
        repo_root: Repository root path

    Returns:
        Primary branch name (e.g., "main", "master", "develop", "2.x")
    """
    # Method 1: Get from origin's HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            ref = result.stdout.strip()
            if ref:
                branch = ref.split("/")[-1]
                if branch:
                    return branch
    except subprocess.TimeoutExpired:
        pass

    # Method 2: Current branch (the user is standing on it for a reason)
    current = get_current_branch(repo_root)
    if current and current != "HEAD":
        return current

    # Method 3: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                cwd=repo_root,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return branch
        except subprocess.TimeoutExpired:
            continue

    # Method 4: Fallback
    return "MAIN"

x_resolve_primary_branch__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_resolve_primary_branch__mutmut_1': x_resolve_primary_branch__mutmut_1, 
    'x_resolve_primary_branch__mutmut_2': x_resolve_primary_branch__mutmut_2, 
    'x_resolve_primary_branch__mutmut_3': x_resolve_primary_branch__mutmut_3, 
    'x_resolve_primary_branch__mutmut_4': x_resolve_primary_branch__mutmut_4, 
    'x_resolve_primary_branch__mutmut_5': x_resolve_primary_branch__mutmut_5, 
    'x_resolve_primary_branch__mutmut_6': x_resolve_primary_branch__mutmut_6, 
    'x_resolve_primary_branch__mutmut_7': x_resolve_primary_branch__mutmut_7, 
    'x_resolve_primary_branch__mutmut_8': x_resolve_primary_branch__mutmut_8, 
    'x_resolve_primary_branch__mutmut_9': x_resolve_primary_branch__mutmut_9, 
    'x_resolve_primary_branch__mutmut_10': x_resolve_primary_branch__mutmut_10, 
    'x_resolve_primary_branch__mutmut_11': x_resolve_primary_branch__mutmut_11, 
    'x_resolve_primary_branch__mutmut_12': x_resolve_primary_branch__mutmut_12, 
    'x_resolve_primary_branch__mutmut_13': x_resolve_primary_branch__mutmut_13, 
    'x_resolve_primary_branch__mutmut_14': x_resolve_primary_branch__mutmut_14, 
    'x_resolve_primary_branch__mutmut_15': x_resolve_primary_branch__mutmut_15, 
    'x_resolve_primary_branch__mutmut_16': x_resolve_primary_branch__mutmut_16, 
    'x_resolve_primary_branch__mutmut_17': x_resolve_primary_branch__mutmut_17, 
    'x_resolve_primary_branch__mutmut_18': x_resolve_primary_branch__mutmut_18, 
    'x_resolve_primary_branch__mutmut_19': x_resolve_primary_branch__mutmut_19, 
    'x_resolve_primary_branch__mutmut_20': x_resolve_primary_branch__mutmut_20, 
    'x_resolve_primary_branch__mutmut_21': x_resolve_primary_branch__mutmut_21, 
    'x_resolve_primary_branch__mutmut_22': x_resolve_primary_branch__mutmut_22, 
    'x_resolve_primary_branch__mutmut_23': x_resolve_primary_branch__mutmut_23, 
    'x_resolve_primary_branch__mutmut_24': x_resolve_primary_branch__mutmut_24, 
    'x_resolve_primary_branch__mutmut_25': x_resolve_primary_branch__mutmut_25, 
    'x_resolve_primary_branch__mutmut_26': x_resolve_primary_branch__mutmut_26, 
    'x_resolve_primary_branch__mutmut_27': x_resolve_primary_branch__mutmut_27, 
    'x_resolve_primary_branch__mutmut_28': x_resolve_primary_branch__mutmut_28, 
    'x_resolve_primary_branch__mutmut_29': x_resolve_primary_branch__mutmut_29, 
    'x_resolve_primary_branch__mutmut_30': x_resolve_primary_branch__mutmut_30, 
    'x_resolve_primary_branch__mutmut_31': x_resolve_primary_branch__mutmut_31, 
    'x_resolve_primary_branch__mutmut_32': x_resolve_primary_branch__mutmut_32, 
    'x_resolve_primary_branch__mutmut_33': x_resolve_primary_branch__mutmut_33, 
    'x_resolve_primary_branch__mutmut_34': x_resolve_primary_branch__mutmut_34, 
    'x_resolve_primary_branch__mutmut_35': x_resolve_primary_branch__mutmut_35, 
    'x_resolve_primary_branch__mutmut_36': x_resolve_primary_branch__mutmut_36, 
    'x_resolve_primary_branch__mutmut_37': x_resolve_primary_branch__mutmut_37, 
    'x_resolve_primary_branch__mutmut_38': x_resolve_primary_branch__mutmut_38, 
    'x_resolve_primary_branch__mutmut_39': x_resolve_primary_branch__mutmut_39, 
    'x_resolve_primary_branch__mutmut_40': x_resolve_primary_branch__mutmut_40, 
    'x_resolve_primary_branch__mutmut_41': x_resolve_primary_branch__mutmut_41, 
    'x_resolve_primary_branch__mutmut_42': x_resolve_primary_branch__mutmut_42, 
    'x_resolve_primary_branch__mutmut_43': x_resolve_primary_branch__mutmut_43, 
    'x_resolve_primary_branch__mutmut_44': x_resolve_primary_branch__mutmut_44, 
    'x_resolve_primary_branch__mutmut_45': x_resolve_primary_branch__mutmut_45, 
    'x_resolve_primary_branch__mutmut_46': x_resolve_primary_branch__mutmut_46, 
    'x_resolve_primary_branch__mutmut_47': x_resolve_primary_branch__mutmut_47, 
    'x_resolve_primary_branch__mutmut_48': x_resolve_primary_branch__mutmut_48, 
    'x_resolve_primary_branch__mutmut_49': x_resolve_primary_branch__mutmut_49, 
    'x_resolve_primary_branch__mutmut_50': x_resolve_primary_branch__mutmut_50, 
    'x_resolve_primary_branch__mutmut_51': x_resolve_primary_branch__mutmut_51, 
    'x_resolve_primary_branch__mutmut_52': x_resolve_primary_branch__mutmut_52, 
    'x_resolve_primary_branch__mutmut_53': x_resolve_primary_branch__mutmut_53, 
    'x_resolve_primary_branch__mutmut_54': x_resolve_primary_branch__mutmut_54, 
    'x_resolve_primary_branch__mutmut_55': x_resolve_primary_branch__mutmut_55, 
    'x_resolve_primary_branch__mutmut_56': x_resolve_primary_branch__mutmut_56, 
    'x_resolve_primary_branch__mutmut_57': x_resolve_primary_branch__mutmut_57, 
    'x_resolve_primary_branch__mutmut_58': x_resolve_primary_branch__mutmut_58, 
    'x_resolve_primary_branch__mutmut_59': x_resolve_primary_branch__mutmut_59, 
    'x_resolve_primary_branch__mutmut_60': x_resolve_primary_branch__mutmut_60, 
    'x_resolve_primary_branch__mutmut_61': x_resolve_primary_branch__mutmut_61, 
    'x_resolve_primary_branch__mutmut_62': x_resolve_primary_branch__mutmut_62, 
    'x_resolve_primary_branch__mutmut_63': x_resolve_primary_branch__mutmut_63, 
    'x_resolve_primary_branch__mutmut_64': x_resolve_primary_branch__mutmut_64, 
    'x_resolve_primary_branch__mutmut_65': x_resolve_primary_branch__mutmut_65, 
    'x_resolve_primary_branch__mutmut_66': x_resolve_primary_branch__mutmut_66, 
    'x_resolve_primary_branch__mutmut_67': x_resolve_primary_branch__mutmut_67, 
    'x_resolve_primary_branch__mutmut_68': x_resolve_primary_branch__mutmut_68, 
    'x_resolve_primary_branch__mutmut_69': x_resolve_primary_branch__mutmut_69, 
    'x_resolve_primary_branch__mutmut_70': x_resolve_primary_branch__mutmut_70, 
    'x_resolve_primary_branch__mutmut_71': x_resolve_primary_branch__mutmut_71, 
    'x_resolve_primary_branch__mutmut_72': x_resolve_primary_branch__mutmut_72, 
    'x_resolve_primary_branch__mutmut_73': x_resolve_primary_branch__mutmut_73, 
    'x_resolve_primary_branch__mutmut_74': x_resolve_primary_branch__mutmut_74, 
    'x_resolve_primary_branch__mutmut_75': x_resolve_primary_branch__mutmut_75, 
    'x_resolve_primary_branch__mutmut_76': x_resolve_primary_branch__mutmut_76, 
    'x_resolve_primary_branch__mutmut_77': x_resolve_primary_branch__mutmut_77
}
x_resolve_primary_branch__mutmut_orig.__name__ = 'x_resolve_primary_branch'


def resolve_target_branch(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    args = [feature_slug, repo_path, current_branch, respect_current]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_resolve_target_branch__mutmut_orig, x_resolve_target_branch__mutmut_mutants, args, kwargs, None)


def x_resolve_target_branch__mutmut_orig(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_1(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = False,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_2(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is not None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_3(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = None
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_4(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(None)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_5(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is not None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_6(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError(None)

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_7(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("XXCould not determine current branchXX")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_8(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_9(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("COULD NOT DETERMINE CURRENT BRANCH")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_10(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = None
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_11(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug * "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_12(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" * feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_13(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path * "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_14(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "XXkitty-specsXX" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_15(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "KITTY-SPECS" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_16(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "XXmeta.jsonXX"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_17(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "META.JSON"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_18(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = None
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_19(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(None)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_20(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = None
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_21(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = None
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_22(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(None)
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_23(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding=None))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_24(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="XXutf-8XX"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_25(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="UTF-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_26(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = None
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_27(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get(None, fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_28(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", None)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_29(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get(fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_30(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", )
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_31(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("XXtarget_branchXX", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_32(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("TARGET_BRANCH", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_33(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = None

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_34(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch != target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_35(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=None,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_36(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=None,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_37(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=None,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_38(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action=None,
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_39(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_40(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_41(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_42(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_43(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_44(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="XXproceedXX",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_45(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="PROCEED",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_46(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=None,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_47(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=None,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_48(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=None,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_49(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action=None,
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_50(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_51(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_52(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_53(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_54(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_55(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="XXstay_on_currentXX",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_56(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="STAY_ON_CURRENT",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_57(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=None,
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_58(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=None,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_59(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=None,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_60(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action=None,
        )


def x_resolve_target_branch__mutmut_61(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            current=current_branch,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_62(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            should_notify=True,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_63(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_64(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            )


def x_resolve_target_branch__mutmut_65(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="checkout_target",
        )


def x_resolve_target_branch__mutmut_66(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="XXcheckout_targetXX",
        )


def x_resolve_target_branch__mutmut_67(
    feature_slug: str,
    repo_path: Path,
    current_branch: str | None = None,
    respect_current: bool = True,
) -> BranchResolution:
    """Resolve target branch for feature operations without auto-checkout.

    This function unifies branch resolution logic across all CLI commands.
    It respects the user's current branch and never performs auto-checkout
    to main/master without explicit permission.

    Args:
        feature_slug: Feature identifier (e.g., "038-v0-15-0-quality-bugfix-release")
        repo_path: Repository root path
        current_branch: User's current branch (auto-detected if None)
        respect_current: If True, stay on current branch (default behavior)

    Returns:
        BranchResolution with:
        - target: Target branch from meta.json (or "main" fallback)
        - current: User's current branch
        - should_notify: True if current != target (show informational message)
        - action: "proceed" if branches match, "stay_on_current" otherwise

    Example:
        >>> resolution = resolve_target_branch("038-bugfix", repo_root, "develop")
        >>> if resolution.should_notify:
        ...     console.print(f"Note: On '{resolution.current}', target is '{resolution.target}'")
        >>> # Proceed on current branch (no checkout)
    """
    # Auto-detect current branch if not provided
    if current_branch is None:
        current_branch = get_current_branch(repo_path)
        if current_branch is None:
            raise RuntimeError("Could not determine current branch")

    # Read target branch from meta.json
    meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"
    fallback = resolve_primary_branch(repo_path)
    target = fallback
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            target = meta.get("target_branch", fallback)
        except (json.JSONDecodeError, OSError):
            # Fallback to detected primary branch if meta.json is invalid
            target = fallback

    # Check if branches match
    if current_branch == target:
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=False,
            action="proceed",
        )

    # Branches differ
    if respect_current:
        # Stay on current branch, notify user
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="stay_on_current",
        )
    else:
        # Legacy behavior: auto-checkout allowed (not recommended)
        return BranchResolution(
            target=target,
            current=current_branch,
            should_notify=True,
            action="CHECKOUT_TARGET",
        )

x_resolve_target_branch__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_resolve_target_branch__mutmut_1': x_resolve_target_branch__mutmut_1, 
    'x_resolve_target_branch__mutmut_2': x_resolve_target_branch__mutmut_2, 
    'x_resolve_target_branch__mutmut_3': x_resolve_target_branch__mutmut_3, 
    'x_resolve_target_branch__mutmut_4': x_resolve_target_branch__mutmut_4, 
    'x_resolve_target_branch__mutmut_5': x_resolve_target_branch__mutmut_5, 
    'x_resolve_target_branch__mutmut_6': x_resolve_target_branch__mutmut_6, 
    'x_resolve_target_branch__mutmut_7': x_resolve_target_branch__mutmut_7, 
    'x_resolve_target_branch__mutmut_8': x_resolve_target_branch__mutmut_8, 
    'x_resolve_target_branch__mutmut_9': x_resolve_target_branch__mutmut_9, 
    'x_resolve_target_branch__mutmut_10': x_resolve_target_branch__mutmut_10, 
    'x_resolve_target_branch__mutmut_11': x_resolve_target_branch__mutmut_11, 
    'x_resolve_target_branch__mutmut_12': x_resolve_target_branch__mutmut_12, 
    'x_resolve_target_branch__mutmut_13': x_resolve_target_branch__mutmut_13, 
    'x_resolve_target_branch__mutmut_14': x_resolve_target_branch__mutmut_14, 
    'x_resolve_target_branch__mutmut_15': x_resolve_target_branch__mutmut_15, 
    'x_resolve_target_branch__mutmut_16': x_resolve_target_branch__mutmut_16, 
    'x_resolve_target_branch__mutmut_17': x_resolve_target_branch__mutmut_17, 
    'x_resolve_target_branch__mutmut_18': x_resolve_target_branch__mutmut_18, 
    'x_resolve_target_branch__mutmut_19': x_resolve_target_branch__mutmut_19, 
    'x_resolve_target_branch__mutmut_20': x_resolve_target_branch__mutmut_20, 
    'x_resolve_target_branch__mutmut_21': x_resolve_target_branch__mutmut_21, 
    'x_resolve_target_branch__mutmut_22': x_resolve_target_branch__mutmut_22, 
    'x_resolve_target_branch__mutmut_23': x_resolve_target_branch__mutmut_23, 
    'x_resolve_target_branch__mutmut_24': x_resolve_target_branch__mutmut_24, 
    'x_resolve_target_branch__mutmut_25': x_resolve_target_branch__mutmut_25, 
    'x_resolve_target_branch__mutmut_26': x_resolve_target_branch__mutmut_26, 
    'x_resolve_target_branch__mutmut_27': x_resolve_target_branch__mutmut_27, 
    'x_resolve_target_branch__mutmut_28': x_resolve_target_branch__mutmut_28, 
    'x_resolve_target_branch__mutmut_29': x_resolve_target_branch__mutmut_29, 
    'x_resolve_target_branch__mutmut_30': x_resolve_target_branch__mutmut_30, 
    'x_resolve_target_branch__mutmut_31': x_resolve_target_branch__mutmut_31, 
    'x_resolve_target_branch__mutmut_32': x_resolve_target_branch__mutmut_32, 
    'x_resolve_target_branch__mutmut_33': x_resolve_target_branch__mutmut_33, 
    'x_resolve_target_branch__mutmut_34': x_resolve_target_branch__mutmut_34, 
    'x_resolve_target_branch__mutmut_35': x_resolve_target_branch__mutmut_35, 
    'x_resolve_target_branch__mutmut_36': x_resolve_target_branch__mutmut_36, 
    'x_resolve_target_branch__mutmut_37': x_resolve_target_branch__mutmut_37, 
    'x_resolve_target_branch__mutmut_38': x_resolve_target_branch__mutmut_38, 
    'x_resolve_target_branch__mutmut_39': x_resolve_target_branch__mutmut_39, 
    'x_resolve_target_branch__mutmut_40': x_resolve_target_branch__mutmut_40, 
    'x_resolve_target_branch__mutmut_41': x_resolve_target_branch__mutmut_41, 
    'x_resolve_target_branch__mutmut_42': x_resolve_target_branch__mutmut_42, 
    'x_resolve_target_branch__mutmut_43': x_resolve_target_branch__mutmut_43, 
    'x_resolve_target_branch__mutmut_44': x_resolve_target_branch__mutmut_44, 
    'x_resolve_target_branch__mutmut_45': x_resolve_target_branch__mutmut_45, 
    'x_resolve_target_branch__mutmut_46': x_resolve_target_branch__mutmut_46, 
    'x_resolve_target_branch__mutmut_47': x_resolve_target_branch__mutmut_47, 
    'x_resolve_target_branch__mutmut_48': x_resolve_target_branch__mutmut_48, 
    'x_resolve_target_branch__mutmut_49': x_resolve_target_branch__mutmut_49, 
    'x_resolve_target_branch__mutmut_50': x_resolve_target_branch__mutmut_50, 
    'x_resolve_target_branch__mutmut_51': x_resolve_target_branch__mutmut_51, 
    'x_resolve_target_branch__mutmut_52': x_resolve_target_branch__mutmut_52, 
    'x_resolve_target_branch__mutmut_53': x_resolve_target_branch__mutmut_53, 
    'x_resolve_target_branch__mutmut_54': x_resolve_target_branch__mutmut_54, 
    'x_resolve_target_branch__mutmut_55': x_resolve_target_branch__mutmut_55, 
    'x_resolve_target_branch__mutmut_56': x_resolve_target_branch__mutmut_56, 
    'x_resolve_target_branch__mutmut_57': x_resolve_target_branch__mutmut_57, 
    'x_resolve_target_branch__mutmut_58': x_resolve_target_branch__mutmut_58, 
    'x_resolve_target_branch__mutmut_59': x_resolve_target_branch__mutmut_59, 
    'x_resolve_target_branch__mutmut_60': x_resolve_target_branch__mutmut_60, 
    'x_resolve_target_branch__mutmut_61': x_resolve_target_branch__mutmut_61, 
    'x_resolve_target_branch__mutmut_62': x_resolve_target_branch__mutmut_62, 
    'x_resolve_target_branch__mutmut_63': x_resolve_target_branch__mutmut_63, 
    'x_resolve_target_branch__mutmut_64': x_resolve_target_branch__mutmut_64, 
    'x_resolve_target_branch__mutmut_65': x_resolve_target_branch__mutmut_65, 
    'x_resolve_target_branch__mutmut_66': x_resolve_target_branch__mutmut_66, 
    'x_resolve_target_branch__mutmut_67': x_resolve_target_branch__mutmut_67
}
x_resolve_target_branch__mutmut_orig.__name__ = 'x_resolve_target_branch'


__all__ = [
    "BranchResolution",
    "exclude_from_git_index",
    "get_current_branch",
    "has_remote",
    "has_tracking_branch",
    "init_git_repo",
    "is_git_repo",
    "resolve_primary_branch",
    "resolve_target_branch",
    "run_command",
]
