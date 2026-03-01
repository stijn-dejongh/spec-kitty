"""Deterministic git preflight checks for agent and merge workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import shlex
import subprocess

__all__ = [
    "GitPreflightIssue",
    "GitPreflightResult",
    "run_git_preflight",
    "build_git_preflight_failure_payload",
]
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
class GitPreflightIssue:
    """Single preflight issue with optional remediation command."""

    code: str
    check: str
    message: str
    remediation: str
    command: str | None = None

    def to_dict(self) -> dict[str, str]:
        payload = {
            "code": self.code,
            "check": self.check,
            "message": self.message,
            "remediation": self.remediation,
        }
        if self.command:
            payload["command"] = self.command
        return payload


@dataclass
class GitPreflightResult:
    """Result envelope for git preflight checks."""

    repo_root: Path
    errors: list[GitPreflightIssue] = field(default_factory=list)
    warnings: list[GitPreflightIssue] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors

    @property
    def first_error(self) -> GitPreflightIssue | None:
        return self.errors[0] if self.errors else None

    def remediation_commands(self) -> list[str]:
        commands: list[str] = []
        for issue in self.errors:
            if issue.command:
                commands.append(issue.command)
        return commands

    def to_dict(self) -> dict[str, object]:
        return {
            "repo_root": str(self.repo_root),
            "passed": self.passed,
            "errors": [issue.to_dict() for issue in self.errors],
            "warnings": [issue.to_dict() for issue in self.warnings],
        }


@dataclass
class _GitCommandResult:
    returncode: int
    stdout: str
    stderr: str


def _run_git(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    args = [repo_root, args, timeout]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__run_git__mutmut_orig, x__run_git__mutmut_mutants, args, kwargs, None)


def x__run_git__mutmut_orig(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_1(repo_root: Path, args: list[str], timeout: int = 16) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_2(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = None
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_3(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            None,
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_4(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_5(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_6(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=None,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_7(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding=None,
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_8(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors=None,
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_9(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=None,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_10(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=None,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_11(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_12(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_13(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_14(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_15(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_16(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_17(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_18(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_19(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["XXgitXX", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_20(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["GIT", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_21(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(None),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_22(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_23(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=False,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_24(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_25(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="UTF-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_26(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_27(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_28(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_29(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=None,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_30(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=None,
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_31(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=None,
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_32(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_33(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_34(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_35(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout and "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_36(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "XXXX",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_37(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr and "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_38(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "XXXX",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_39(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=None,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_40(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout=None,
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_41(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr=None,
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_42(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_43(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_44(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_45(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=128,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_46(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="XXXX",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_47(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="XXgit executable not found on PATHXX",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_48(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on path",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_49(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="GIT EXECUTABLE NOT FOUND ON PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_50(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=None,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_51(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout=None,
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_52(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=None,
        )


def x__run_git__mutmut_53(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_54(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_55(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            )


def x__run_git__mutmut_56(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=125,
            stdout="",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_57(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="XXXX",
            stderr=f"git command timed out: git {' '.join(args)}",
        )


def x__run_git__mutmut_58(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {' '.join(None)}",
        )


def x__run_git__mutmut_59(repo_root: Path, args: list[str], timeout: int = 15) -> _GitCommandResult:
    """Run git command and normalize failure shape for deterministic handling."""
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return _GitCommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except FileNotFoundError:
        return _GitCommandResult(
            returncode=127,
            stdout="",
            stderr="git executable not found on PATH",
        )
    except subprocess.TimeoutExpired:
        return _GitCommandResult(
            returncode=124,
            stdout="",
            stderr=f"git command timed out: git {'XX XX'.join(args)}",
        )

x__run_git__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__run_git__mutmut_1': x__run_git__mutmut_1, 
    'x__run_git__mutmut_2': x__run_git__mutmut_2, 
    'x__run_git__mutmut_3': x__run_git__mutmut_3, 
    'x__run_git__mutmut_4': x__run_git__mutmut_4, 
    'x__run_git__mutmut_5': x__run_git__mutmut_5, 
    'x__run_git__mutmut_6': x__run_git__mutmut_6, 
    'x__run_git__mutmut_7': x__run_git__mutmut_7, 
    'x__run_git__mutmut_8': x__run_git__mutmut_8, 
    'x__run_git__mutmut_9': x__run_git__mutmut_9, 
    'x__run_git__mutmut_10': x__run_git__mutmut_10, 
    'x__run_git__mutmut_11': x__run_git__mutmut_11, 
    'x__run_git__mutmut_12': x__run_git__mutmut_12, 
    'x__run_git__mutmut_13': x__run_git__mutmut_13, 
    'x__run_git__mutmut_14': x__run_git__mutmut_14, 
    'x__run_git__mutmut_15': x__run_git__mutmut_15, 
    'x__run_git__mutmut_16': x__run_git__mutmut_16, 
    'x__run_git__mutmut_17': x__run_git__mutmut_17, 
    'x__run_git__mutmut_18': x__run_git__mutmut_18, 
    'x__run_git__mutmut_19': x__run_git__mutmut_19, 
    'x__run_git__mutmut_20': x__run_git__mutmut_20, 
    'x__run_git__mutmut_21': x__run_git__mutmut_21, 
    'x__run_git__mutmut_22': x__run_git__mutmut_22, 
    'x__run_git__mutmut_23': x__run_git__mutmut_23, 
    'x__run_git__mutmut_24': x__run_git__mutmut_24, 
    'x__run_git__mutmut_25': x__run_git__mutmut_25, 
    'x__run_git__mutmut_26': x__run_git__mutmut_26, 
    'x__run_git__mutmut_27': x__run_git__mutmut_27, 
    'x__run_git__mutmut_28': x__run_git__mutmut_28, 
    'x__run_git__mutmut_29': x__run_git__mutmut_29, 
    'x__run_git__mutmut_30': x__run_git__mutmut_30, 
    'x__run_git__mutmut_31': x__run_git__mutmut_31, 
    'x__run_git__mutmut_32': x__run_git__mutmut_32, 
    'x__run_git__mutmut_33': x__run_git__mutmut_33, 
    'x__run_git__mutmut_34': x__run_git__mutmut_34, 
    'x__run_git__mutmut_35': x__run_git__mutmut_35, 
    'x__run_git__mutmut_36': x__run_git__mutmut_36, 
    'x__run_git__mutmut_37': x__run_git__mutmut_37, 
    'x__run_git__mutmut_38': x__run_git__mutmut_38, 
    'x__run_git__mutmut_39': x__run_git__mutmut_39, 
    'x__run_git__mutmut_40': x__run_git__mutmut_40, 
    'x__run_git__mutmut_41': x__run_git__mutmut_41, 
    'x__run_git__mutmut_42': x__run_git__mutmut_42, 
    'x__run_git__mutmut_43': x__run_git__mutmut_43, 
    'x__run_git__mutmut_44': x__run_git__mutmut_44, 
    'x__run_git__mutmut_45': x__run_git__mutmut_45, 
    'x__run_git__mutmut_46': x__run_git__mutmut_46, 
    'x__run_git__mutmut_47': x__run_git__mutmut_47, 
    'x__run_git__mutmut_48': x__run_git__mutmut_48, 
    'x__run_git__mutmut_49': x__run_git__mutmut_49, 
    'x__run_git__mutmut_50': x__run_git__mutmut_50, 
    'x__run_git__mutmut_51': x__run_git__mutmut_51, 
    'x__run_git__mutmut_52': x__run_git__mutmut_52, 
    'x__run_git__mutmut_53': x__run_git__mutmut_53, 
    'x__run_git__mutmut_54': x__run_git__mutmut_54, 
    'x__run_git__mutmut_55': x__run_git__mutmut_55, 
    'x__run_git__mutmut_56': x__run_git__mutmut_56, 
    'x__run_git__mutmut_57': x__run_git__mutmut_57, 
    'x__run_git__mutmut_58': x__run_git__mutmut_58, 
    'x__run_git__mutmut_59': x__run_git__mutmut_59
}
x__run_git__mutmut_orig.__name__ = 'x__run_git'


def _is_dubious_ownership(stderr: str) -> bool:
    args = [stderr]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__is_dubious_ownership__mutmut_orig, x__is_dubious_ownership__mutmut_mutants, args, kwargs, None)


def x__is_dubious_ownership__mutmut_orig(stderr: str) -> bool:
    text = stderr.lower()
    return "dubious ownership" in text or "safe.directory" in text


def x__is_dubious_ownership__mutmut_1(stderr: str) -> bool:
    text = None
    return "dubious ownership" in text or "safe.directory" in text


def x__is_dubious_ownership__mutmut_2(stderr: str) -> bool:
    text = stderr.upper()
    return "dubious ownership" in text or "safe.directory" in text


def x__is_dubious_ownership__mutmut_3(stderr: str) -> bool:
    text = stderr.lower()
    return "dubious ownership" in text and "safe.directory" in text


def x__is_dubious_ownership__mutmut_4(stderr: str) -> bool:
    text = stderr.lower()
    return "XXdubious ownershipXX" in text or "safe.directory" in text


def x__is_dubious_ownership__mutmut_5(stderr: str) -> bool:
    text = stderr.lower()
    return "DUBIOUS OWNERSHIP" in text or "safe.directory" in text


def x__is_dubious_ownership__mutmut_6(stderr: str) -> bool:
    text = stderr.lower()
    return "dubious ownership" not in text or "safe.directory" in text


def x__is_dubious_ownership__mutmut_7(stderr: str) -> bool:
    text = stderr.lower()
    return "dubious ownership" in text or "XXsafe.directoryXX" in text


def x__is_dubious_ownership__mutmut_8(stderr: str) -> bool:
    text = stderr.lower()
    return "dubious ownership" in text or "SAFE.DIRECTORY" in text


def x__is_dubious_ownership__mutmut_9(stderr: str) -> bool:
    text = stderr.lower()
    return "dubious ownership" in text or "safe.directory" not in text

x__is_dubious_ownership__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__is_dubious_ownership__mutmut_1': x__is_dubious_ownership__mutmut_1, 
    'x__is_dubious_ownership__mutmut_2': x__is_dubious_ownership__mutmut_2, 
    'x__is_dubious_ownership__mutmut_3': x__is_dubious_ownership__mutmut_3, 
    'x__is_dubious_ownership__mutmut_4': x__is_dubious_ownership__mutmut_4, 
    'x__is_dubious_ownership__mutmut_5': x__is_dubious_ownership__mutmut_5, 
    'x__is_dubious_ownership__mutmut_6': x__is_dubious_ownership__mutmut_6, 
    'x__is_dubious_ownership__mutmut_7': x__is_dubious_ownership__mutmut_7, 
    'x__is_dubious_ownership__mutmut_8': x__is_dubious_ownership__mutmut_8, 
    'x__is_dubious_ownership__mutmut_9': x__is_dubious_ownership__mutmut_9
}
x__is_dubious_ownership__mutmut_orig.__name__ = 'x__is_dubious_ownership'


def _safe_directory_command(repo_root: Path) -> str:
    args = [repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__safe_directory_command__mutmut_orig, x__safe_directory_command__mutmut_mutants, args, kwargs, None)


def x__safe_directory_command__mutmut_orig(repo_root: Path) -> str:
    return f"git config --global --add safe.directory {shlex.quote(str(repo_root))}"


def x__safe_directory_command__mutmut_1(repo_root: Path) -> str:
    return f"git config --global --add safe.directory {shlex.quote(None)}"


def x__safe_directory_command__mutmut_2(repo_root: Path) -> str:
    return f"git config --global --add safe.directory {shlex.quote(str(None))}"

x__safe_directory_command__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__safe_directory_command__mutmut_1': x__safe_directory_command__mutmut_1, 
    'x__safe_directory_command__mutmut_2': x__safe_directory_command__mutmut_2
}
x__safe_directory_command__mutmut_orig.__name__ = 'x__safe_directory_command'


def _first_line(text: str) -> str:
    args = [text]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__first_line__mutmut_orig, x__first_line__mutmut_mutants, args, kwargs, None)


def x__first_line__mutmut_orig(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def x__first_line__mutmut_1(text: str) -> str:
    for line in text.splitlines():
        stripped = None
        if stripped:
            return stripped
    return ""


def x__first_line__mutmut_2(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return "XXXX"

x__first_line__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__first_line__mutmut_1': x__first_line__mutmut_1, 
    'x__first_line__mutmut_2': x__first_line__mutmut_2
}
x__first_line__mutmut_orig.__name__ = 'x__first_line'


def run_git_preflight(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    args = [repo_root]# type: ignore
    kwargs = {'check_worktree_list': check_worktree_list}# type: ignore
    return _mutmut_trampoline(x_run_git_preflight__mutmut_orig, x_run_git_preflight__mutmut_mutants, args, kwargs, None)


def x_run_git_preflight__mutmut_orig(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_1(
    repo_root: Path,
    *,
    check_worktree_list: bool = False,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_2(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = None
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_3(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = None

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_4(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=None)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_5(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = None
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_6(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(None, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_7(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, None)
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_8(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_9(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, )
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_10(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["XXrev-parseXX", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_11(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["REV-PARSE", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_12(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "XX--is-inside-work-treeXX"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_13(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--IS-INSIDE-WORK-TREE"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_14(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 and repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_15(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode == 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_16(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 1 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_17(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().upper() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_18(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() == "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_19(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "XXtrueXX":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_20(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "TRUE":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_21(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(None):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_22(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                None
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_23(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code=None,
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_24(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check=None,
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_25(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message=None,
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_26(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation=None,
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_27(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=None,
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_28(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_29(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_30(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_31(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_32(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_33(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="XXUNTRUSTED_REPOSITORYXX",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_34(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="untrusted_repository",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_35(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="XXrepository_trustXX",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_36(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="REPOSITORY_TRUST",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_37(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="XXGit rejected repository ownership trust (safe.directory).XX",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_38(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_39(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="GIT REJECTED REPOSITORY OWNERSHIP TRUST (SAFE.DIRECTORY).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_40(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="XXMark the repository as trusted for this machine.XX",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_41(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_42(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="MARK THE REPOSITORY AS TRUSTED FOR THIS MACHINE.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_43(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(None),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_44(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = None
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_45(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) and "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_46(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(None) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_47(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "XXRepository is not recognized by git.XX"
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_48(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_49(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "REPOSITORY IS NOT RECOGNIZED BY GIT."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_50(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                None
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_51(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code=None,
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_52(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check=None,
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_53(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=None,
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_54(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation=None,
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_55(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=None,
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_56(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_57(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_58(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_59(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_60(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_61(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="XXNOT_A_GIT_REPOSITORYXX",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_62(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="not_a_git_repository",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_63(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="XXrepository_presenceXX",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_64(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="REPOSITORY_PRESENCE",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_65(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="XXRun command from the repository root or set SPECIFY_REPO_ROOT.XX",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_66(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="run command from the repository root or set specify_repo_root.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_67(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="RUN COMMAND FROM THE REPOSITORY ROOT OR SET SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_68(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(None)} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_69(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(None))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_70(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = None
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_71(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(None, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_72(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, None)
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_73(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_74(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, )
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_75(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["XXworktreeXX", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_76(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["WORKTREE", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_77(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "XXlistXX", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_78(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "LIST", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_79(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "XX--porcelainXX"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_80(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--PORCELAIN"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_81(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode == 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_82(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 1:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_83(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(None):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_84(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    None
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_85(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code=None,
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_86(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check=None,
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_87(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message=None,
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_88(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation=None,
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_89(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=None,
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_90(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_91(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_92(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_93(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_94(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_95(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="XXUNTRUSTED_REPOSITORYXX",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_96(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="untrusted_repository",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_97(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="XXrepository_trustXX",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_98(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="REPOSITORY_TRUST",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_99(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="XXGit rejected repository ownership trust while listing worktrees.XX",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_100(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_101(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="GIT REJECTED REPOSITORY OWNERSHIP TRUST WHILE LISTING WORKTREES.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_102(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="XXMark the repository as trusted for this machine.XX",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_103(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_104(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="MARK THE REPOSITORY AS TRUSTED FOR THIS MACHINE.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_105(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(None),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_106(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = None
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_107(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) and "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_108(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(None) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_109(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "XXUnable to enumerate git worktrees.XX"
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_110(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_111(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "UNABLE TO ENUMERATE GIT WORKTREES."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_112(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    None
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_113(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code=None,
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_114(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check=None,
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_115(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=None,
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_116(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation=None,
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_117(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=None,
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_118(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_119(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_120(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_121(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_122(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_123(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="XXWORKTREE_LIST_FAILEDXX",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_124(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="worktree_list_failed",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_125(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="XXworktree_listingXX",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_126(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="WORKTREE_LISTING",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_127(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="XXRun the worktree listing command from the primary checkout root.XX",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_128(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_129(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="RUN THE WORKTREE LISTING COMMAND FROM THE PRIMARY CHECKOUT ROOT.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_130(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(None)} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_131(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(None))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_132(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = None
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_133(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(None, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_134(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, None)
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_135(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_136(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, )
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_137(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["XXremoteXX", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_138(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["REMOTE", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_139(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "XXget-urlXX", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_140(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "GET-URL", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_141(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "XXoriginXX"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_142(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "ORIGIN"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_143(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode == 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_144(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 1:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_145(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            None
        )

    return result


def x_run_git_preflight__mutmut_146(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code=None,
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_147(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check=None,
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_148(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message=None,
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_149(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation=None,
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_150(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=None,
            )
        )

    return result


def x_run_git_preflight__mutmut_151(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_152(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_153(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_154(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_155(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                )
        )

    return result


def x_run_git_preflight__mutmut_156(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="XXMISSING_ORIGIN_REMOTEXX",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_157(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="missing_origin_remote",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_158(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="XXremote_originXX",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_159(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="REMOTE_ORIGIN",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_160(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="XXRemote 'origin' is not configured; fetch/push steps may be skipped.XX",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_161(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_162(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="REMOTE 'ORIGIN' IS NOT CONFIGURED; FETCH/PUSH STEPS MAY BE SKIPPED.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_163(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="XXConfigure origin if remote sync is required.XX",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_164(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_165(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="CONFIGURE ORIGIN IF REMOTE SYNC IS REQUIRED.",
                command=f"git -C {shlex.quote(str(root))} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_166(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(None)} remote add origin <url>",
            )
        )

    return result


def x_run_git_preflight__mutmut_167(
    repo_root: Path,
    *,
    check_worktree_list: bool = True,
) -> GitPreflightResult:
    """Run deterministic git preflight checks with actionable remediation."""
    root = repo_root.resolve()
    result = GitPreflightResult(repo_root=root)

    repo_check = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo_check.returncode != 0 or repo_check.stdout.strip().lower() != "true":
        if _is_dubious_ownership(repo_check.stderr):
            result.errors.append(
                GitPreflightIssue(
                    code="UNTRUSTED_REPOSITORY",
                    check="repository_trust",
                    message="Git rejected repository ownership trust (safe.directory).",
                    remediation="Mark the repository as trusted for this machine.",
                    command=_safe_directory_command(root),
                )
            )
        else:
            detail = _first_line(repo_check.stderr) or "Repository is not recognized by git."
            result.errors.append(
                GitPreflightIssue(
                    code="NOT_A_GIT_REPOSITORY",
                    check="repository_presence",
                    message=f"Git repository check failed: {detail}",
                    remediation="Run command from the repository root or set SPECIFY_REPO_ROOT.",
                    command=f"cd {shlex.quote(str(root))} && git status",
                )
            )
        return result

    if check_worktree_list:
        worktree_check = _run_git(root, ["worktree", "list", "--porcelain"])
        if worktree_check.returncode != 0:
            if _is_dubious_ownership(worktree_check.stderr):
                result.errors.append(
                    GitPreflightIssue(
                        code="UNTRUSTED_REPOSITORY",
                        check="repository_trust",
                        message="Git rejected repository ownership trust while listing worktrees.",
                        remediation="Mark the repository as trusted for this machine.",
                        command=_safe_directory_command(root),
                    )
                )
            else:
                detail = _first_line(worktree_check.stderr) or "Unable to enumerate git worktrees."
                result.errors.append(
                    GitPreflightIssue(
                        code="WORKTREE_LIST_FAILED",
                        check="worktree_listing",
                        message=f"Git worktree discovery failed: {detail}",
                        remediation="Run the worktree listing command from the primary checkout root.",
                        command=f"git -C {shlex.quote(str(root))} worktree list --porcelain",
                    )
                )
            return result

    origin_check = _run_git(root, ["remote", "get-url", "origin"])
    if origin_check.returncode != 0:
        result.warnings.append(
            GitPreflightIssue(
                code="MISSING_ORIGIN_REMOTE",
                check="remote_origin",
                message="Remote 'origin' is not configured; fetch/push steps may be skipped.",
                remediation="Configure origin if remote sync is required.",
                command=f"git -C {shlex.quote(str(None))} remote add origin <url>",
            )
        )

    return result

x_run_git_preflight__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_run_git_preflight__mutmut_1': x_run_git_preflight__mutmut_1, 
    'x_run_git_preflight__mutmut_2': x_run_git_preflight__mutmut_2, 
    'x_run_git_preflight__mutmut_3': x_run_git_preflight__mutmut_3, 
    'x_run_git_preflight__mutmut_4': x_run_git_preflight__mutmut_4, 
    'x_run_git_preflight__mutmut_5': x_run_git_preflight__mutmut_5, 
    'x_run_git_preflight__mutmut_6': x_run_git_preflight__mutmut_6, 
    'x_run_git_preflight__mutmut_7': x_run_git_preflight__mutmut_7, 
    'x_run_git_preflight__mutmut_8': x_run_git_preflight__mutmut_8, 
    'x_run_git_preflight__mutmut_9': x_run_git_preflight__mutmut_9, 
    'x_run_git_preflight__mutmut_10': x_run_git_preflight__mutmut_10, 
    'x_run_git_preflight__mutmut_11': x_run_git_preflight__mutmut_11, 
    'x_run_git_preflight__mutmut_12': x_run_git_preflight__mutmut_12, 
    'x_run_git_preflight__mutmut_13': x_run_git_preflight__mutmut_13, 
    'x_run_git_preflight__mutmut_14': x_run_git_preflight__mutmut_14, 
    'x_run_git_preflight__mutmut_15': x_run_git_preflight__mutmut_15, 
    'x_run_git_preflight__mutmut_16': x_run_git_preflight__mutmut_16, 
    'x_run_git_preflight__mutmut_17': x_run_git_preflight__mutmut_17, 
    'x_run_git_preflight__mutmut_18': x_run_git_preflight__mutmut_18, 
    'x_run_git_preflight__mutmut_19': x_run_git_preflight__mutmut_19, 
    'x_run_git_preflight__mutmut_20': x_run_git_preflight__mutmut_20, 
    'x_run_git_preflight__mutmut_21': x_run_git_preflight__mutmut_21, 
    'x_run_git_preflight__mutmut_22': x_run_git_preflight__mutmut_22, 
    'x_run_git_preflight__mutmut_23': x_run_git_preflight__mutmut_23, 
    'x_run_git_preflight__mutmut_24': x_run_git_preflight__mutmut_24, 
    'x_run_git_preflight__mutmut_25': x_run_git_preflight__mutmut_25, 
    'x_run_git_preflight__mutmut_26': x_run_git_preflight__mutmut_26, 
    'x_run_git_preflight__mutmut_27': x_run_git_preflight__mutmut_27, 
    'x_run_git_preflight__mutmut_28': x_run_git_preflight__mutmut_28, 
    'x_run_git_preflight__mutmut_29': x_run_git_preflight__mutmut_29, 
    'x_run_git_preflight__mutmut_30': x_run_git_preflight__mutmut_30, 
    'x_run_git_preflight__mutmut_31': x_run_git_preflight__mutmut_31, 
    'x_run_git_preflight__mutmut_32': x_run_git_preflight__mutmut_32, 
    'x_run_git_preflight__mutmut_33': x_run_git_preflight__mutmut_33, 
    'x_run_git_preflight__mutmut_34': x_run_git_preflight__mutmut_34, 
    'x_run_git_preflight__mutmut_35': x_run_git_preflight__mutmut_35, 
    'x_run_git_preflight__mutmut_36': x_run_git_preflight__mutmut_36, 
    'x_run_git_preflight__mutmut_37': x_run_git_preflight__mutmut_37, 
    'x_run_git_preflight__mutmut_38': x_run_git_preflight__mutmut_38, 
    'x_run_git_preflight__mutmut_39': x_run_git_preflight__mutmut_39, 
    'x_run_git_preflight__mutmut_40': x_run_git_preflight__mutmut_40, 
    'x_run_git_preflight__mutmut_41': x_run_git_preflight__mutmut_41, 
    'x_run_git_preflight__mutmut_42': x_run_git_preflight__mutmut_42, 
    'x_run_git_preflight__mutmut_43': x_run_git_preflight__mutmut_43, 
    'x_run_git_preflight__mutmut_44': x_run_git_preflight__mutmut_44, 
    'x_run_git_preflight__mutmut_45': x_run_git_preflight__mutmut_45, 
    'x_run_git_preflight__mutmut_46': x_run_git_preflight__mutmut_46, 
    'x_run_git_preflight__mutmut_47': x_run_git_preflight__mutmut_47, 
    'x_run_git_preflight__mutmut_48': x_run_git_preflight__mutmut_48, 
    'x_run_git_preflight__mutmut_49': x_run_git_preflight__mutmut_49, 
    'x_run_git_preflight__mutmut_50': x_run_git_preflight__mutmut_50, 
    'x_run_git_preflight__mutmut_51': x_run_git_preflight__mutmut_51, 
    'x_run_git_preflight__mutmut_52': x_run_git_preflight__mutmut_52, 
    'x_run_git_preflight__mutmut_53': x_run_git_preflight__mutmut_53, 
    'x_run_git_preflight__mutmut_54': x_run_git_preflight__mutmut_54, 
    'x_run_git_preflight__mutmut_55': x_run_git_preflight__mutmut_55, 
    'x_run_git_preflight__mutmut_56': x_run_git_preflight__mutmut_56, 
    'x_run_git_preflight__mutmut_57': x_run_git_preflight__mutmut_57, 
    'x_run_git_preflight__mutmut_58': x_run_git_preflight__mutmut_58, 
    'x_run_git_preflight__mutmut_59': x_run_git_preflight__mutmut_59, 
    'x_run_git_preflight__mutmut_60': x_run_git_preflight__mutmut_60, 
    'x_run_git_preflight__mutmut_61': x_run_git_preflight__mutmut_61, 
    'x_run_git_preflight__mutmut_62': x_run_git_preflight__mutmut_62, 
    'x_run_git_preflight__mutmut_63': x_run_git_preflight__mutmut_63, 
    'x_run_git_preflight__mutmut_64': x_run_git_preflight__mutmut_64, 
    'x_run_git_preflight__mutmut_65': x_run_git_preflight__mutmut_65, 
    'x_run_git_preflight__mutmut_66': x_run_git_preflight__mutmut_66, 
    'x_run_git_preflight__mutmut_67': x_run_git_preflight__mutmut_67, 
    'x_run_git_preflight__mutmut_68': x_run_git_preflight__mutmut_68, 
    'x_run_git_preflight__mutmut_69': x_run_git_preflight__mutmut_69, 
    'x_run_git_preflight__mutmut_70': x_run_git_preflight__mutmut_70, 
    'x_run_git_preflight__mutmut_71': x_run_git_preflight__mutmut_71, 
    'x_run_git_preflight__mutmut_72': x_run_git_preflight__mutmut_72, 
    'x_run_git_preflight__mutmut_73': x_run_git_preflight__mutmut_73, 
    'x_run_git_preflight__mutmut_74': x_run_git_preflight__mutmut_74, 
    'x_run_git_preflight__mutmut_75': x_run_git_preflight__mutmut_75, 
    'x_run_git_preflight__mutmut_76': x_run_git_preflight__mutmut_76, 
    'x_run_git_preflight__mutmut_77': x_run_git_preflight__mutmut_77, 
    'x_run_git_preflight__mutmut_78': x_run_git_preflight__mutmut_78, 
    'x_run_git_preflight__mutmut_79': x_run_git_preflight__mutmut_79, 
    'x_run_git_preflight__mutmut_80': x_run_git_preflight__mutmut_80, 
    'x_run_git_preflight__mutmut_81': x_run_git_preflight__mutmut_81, 
    'x_run_git_preflight__mutmut_82': x_run_git_preflight__mutmut_82, 
    'x_run_git_preflight__mutmut_83': x_run_git_preflight__mutmut_83, 
    'x_run_git_preflight__mutmut_84': x_run_git_preflight__mutmut_84, 
    'x_run_git_preflight__mutmut_85': x_run_git_preflight__mutmut_85, 
    'x_run_git_preflight__mutmut_86': x_run_git_preflight__mutmut_86, 
    'x_run_git_preflight__mutmut_87': x_run_git_preflight__mutmut_87, 
    'x_run_git_preflight__mutmut_88': x_run_git_preflight__mutmut_88, 
    'x_run_git_preflight__mutmut_89': x_run_git_preflight__mutmut_89, 
    'x_run_git_preflight__mutmut_90': x_run_git_preflight__mutmut_90, 
    'x_run_git_preflight__mutmut_91': x_run_git_preflight__mutmut_91, 
    'x_run_git_preflight__mutmut_92': x_run_git_preflight__mutmut_92, 
    'x_run_git_preflight__mutmut_93': x_run_git_preflight__mutmut_93, 
    'x_run_git_preflight__mutmut_94': x_run_git_preflight__mutmut_94, 
    'x_run_git_preflight__mutmut_95': x_run_git_preflight__mutmut_95, 
    'x_run_git_preflight__mutmut_96': x_run_git_preflight__mutmut_96, 
    'x_run_git_preflight__mutmut_97': x_run_git_preflight__mutmut_97, 
    'x_run_git_preflight__mutmut_98': x_run_git_preflight__mutmut_98, 
    'x_run_git_preflight__mutmut_99': x_run_git_preflight__mutmut_99, 
    'x_run_git_preflight__mutmut_100': x_run_git_preflight__mutmut_100, 
    'x_run_git_preflight__mutmut_101': x_run_git_preflight__mutmut_101, 
    'x_run_git_preflight__mutmut_102': x_run_git_preflight__mutmut_102, 
    'x_run_git_preflight__mutmut_103': x_run_git_preflight__mutmut_103, 
    'x_run_git_preflight__mutmut_104': x_run_git_preflight__mutmut_104, 
    'x_run_git_preflight__mutmut_105': x_run_git_preflight__mutmut_105, 
    'x_run_git_preflight__mutmut_106': x_run_git_preflight__mutmut_106, 
    'x_run_git_preflight__mutmut_107': x_run_git_preflight__mutmut_107, 
    'x_run_git_preflight__mutmut_108': x_run_git_preflight__mutmut_108, 
    'x_run_git_preflight__mutmut_109': x_run_git_preflight__mutmut_109, 
    'x_run_git_preflight__mutmut_110': x_run_git_preflight__mutmut_110, 
    'x_run_git_preflight__mutmut_111': x_run_git_preflight__mutmut_111, 
    'x_run_git_preflight__mutmut_112': x_run_git_preflight__mutmut_112, 
    'x_run_git_preflight__mutmut_113': x_run_git_preflight__mutmut_113, 
    'x_run_git_preflight__mutmut_114': x_run_git_preflight__mutmut_114, 
    'x_run_git_preflight__mutmut_115': x_run_git_preflight__mutmut_115, 
    'x_run_git_preflight__mutmut_116': x_run_git_preflight__mutmut_116, 
    'x_run_git_preflight__mutmut_117': x_run_git_preflight__mutmut_117, 
    'x_run_git_preflight__mutmut_118': x_run_git_preflight__mutmut_118, 
    'x_run_git_preflight__mutmut_119': x_run_git_preflight__mutmut_119, 
    'x_run_git_preflight__mutmut_120': x_run_git_preflight__mutmut_120, 
    'x_run_git_preflight__mutmut_121': x_run_git_preflight__mutmut_121, 
    'x_run_git_preflight__mutmut_122': x_run_git_preflight__mutmut_122, 
    'x_run_git_preflight__mutmut_123': x_run_git_preflight__mutmut_123, 
    'x_run_git_preflight__mutmut_124': x_run_git_preflight__mutmut_124, 
    'x_run_git_preflight__mutmut_125': x_run_git_preflight__mutmut_125, 
    'x_run_git_preflight__mutmut_126': x_run_git_preflight__mutmut_126, 
    'x_run_git_preflight__mutmut_127': x_run_git_preflight__mutmut_127, 
    'x_run_git_preflight__mutmut_128': x_run_git_preflight__mutmut_128, 
    'x_run_git_preflight__mutmut_129': x_run_git_preflight__mutmut_129, 
    'x_run_git_preflight__mutmut_130': x_run_git_preflight__mutmut_130, 
    'x_run_git_preflight__mutmut_131': x_run_git_preflight__mutmut_131, 
    'x_run_git_preflight__mutmut_132': x_run_git_preflight__mutmut_132, 
    'x_run_git_preflight__mutmut_133': x_run_git_preflight__mutmut_133, 
    'x_run_git_preflight__mutmut_134': x_run_git_preflight__mutmut_134, 
    'x_run_git_preflight__mutmut_135': x_run_git_preflight__mutmut_135, 
    'x_run_git_preflight__mutmut_136': x_run_git_preflight__mutmut_136, 
    'x_run_git_preflight__mutmut_137': x_run_git_preflight__mutmut_137, 
    'x_run_git_preflight__mutmut_138': x_run_git_preflight__mutmut_138, 
    'x_run_git_preflight__mutmut_139': x_run_git_preflight__mutmut_139, 
    'x_run_git_preflight__mutmut_140': x_run_git_preflight__mutmut_140, 
    'x_run_git_preflight__mutmut_141': x_run_git_preflight__mutmut_141, 
    'x_run_git_preflight__mutmut_142': x_run_git_preflight__mutmut_142, 
    'x_run_git_preflight__mutmut_143': x_run_git_preflight__mutmut_143, 
    'x_run_git_preflight__mutmut_144': x_run_git_preflight__mutmut_144, 
    'x_run_git_preflight__mutmut_145': x_run_git_preflight__mutmut_145, 
    'x_run_git_preflight__mutmut_146': x_run_git_preflight__mutmut_146, 
    'x_run_git_preflight__mutmut_147': x_run_git_preflight__mutmut_147, 
    'x_run_git_preflight__mutmut_148': x_run_git_preflight__mutmut_148, 
    'x_run_git_preflight__mutmut_149': x_run_git_preflight__mutmut_149, 
    'x_run_git_preflight__mutmut_150': x_run_git_preflight__mutmut_150, 
    'x_run_git_preflight__mutmut_151': x_run_git_preflight__mutmut_151, 
    'x_run_git_preflight__mutmut_152': x_run_git_preflight__mutmut_152, 
    'x_run_git_preflight__mutmut_153': x_run_git_preflight__mutmut_153, 
    'x_run_git_preflight__mutmut_154': x_run_git_preflight__mutmut_154, 
    'x_run_git_preflight__mutmut_155': x_run_git_preflight__mutmut_155, 
    'x_run_git_preflight__mutmut_156': x_run_git_preflight__mutmut_156, 
    'x_run_git_preflight__mutmut_157': x_run_git_preflight__mutmut_157, 
    'x_run_git_preflight__mutmut_158': x_run_git_preflight__mutmut_158, 
    'x_run_git_preflight__mutmut_159': x_run_git_preflight__mutmut_159, 
    'x_run_git_preflight__mutmut_160': x_run_git_preflight__mutmut_160, 
    'x_run_git_preflight__mutmut_161': x_run_git_preflight__mutmut_161, 
    'x_run_git_preflight__mutmut_162': x_run_git_preflight__mutmut_162, 
    'x_run_git_preflight__mutmut_163': x_run_git_preflight__mutmut_163, 
    'x_run_git_preflight__mutmut_164': x_run_git_preflight__mutmut_164, 
    'x_run_git_preflight__mutmut_165': x_run_git_preflight__mutmut_165, 
    'x_run_git_preflight__mutmut_166': x_run_git_preflight__mutmut_166, 
    'x_run_git_preflight__mutmut_167': x_run_git_preflight__mutmut_167
}
x_run_git_preflight__mutmut_orig.__name__ = 'x_run_git_preflight'


def build_git_preflight_failure_payload(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    args = [preflight]# type: ignore
    kwargs = {'command_name': command_name}# type: ignore
    return _mutmut_trampoline(x_build_git_preflight_failure_payload__mutmut_orig, x_build_git_preflight_failure_payload__mutmut_mutants, args, kwargs, None)


def x_build_git_preflight_failure_payload__mutmut_orig(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_1(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = None
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_2(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = None
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_3(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "XXGit preflight failed.XX"
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_4(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_5(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "GIT PREFLIGHT FAILED."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_6(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "XXerror_codeXX": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_7(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "ERROR_CODE": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_8(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "XXGIT_PREFLIGHT_FAILEDXX",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_9(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "git_preflight_failed",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_10(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "XXerrorXX": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_11(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "ERROR": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_12(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "XXcommandXX": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_13(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "COMMAND": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_14(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "XXrepo_rootXX": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_15(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "REPO_ROOT": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_16(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "repo_root": str(None),
        "preflight": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_17(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "XXpreflightXX": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_18(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "PREFLIGHT": preflight.to_dict(),
        "remediation": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_19(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "XXremediationXX": preflight.remediation_commands(),
    }


def x_build_git_preflight_failure_payload__mutmut_20(
    preflight: GitPreflightResult,
    *,
    command_name: str,
) -> dict[str, object]:
    """Build deterministic JSON payload for preflight failures."""
    primary = preflight.first_error
    message = primary.message if primary else "Git preflight failed."
    return {
        "error_code": "GIT_PREFLIGHT_FAILED",
        "error": message,
        "command": command_name,
        "repo_root": str(preflight.repo_root),
        "preflight": preflight.to_dict(),
        "REMEDIATION": preflight.remediation_commands(),
    }

x_build_git_preflight_failure_payload__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_build_git_preflight_failure_payload__mutmut_1': x_build_git_preflight_failure_payload__mutmut_1, 
    'x_build_git_preflight_failure_payload__mutmut_2': x_build_git_preflight_failure_payload__mutmut_2, 
    'x_build_git_preflight_failure_payload__mutmut_3': x_build_git_preflight_failure_payload__mutmut_3, 
    'x_build_git_preflight_failure_payload__mutmut_4': x_build_git_preflight_failure_payload__mutmut_4, 
    'x_build_git_preflight_failure_payload__mutmut_5': x_build_git_preflight_failure_payload__mutmut_5, 
    'x_build_git_preflight_failure_payload__mutmut_6': x_build_git_preflight_failure_payload__mutmut_6, 
    'x_build_git_preflight_failure_payload__mutmut_7': x_build_git_preflight_failure_payload__mutmut_7, 
    'x_build_git_preflight_failure_payload__mutmut_8': x_build_git_preflight_failure_payload__mutmut_8, 
    'x_build_git_preflight_failure_payload__mutmut_9': x_build_git_preflight_failure_payload__mutmut_9, 
    'x_build_git_preflight_failure_payload__mutmut_10': x_build_git_preflight_failure_payload__mutmut_10, 
    'x_build_git_preflight_failure_payload__mutmut_11': x_build_git_preflight_failure_payload__mutmut_11, 
    'x_build_git_preflight_failure_payload__mutmut_12': x_build_git_preflight_failure_payload__mutmut_12, 
    'x_build_git_preflight_failure_payload__mutmut_13': x_build_git_preflight_failure_payload__mutmut_13, 
    'x_build_git_preflight_failure_payload__mutmut_14': x_build_git_preflight_failure_payload__mutmut_14, 
    'x_build_git_preflight_failure_payload__mutmut_15': x_build_git_preflight_failure_payload__mutmut_15, 
    'x_build_git_preflight_failure_payload__mutmut_16': x_build_git_preflight_failure_payload__mutmut_16, 
    'x_build_git_preflight_failure_payload__mutmut_17': x_build_git_preflight_failure_payload__mutmut_17, 
    'x_build_git_preflight_failure_payload__mutmut_18': x_build_git_preflight_failure_payload__mutmut_18, 
    'x_build_git_preflight_failure_payload__mutmut_19': x_build_git_preflight_failure_payload__mutmut_19, 
    'x_build_git_preflight_failure_payload__mutmut_20': x_build_git_preflight_failure_payload__mutmut_20
}
x_build_git_preflight_failure_payload__mutmut_orig.__name__ = 'x_build_git_preflight_failure_payload'
