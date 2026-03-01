"""JSONL event store for status events.

Provides append-only persistence of StatusEvent records to a JSONL file
(status.events.jsonl). Each line is a JSON object with deterministic
(sorted) key ordering.
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import StatusEvent

EVENTS_FILENAME = "status.events.jsonl"
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


class StoreError(Exception):
    """Raised when the event store encounters corruption or I/O errors."""


def _events_path(feature_dir: Path) -> Path:
    args = [feature_dir]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__events_path__mutmut_orig, x__events_path__mutmut_mutants, args, kwargs, None)


def x__events_path__mutmut_orig(feature_dir: Path) -> Path:
    """Return the canonical path to the events JSONL file."""
    return feature_dir / EVENTS_FILENAME


def x__events_path__mutmut_1(feature_dir: Path) -> Path:
    """Return the canonical path to the events JSONL file."""
    return feature_dir * EVENTS_FILENAME

x__events_path__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__events_path__mutmut_1': x__events_path__mutmut_1
}
x__events_path__mutmut_orig.__name__ = 'x__events_path'


def append_event(feature_dir: Path, event: StatusEvent) -> None:
    args = [feature_dir, event]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_append_event__mutmut_orig, x_append_event__mutmut_mutants, args, kwargs, None)


def x_append_event__mutmut_orig(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_1(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = None
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_2(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(None)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_3(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=None, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_4(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=None)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_5(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_6(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, )
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_7(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=False, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_8(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=False)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_9(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = None
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_10(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(None, sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_11(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=None)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_12(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_13(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), )
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_14(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=False)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_15(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open(None, encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_16(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding=None) as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_17(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open(encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_18(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", ) as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_19(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("XXaXX", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_20(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("A", encoding="utf-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_21(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="XXutf-8XX") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_22(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="UTF-8") as fh:
        fh.write(line + "\n")


def x_append_event__mutmut_23(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(None)


def x_append_event__mutmut_24(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line - "\n")


def x_append_event__mutmut_25(feature_dir: Path, event: StatusEvent) -> None:
    """Atomically append a StatusEvent as a single JSON line.

    Creates parent directories and the file if they do not exist.
    Uses ``sort_keys=True`` for deterministic key ordering.
    """
    path = _events_path(feature_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event.to_dict(), sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "XX\nXX")

x_append_event__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_append_event__mutmut_1': x_append_event__mutmut_1, 
    'x_append_event__mutmut_2': x_append_event__mutmut_2, 
    'x_append_event__mutmut_3': x_append_event__mutmut_3, 
    'x_append_event__mutmut_4': x_append_event__mutmut_4, 
    'x_append_event__mutmut_5': x_append_event__mutmut_5, 
    'x_append_event__mutmut_6': x_append_event__mutmut_6, 
    'x_append_event__mutmut_7': x_append_event__mutmut_7, 
    'x_append_event__mutmut_8': x_append_event__mutmut_8, 
    'x_append_event__mutmut_9': x_append_event__mutmut_9, 
    'x_append_event__mutmut_10': x_append_event__mutmut_10, 
    'x_append_event__mutmut_11': x_append_event__mutmut_11, 
    'x_append_event__mutmut_12': x_append_event__mutmut_12, 
    'x_append_event__mutmut_13': x_append_event__mutmut_13, 
    'x_append_event__mutmut_14': x_append_event__mutmut_14, 
    'x_append_event__mutmut_15': x_append_event__mutmut_15, 
    'x_append_event__mutmut_16': x_append_event__mutmut_16, 
    'x_append_event__mutmut_17': x_append_event__mutmut_17, 
    'x_append_event__mutmut_18': x_append_event__mutmut_18, 
    'x_append_event__mutmut_19': x_append_event__mutmut_19, 
    'x_append_event__mutmut_20': x_append_event__mutmut_20, 
    'x_append_event__mutmut_21': x_append_event__mutmut_21, 
    'x_append_event__mutmut_22': x_append_event__mutmut_22, 
    'x_append_event__mutmut_23': x_append_event__mutmut_23, 
    'x_append_event__mutmut_24': x_append_event__mutmut_24, 
    'x_append_event__mutmut_25': x_append_event__mutmut_25
}
x_append_event__mutmut_orig.__name__ = 'x_append_event'


def read_events_raw(feature_dir: Path) -> list[dict]:
    args = [feature_dir]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_read_events_raw__mutmut_orig, x_read_events_raw__mutmut_mutants, args, kwargs, None)


def x_read_events_raw__mutmut_orig(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_1(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = None
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_2(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(None)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_3(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_4(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = None
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_5(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open(None, encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_6(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding=None) as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_7(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open(encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_8(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", ) as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_9(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("XXrXX", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_10(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("R", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_11(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="XXutf-8XX") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_12(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="UTF-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_13(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(None, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_14(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=None):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_15(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_16(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, ):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_17(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=2):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_18(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = None
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_19(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_20(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                break
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_21(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = None
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_22(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(None)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_23(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    None
                ) from exc
            results.append(obj)
    return results


def x_read_events_raw__mutmut_24(feature_dir: Path) -> list[dict]:
    """Read raw JSON dicts from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON, including the 1-based
    line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            results.append(None)
    return results

x_read_events_raw__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_read_events_raw__mutmut_1': x_read_events_raw__mutmut_1, 
    'x_read_events_raw__mutmut_2': x_read_events_raw__mutmut_2, 
    'x_read_events_raw__mutmut_3': x_read_events_raw__mutmut_3, 
    'x_read_events_raw__mutmut_4': x_read_events_raw__mutmut_4, 
    'x_read_events_raw__mutmut_5': x_read_events_raw__mutmut_5, 
    'x_read_events_raw__mutmut_6': x_read_events_raw__mutmut_6, 
    'x_read_events_raw__mutmut_7': x_read_events_raw__mutmut_7, 
    'x_read_events_raw__mutmut_8': x_read_events_raw__mutmut_8, 
    'x_read_events_raw__mutmut_9': x_read_events_raw__mutmut_9, 
    'x_read_events_raw__mutmut_10': x_read_events_raw__mutmut_10, 
    'x_read_events_raw__mutmut_11': x_read_events_raw__mutmut_11, 
    'x_read_events_raw__mutmut_12': x_read_events_raw__mutmut_12, 
    'x_read_events_raw__mutmut_13': x_read_events_raw__mutmut_13, 
    'x_read_events_raw__mutmut_14': x_read_events_raw__mutmut_14, 
    'x_read_events_raw__mutmut_15': x_read_events_raw__mutmut_15, 
    'x_read_events_raw__mutmut_16': x_read_events_raw__mutmut_16, 
    'x_read_events_raw__mutmut_17': x_read_events_raw__mutmut_17, 
    'x_read_events_raw__mutmut_18': x_read_events_raw__mutmut_18, 
    'x_read_events_raw__mutmut_19': x_read_events_raw__mutmut_19, 
    'x_read_events_raw__mutmut_20': x_read_events_raw__mutmut_20, 
    'x_read_events_raw__mutmut_21': x_read_events_raw__mutmut_21, 
    'x_read_events_raw__mutmut_22': x_read_events_raw__mutmut_22, 
    'x_read_events_raw__mutmut_23': x_read_events_raw__mutmut_23, 
    'x_read_events_raw__mutmut_24': x_read_events_raw__mutmut_24
}
x_read_events_raw__mutmut_orig.__name__ = 'x_read_events_raw'


def read_events(feature_dir: Path) -> list[StatusEvent]:
    args = [feature_dir]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_read_events__mutmut_orig, x_read_events__mutmut_mutants, args, kwargs, None)


def x_read_events__mutmut_orig(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_1(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = None
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_2(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(None)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_3(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_4(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = None
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_5(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open(None, encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_6(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding=None) as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_7(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open(encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_8(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", ) as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_9(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("XXrXX", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_10(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("R", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_11(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="XXutf-8XX") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_12(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="UTF-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_13(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(None, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_14(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=None):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_15(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_16(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, ):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_17(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=2):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_18(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = None
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_19(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_20(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                break
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_21(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = None
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_22(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(None)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_23(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    None
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_24(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = None
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_25(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(None)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_26(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    None
                ) from exc
            results.append(event)
    return results


def x_read_events__mutmut_27(feature_dir: Path) -> list[StatusEvent]:
    """Read and deserialize StatusEvent objects from the events file.

    Returns an empty list when the file does not exist.
    Blank lines are silently skipped.
    Raises :class:`StoreError` on invalid JSON **or** invalid event
    structure, including the 1-based line number in the message.
    """
    path = _events_path(feature_dir)
    if not path.exists():
        return []

    results: list[StatusEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StoreError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            try:
                event = StatusEvent.from_dict(obj)
            except (KeyError, ValueError, TypeError) as exc:
                raise StoreError(
                    f"Invalid event structure on line {line_number}: {exc}"
                ) from exc
            results.append(None)
    return results

x_read_events__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_read_events__mutmut_1': x_read_events__mutmut_1, 
    'x_read_events__mutmut_2': x_read_events__mutmut_2, 
    'x_read_events__mutmut_3': x_read_events__mutmut_3, 
    'x_read_events__mutmut_4': x_read_events__mutmut_4, 
    'x_read_events__mutmut_5': x_read_events__mutmut_5, 
    'x_read_events__mutmut_6': x_read_events__mutmut_6, 
    'x_read_events__mutmut_7': x_read_events__mutmut_7, 
    'x_read_events__mutmut_8': x_read_events__mutmut_8, 
    'x_read_events__mutmut_9': x_read_events__mutmut_9, 
    'x_read_events__mutmut_10': x_read_events__mutmut_10, 
    'x_read_events__mutmut_11': x_read_events__mutmut_11, 
    'x_read_events__mutmut_12': x_read_events__mutmut_12, 
    'x_read_events__mutmut_13': x_read_events__mutmut_13, 
    'x_read_events__mutmut_14': x_read_events__mutmut_14, 
    'x_read_events__mutmut_15': x_read_events__mutmut_15, 
    'x_read_events__mutmut_16': x_read_events__mutmut_16, 
    'x_read_events__mutmut_17': x_read_events__mutmut_17, 
    'x_read_events__mutmut_18': x_read_events__mutmut_18, 
    'x_read_events__mutmut_19': x_read_events__mutmut_19, 
    'x_read_events__mutmut_20': x_read_events__mutmut_20, 
    'x_read_events__mutmut_21': x_read_events__mutmut_21, 
    'x_read_events__mutmut_22': x_read_events__mutmut_22, 
    'x_read_events__mutmut_23': x_read_events__mutmut_23, 
    'x_read_events__mutmut_24': x_read_events__mutmut_24, 
    'x_read_events__mutmut_25': x_read_events__mutmut_25, 
    'x_read_events__mutmut_26': x_read_events__mutmut_26, 
    'x_read_events__mutmut_27': x_read_events__mutmut_27
}
x_read_events__mutmut_orig.__name__ = 'x_read_events'
