"""Status doctor: health check framework for operational hygiene.

Detects stale claims, orphan workspaces, materialization drift,
and derived-view drift. Reports problems and recommends actions
but NEVER modifies files (read-only).
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from pathlib import Path

from .models import StatusSnapshot
from .reducer import SNAPSHOT_FILENAME, reduce
from .store import read_events

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


class Severity(StrEnum):
    WARNING = "warning"
    ERROR = "error"


class Category(StrEnum):
    STALE_CLAIM = "stale_claim"
    ORPHAN_WORKSPACE = "orphan_workspace"
    MATERIALIZATION_DRIFT = "materialization_drift"
    DERIVED_VIEW_DRIFT = "derived_view_drift"


@dataclass
class Finding:
    """A single health check finding."""

    severity: Severity
    category: Category
    wp_id: str | None
    message: str
    recommended_action: str


@dataclass
class DoctorResult:
    """Aggregate result of all health checks."""

    feature_slug: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(f.severity == Severity.ERROR for f in self.findings)

    @property
    def has_warnings(self) -> bool:
        return any(f.severity == Severity.WARNING for f in self.findings)

    @property
    def is_healthy(self) -> bool:
        return len(self.findings) == 0

    def findings_by_category(self, category: Category) -> list[Finding]:
        return [f for f in self.findings if f.category == category]


def _load_or_reduce_snapshot(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    args = [feature_dir, feature_slug]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__load_or_reduce_snapshot__mutmut_orig, x__load_or_reduce_snapshot__mutmut_mutants, args, kwargs, None)


def x__load_or_reduce_snapshot__mutmut_orig(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_1(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = None
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_2(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir * SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_3(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = None
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_4(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(None)
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_5(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding=None))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_6(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="XXutf-8XX"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_7(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="UTF-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_8(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug(None)

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_9(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("XXCould not read status.json, trying event logXX")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_10(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_11(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("COULD NOT READ STATUS.JSON, TRYING EVENT LOG")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_12(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = None
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_13(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(None)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_14(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = None
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_15(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(None)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_16(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug(None, exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_17(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=None)

    return None


def x__load_or_reduce_snapshot__mutmut_18(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug(exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_19(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", )

    return None


def x__load_or_reduce_snapshot__mutmut_20(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("XXCould not reduce from event logXX", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_21(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("could not reduce from event log", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_22(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("COULD NOT REDUCE FROM EVENT LOG", exc_info=True)

    return None


def x__load_or_reduce_snapshot__mutmut_23(
    feature_dir: Path,
    feature_slug: str,
) -> dict | None:
    """Load snapshot from status.json or reduce from events.

    Returns the snapshot as a dict (work_packages keyed by WP ID),
    or None if neither source is available.
    """
    # Try status.json first
    status_path = feature_dir / SNAPSHOT_FILENAME
    if status_path.exists():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            logger.debug("Could not read status.json, trying event log")

    # Try reducing from event log
    try:
        events = read_events(feature_dir)
        if events:
            snapshot = reduce(events)
            return snapshot.to_dict()
    except Exception:
        logger.debug("Could not reduce from event log", exc_info=False)

    return None

x__load_or_reduce_snapshot__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__load_or_reduce_snapshot__mutmut_1': x__load_or_reduce_snapshot__mutmut_1, 
    'x__load_or_reduce_snapshot__mutmut_2': x__load_or_reduce_snapshot__mutmut_2, 
    'x__load_or_reduce_snapshot__mutmut_3': x__load_or_reduce_snapshot__mutmut_3, 
    'x__load_or_reduce_snapshot__mutmut_4': x__load_or_reduce_snapshot__mutmut_4, 
    'x__load_or_reduce_snapshot__mutmut_5': x__load_or_reduce_snapshot__mutmut_5, 
    'x__load_or_reduce_snapshot__mutmut_6': x__load_or_reduce_snapshot__mutmut_6, 
    'x__load_or_reduce_snapshot__mutmut_7': x__load_or_reduce_snapshot__mutmut_7, 
    'x__load_or_reduce_snapshot__mutmut_8': x__load_or_reduce_snapshot__mutmut_8, 
    'x__load_or_reduce_snapshot__mutmut_9': x__load_or_reduce_snapshot__mutmut_9, 
    'x__load_or_reduce_snapshot__mutmut_10': x__load_or_reduce_snapshot__mutmut_10, 
    'x__load_or_reduce_snapshot__mutmut_11': x__load_or_reduce_snapshot__mutmut_11, 
    'x__load_or_reduce_snapshot__mutmut_12': x__load_or_reduce_snapshot__mutmut_12, 
    'x__load_or_reduce_snapshot__mutmut_13': x__load_or_reduce_snapshot__mutmut_13, 
    'x__load_or_reduce_snapshot__mutmut_14': x__load_or_reduce_snapshot__mutmut_14, 
    'x__load_or_reduce_snapshot__mutmut_15': x__load_or_reduce_snapshot__mutmut_15, 
    'x__load_or_reduce_snapshot__mutmut_16': x__load_or_reduce_snapshot__mutmut_16, 
    'x__load_or_reduce_snapshot__mutmut_17': x__load_or_reduce_snapshot__mutmut_17, 
    'x__load_or_reduce_snapshot__mutmut_18': x__load_or_reduce_snapshot__mutmut_18, 
    'x__load_or_reduce_snapshot__mutmut_19': x__load_or_reduce_snapshot__mutmut_19, 
    'x__load_or_reduce_snapshot__mutmut_20': x__load_or_reduce_snapshot__mutmut_20, 
    'x__load_or_reduce_snapshot__mutmut_21': x__load_or_reduce_snapshot__mutmut_21, 
    'x__load_or_reduce_snapshot__mutmut_22': x__load_or_reduce_snapshot__mutmut_22, 
    'x__load_or_reduce_snapshot__mutmut_23': x__load_or_reduce_snapshot__mutmut_23
}
x__load_or_reduce_snapshot__mutmut_orig.__name__ = 'x__load_or_reduce_snapshot'


def check_stale_claims(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    args = [feature_dir, snapshot]# type: ignore
    kwargs = {'claimed_threshold_days': claimed_threshold_days, 'in_progress_threshold_days': in_progress_threshold_days}# type: ignore
    return _mutmut_trampoline(x_check_stale_claims__mutmut_orig, x_check_stale_claims__mutmut_mutants, args, kwargs, None)


def x_check_stale_claims__mutmut_orig(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_1(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 8,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_2(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 15,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_3(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = None
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_4(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = None

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_5(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(None)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_6(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = None
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_7(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get(None, {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_8(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", None)
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_9(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get({})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_10(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", )
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_11(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("XXwork_packagesXX", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_12(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("WORK_PACKAGES", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_13(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = None
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_14(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get(None)
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_15(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("XXlaneXX")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_16(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("LANE")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_17(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = None

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_18(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get(None)

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_19(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("XXlast_transition_atXX")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_20(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("LAST_TRANSITION_AT")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_21(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_22(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            break

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_23(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = None
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_24(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(None)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_25(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            break

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_26(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = None

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_27(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now + transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_28(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" or age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_29(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane != "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_30(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "XXclaimedXX" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_31(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "CLAIMED" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_32(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days >= claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_33(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                None
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_34(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=None,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_35(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=None,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_36(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=None,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_37(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=None,
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_38(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=None,
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_39(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_40(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_41(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_42(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_43(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_44(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get(None, 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_45(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', None)}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_46(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_47(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', )}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_48(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('XXactorXX', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_49(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('ACTOR', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_50(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'XXunknownXX')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_51(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'UNKNOWN')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_52(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" or age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_53(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane != "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_54(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "XXin_progressXX" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_55(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "IN_PROGRESS" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_56(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days >= in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_57(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                None
            )

    return findings


def x_check_stale_claims__mutmut_58(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=None,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_59(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=None,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_60(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=None,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_61(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=None,
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_62(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=None,
                )
            )

    return findings


def x_check_stale_claims__mutmut_63(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_64(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_65(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_66(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_67(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    )
            )

    return findings


def x_check_stale_claims__mutmut_68(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get(None, 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_69(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', None)}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_70(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_71(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', )}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_72(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('XXactorXX', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_73(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('ACTOR', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_74(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'XXunknownXX')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings


def x_check_stale_claims__mutmut_75(
    feature_dir: Path,
    snapshot: dict,
    *,
    claimed_threshold_days: int = 7,
    in_progress_threshold_days: int = 14,
) -> list[Finding]:
    """Check for WPs stuck in claimed or in_progress."""
    findings: list[Finding] = []
    now = datetime.now(timezone.utc)

    work_packages = snapshot.get("work_packages", {})
    for wp_id, wp_state in work_packages.items():
        lane = wp_state.get("lane")
        last_transition_at = wp_state.get("last_transition_at")

        if not last_transition_at:
            continue

        try:
            transition_time = datetime.fromisoformat(last_transition_at)
        except (ValueError, TypeError):
            continue

        age_days = (now - transition_time).days

        if lane == "claimed" and age_days > claimed_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'claimed' for {age_days} days "
                        f"(threshold: {claimed_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'unknown')}"
                    ),
                    recommended_action=(
                        f"Either begin work on {wp_id} (move to in_progress) "
                        f"or release the claim (move back to planned)."
                    ),
                )
            )

        if lane == "in_progress" and age_days > in_progress_threshold_days:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.STALE_CLAIM,
                    wp_id=wp_id,
                    message=(
                        f"{wp_id} has been in 'in_progress' for {age_days} days "
                        f"(threshold: {in_progress_threshold_days} days). "
                        f"Actor: {wp_state.get('actor', 'UNKNOWN')}"
                    ),
                    recommended_action=(
                        f"Check if {wp_id} is blocked (move to blocked with reason) "
                        f"or complete the work (move to for_review)."
                    ),
                )
            )

    return findings

x_check_stale_claims__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_stale_claims__mutmut_1': x_check_stale_claims__mutmut_1, 
    'x_check_stale_claims__mutmut_2': x_check_stale_claims__mutmut_2, 
    'x_check_stale_claims__mutmut_3': x_check_stale_claims__mutmut_3, 
    'x_check_stale_claims__mutmut_4': x_check_stale_claims__mutmut_4, 
    'x_check_stale_claims__mutmut_5': x_check_stale_claims__mutmut_5, 
    'x_check_stale_claims__mutmut_6': x_check_stale_claims__mutmut_6, 
    'x_check_stale_claims__mutmut_7': x_check_stale_claims__mutmut_7, 
    'x_check_stale_claims__mutmut_8': x_check_stale_claims__mutmut_8, 
    'x_check_stale_claims__mutmut_9': x_check_stale_claims__mutmut_9, 
    'x_check_stale_claims__mutmut_10': x_check_stale_claims__mutmut_10, 
    'x_check_stale_claims__mutmut_11': x_check_stale_claims__mutmut_11, 
    'x_check_stale_claims__mutmut_12': x_check_stale_claims__mutmut_12, 
    'x_check_stale_claims__mutmut_13': x_check_stale_claims__mutmut_13, 
    'x_check_stale_claims__mutmut_14': x_check_stale_claims__mutmut_14, 
    'x_check_stale_claims__mutmut_15': x_check_stale_claims__mutmut_15, 
    'x_check_stale_claims__mutmut_16': x_check_stale_claims__mutmut_16, 
    'x_check_stale_claims__mutmut_17': x_check_stale_claims__mutmut_17, 
    'x_check_stale_claims__mutmut_18': x_check_stale_claims__mutmut_18, 
    'x_check_stale_claims__mutmut_19': x_check_stale_claims__mutmut_19, 
    'x_check_stale_claims__mutmut_20': x_check_stale_claims__mutmut_20, 
    'x_check_stale_claims__mutmut_21': x_check_stale_claims__mutmut_21, 
    'x_check_stale_claims__mutmut_22': x_check_stale_claims__mutmut_22, 
    'x_check_stale_claims__mutmut_23': x_check_stale_claims__mutmut_23, 
    'x_check_stale_claims__mutmut_24': x_check_stale_claims__mutmut_24, 
    'x_check_stale_claims__mutmut_25': x_check_stale_claims__mutmut_25, 
    'x_check_stale_claims__mutmut_26': x_check_stale_claims__mutmut_26, 
    'x_check_stale_claims__mutmut_27': x_check_stale_claims__mutmut_27, 
    'x_check_stale_claims__mutmut_28': x_check_stale_claims__mutmut_28, 
    'x_check_stale_claims__mutmut_29': x_check_stale_claims__mutmut_29, 
    'x_check_stale_claims__mutmut_30': x_check_stale_claims__mutmut_30, 
    'x_check_stale_claims__mutmut_31': x_check_stale_claims__mutmut_31, 
    'x_check_stale_claims__mutmut_32': x_check_stale_claims__mutmut_32, 
    'x_check_stale_claims__mutmut_33': x_check_stale_claims__mutmut_33, 
    'x_check_stale_claims__mutmut_34': x_check_stale_claims__mutmut_34, 
    'x_check_stale_claims__mutmut_35': x_check_stale_claims__mutmut_35, 
    'x_check_stale_claims__mutmut_36': x_check_stale_claims__mutmut_36, 
    'x_check_stale_claims__mutmut_37': x_check_stale_claims__mutmut_37, 
    'x_check_stale_claims__mutmut_38': x_check_stale_claims__mutmut_38, 
    'x_check_stale_claims__mutmut_39': x_check_stale_claims__mutmut_39, 
    'x_check_stale_claims__mutmut_40': x_check_stale_claims__mutmut_40, 
    'x_check_stale_claims__mutmut_41': x_check_stale_claims__mutmut_41, 
    'x_check_stale_claims__mutmut_42': x_check_stale_claims__mutmut_42, 
    'x_check_stale_claims__mutmut_43': x_check_stale_claims__mutmut_43, 
    'x_check_stale_claims__mutmut_44': x_check_stale_claims__mutmut_44, 
    'x_check_stale_claims__mutmut_45': x_check_stale_claims__mutmut_45, 
    'x_check_stale_claims__mutmut_46': x_check_stale_claims__mutmut_46, 
    'x_check_stale_claims__mutmut_47': x_check_stale_claims__mutmut_47, 
    'x_check_stale_claims__mutmut_48': x_check_stale_claims__mutmut_48, 
    'x_check_stale_claims__mutmut_49': x_check_stale_claims__mutmut_49, 
    'x_check_stale_claims__mutmut_50': x_check_stale_claims__mutmut_50, 
    'x_check_stale_claims__mutmut_51': x_check_stale_claims__mutmut_51, 
    'x_check_stale_claims__mutmut_52': x_check_stale_claims__mutmut_52, 
    'x_check_stale_claims__mutmut_53': x_check_stale_claims__mutmut_53, 
    'x_check_stale_claims__mutmut_54': x_check_stale_claims__mutmut_54, 
    'x_check_stale_claims__mutmut_55': x_check_stale_claims__mutmut_55, 
    'x_check_stale_claims__mutmut_56': x_check_stale_claims__mutmut_56, 
    'x_check_stale_claims__mutmut_57': x_check_stale_claims__mutmut_57, 
    'x_check_stale_claims__mutmut_58': x_check_stale_claims__mutmut_58, 
    'x_check_stale_claims__mutmut_59': x_check_stale_claims__mutmut_59, 
    'x_check_stale_claims__mutmut_60': x_check_stale_claims__mutmut_60, 
    'x_check_stale_claims__mutmut_61': x_check_stale_claims__mutmut_61, 
    'x_check_stale_claims__mutmut_62': x_check_stale_claims__mutmut_62, 
    'x_check_stale_claims__mutmut_63': x_check_stale_claims__mutmut_63, 
    'x_check_stale_claims__mutmut_64': x_check_stale_claims__mutmut_64, 
    'x_check_stale_claims__mutmut_65': x_check_stale_claims__mutmut_65, 
    'x_check_stale_claims__mutmut_66': x_check_stale_claims__mutmut_66, 
    'x_check_stale_claims__mutmut_67': x_check_stale_claims__mutmut_67, 
    'x_check_stale_claims__mutmut_68': x_check_stale_claims__mutmut_68, 
    'x_check_stale_claims__mutmut_69': x_check_stale_claims__mutmut_69, 
    'x_check_stale_claims__mutmut_70': x_check_stale_claims__mutmut_70, 
    'x_check_stale_claims__mutmut_71': x_check_stale_claims__mutmut_71, 
    'x_check_stale_claims__mutmut_72': x_check_stale_claims__mutmut_72, 
    'x_check_stale_claims__mutmut_73': x_check_stale_claims__mutmut_73, 
    'x_check_stale_claims__mutmut_74': x_check_stale_claims__mutmut_74, 
    'x_check_stale_claims__mutmut_75': x_check_stale_claims__mutmut_75
}
x_check_stale_claims__mutmut_orig.__name__ = 'x_check_stale_claims'


def check_orphan_workspaces(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    args = [repo_root, feature_slug, snapshot]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_orphan_workspaces__mutmut_orig, x_check_orphan_workspaces__mutmut_mutants, args, kwargs, None)


def x_check_orphan_workspaces__mutmut_orig(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_1(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = None

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_2(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = None
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_3(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get(None, {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_4(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", None)
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_5(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get({})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_6(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", )
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_7(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("XXwork_packagesXX", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_8(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("WORK_PACKAGES", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_9(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_10(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = None
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_11(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"XXdoneXX", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_12(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"DONE", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_13(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "XXcanceledXX"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_14(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "CANCELED"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_15(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = None

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_16(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        None
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_17(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get(None) in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_18(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("XXlaneXX") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_19(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("LANE") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_20(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") not in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_21(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_22(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = None
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_23(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root * ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_24(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / "XX.worktreesXX"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_25(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".WORKTREES"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_26(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_27(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = None
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_28(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = None

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_29(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(None)

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_30(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(None))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_31(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                None
            )

    return findings


def x_check_orphan_workspaces__mutmut_32(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=None,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_33(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=None,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_34(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=None,
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_35(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=None,
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_36(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_37(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_38(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_39(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_40(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    )
            )

    return findings


def x_check_orphan_workspaces__mutmut_41(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(None)}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_42(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({'XX, XX'.join(sorted(terminal_lanes))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings


def x_check_orphan_workspaces__mutmut_43(
    repo_root: Path,
    feature_slug: str,
    snapshot: dict,
) -> list[Finding]:
    """Detect orphan worktrees for completed/canceled features."""
    findings: list[Finding] = []

    # Check if all WPs are in terminal states
    work_packages = snapshot.get("work_packages", {})
    if not work_packages:
        return findings

    terminal_lanes = {"done", "canceled"}
    all_terminal = all(
        wp.get("lane") in terminal_lanes for wp in work_packages.values()
    )

    if not all_terminal:
        return findings  # Feature still has active WPs, worktrees are legitimate

    # Scan for worktrees matching this feature
    worktrees_dir = repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return findings

    feature_pattern = f"{feature_slug}-WP*"
    orphan_dirs = list(worktrees_dir.glob(feature_pattern))

    for orphan_dir in orphan_dirs:
        if orphan_dir.is_dir():
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    category=Category.ORPHAN_WORKSPACE,
                    wp_id=None,
                    message=(
                        f"Worktree '{orphan_dir.name}' exists but all WPs in "
                        f"'{feature_slug}' are terminal "
                        f"({', '.join(sorted(None))}). "
                        f"Path: {orphan_dir}"
                    ),
                    recommended_action=(
                        f"Remove the orphan worktree: "
                        f"git worktree remove {orphan_dir.name}"
                    ),
                )
            )

    return findings

x_check_orphan_workspaces__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_orphan_workspaces__mutmut_1': x_check_orphan_workspaces__mutmut_1, 
    'x_check_orphan_workspaces__mutmut_2': x_check_orphan_workspaces__mutmut_2, 
    'x_check_orphan_workspaces__mutmut_3': x_check_orphan_workspaces__mutmut_3, 
    'x_check_orphan_workspaces__mutmut_4': x_check_orphan_workspaces__mutmut_4, 
    'x_check_orphan_workspaces__mutmut_5': x_check_orphan_workspaces__mutmut_5, 
    'x_check_orphan_workspaces__mutmut_6': x_check_orphan_workspaces__mutmut_6, 
    'x_check_orphan_workspaces__mutmut_7': x_check_orphan_workspaces__mutmut_7, 
    'x_check_orphan_workspaces__mutmut_8': x_check_orphan_workspaces__mutmut_8, 
    'x_check_orphan_workspaces__mutmut_9': x_check_orphan_workspaces__mutmut_9, 
    'x_check_orphan_workspaces__mutmut_10': x_check_orphan_workspaces__mutmut_10, 
    'x_check_orphan_workspaces__mutmut_11': x_check_orphan_workspaces__mutmut_11, 
    'x_check_orphan_workspaces__mutmut_12': x_check_orphan_workspaces__mutmut_12, 
    'x_check_orphan_workspaces__mutmut_13': x_check_orphan_workspaces__mutmut_13, 
    'x_check_orphan_workspaces__mutmut_14': x_check_orphan_workspaces__mutmut_14, 
    'x_check_orphan_workspaces__mutmut_15': x_check_orphan_workspaces__mutmut_15, 
    'x_check_orphan_workspaces__mutmut_16': x_check_orphan_workspaces__mutmut_16, 
    'x_check_orphan_workspaces__mutmut_17': x_check_orphan_workspaces__mutmut_17, 
    'x_check_orphan_workspaces__mutmut_18': x_check_orphan_workspaces__mutmut_18, 
    'x_check_orphan_workspaces__mutmut_19': x_check_orphan_workspaces__mutmut_19, 
    'x_check_orphan_workspaces__mutmut_20': x_check_orphan_workspaces__mutmut_20, 
    'x_check_orphan_workspaces__mutmut_21': x_check_orphan_workspaces__mutmut_21, 
    'x_check_orphan_workspaces__mutmut_22': x_check_orphan_workspaces__mutmut_22, 
    'x_check_orphan_workspaces__mutmut_23': x_check_orphan_workspaces__mutmut_23, 
    'x_check_orphan_workspaces__mutmut_24': x_check_orphan_workspaces__mutmut_24, 
    'x_check_orphan_workspaces__mutmut_25': x_check_orphan_workspaces__mutmut_25, 
    'x_check_orphan_workspaces__mutmut_26': x_check_orphan_workspaces__mutmut_26, 
    'x_check_orphan_workspaces__mutmut_27': x_check_orphan_workspaces__mutmut_27, 
    'x_check_orphan_workspaces__mutmut_28': x_check_orphan_workspaces__mutmut_28, 
    'x_check_orphan_workspaces__mutmut_29': x_check_orphan_workspaces__mutmut_29, 
    'x_check_orphan_workspaces__mutmut_30': x_check_orphan_workspaces__mutmut_30, 
    'x_check_orphan_workspaces__mutmut_31': x_check_orphan_workspaces__mutmut_31, 
    'x_check_orphan_workspaces__mutmut_32': x_check_orphan_workspaces__mutmut_32, 
    'x_check_orphan_workspaces__mutmut_33': x_check_orphan_workspaces__mutmut_33, 
    'x_check_orphan_workspaces__mutmut_34': x_check_orphan_workspaces__mutmut_34, 
    'x_check_orphan_workspaces__mutmut_35': x_check_orphan_workspaces__mutmut_35, 
    'x_check_orphan_workspaces__mutmut_36': x_check_orphan_workspaces__mutmut_36, 
    'x_check_orphan_workspaces__mutmut_37': x_check_orphan_workspaces__mutmut_37, 
    'x_check_orphan_workspaces__mutmut_38': x_check_orphan_workspaces__mutmut_38, 
    'x_check_orphan_workspaces__mutmut_39': x_check_orphan_workspaces__mutmut_39, 
    'x_check_orphan_workspaces__mutmut_40': x_check_orphan_workspaces__mutmut_40, 
    'x_check_orphan_workspaces__mutmut_41': x_check_orphan_workspaces__mutmut_41, 
    'x_check_orphan_workspaces__mutmut_42': x_check_orphan_workspaces__mutmut_42, 
    'x_check_orphan_workspaces__mutmut_43': x_check_orphan_workspaces__mutmut_43
}
x_check_orphan_workspaces__mutmut_orig.__name__ = 'x_check_orphan_workspaces'


def check_drift(feature_dir: Path) -> list[Finding]:
    args = [feature_dir]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_drift__mutmut_orig, x_check_drift__mutmut_mutants, args, kwargs, None)


def x_check_drift__mutmut_orig(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_1(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = None
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_2(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = None
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_3(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(None)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_4(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            None
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_5(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=None,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_6(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=None,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_7(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=None,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_8(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=None,
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_9(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_10(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_11(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_12(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_13(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_14(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "XXRun 'spec-kitty agent status materialize' to regenerate XX"
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_15(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_16(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "RUN 'SPEC-KITTY AGENT STATUS MATERIALIZE' TO REGENERATE "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_17(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "XXstatus.json from the canonical event log.XX"
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_18(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "STATUS.JSON FROM THE CANONICAL EVENT LOG."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_19(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = None
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_20(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir * SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_21(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = None
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_22(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(None)
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_23(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding=None))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_24(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="XXutf-8XX"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_25(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="UTF-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_26(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = None
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_27(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(None, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_28(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, None)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_29(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_30(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, )
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_31(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = None
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_32(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                None,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_33(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                None,
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_34(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                None,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_35(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_36(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_37(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_38(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get(None, {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_39(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", None),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_40(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get({}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_41(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", ),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_42(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("XXwork_packagesXX", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_43(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("WORK_PACKAGES", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_44(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    None
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_45(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=None,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_46(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=None,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_47(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=None,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_48(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=None,
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_49(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_50(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_51(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_52(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_53(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_54(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "XXRun 'spec-kitty agent status materialize' to XX"
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_55(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_56(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "RUN 'SPEC-KITTY AGENT STATUS MATERIALIZE' TO "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_57(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "XXregenerate derived views from status.json.XX"
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_58(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "REGENERATE DERIVED VIEWS FROM STATUS.JSON."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_59(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug(None, exc_info=True)

    return findings


def x_check_drift__mutmut_60(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=None)

    return findings


def x_check_drift__mutmut_61(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug(exc_info=True)

    return findings


def x_check_drift__mutmut_62(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", )

    return findings


def x_check_drift__mutmut_63(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("XXCould not check derived-view driftXX", exc_info=True)

    return findings


def x_check_drift__mutmut_64(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("could not check derived-view drift", exc_info=True)

    return findings


def x_check_drift__mutmut_65(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("COULD NOT CHECK DERIVED-VIEW DRIFT", exc_info=True)

    return findings


def x_check_drift__mutmut_66(feature_dir: Path) -> list[Finding]:
    """Delegate to validation engine for drift detection.

    Uses try/except import to handle the case where WP11
    (validate) is not yet implemented.
    """
    findings: list[Finding] = []
    try:
        from specify_cli.status.validate import (
            validate_derived_views,
            validate_materialization_drift,
        )
    except ImportError:
        # Validation engine not available yet (WP11 not merged)
        return findings

    # Materialization drift
    drift_findings = validate_materialization_drift(feature_dir)
    for msg in drift_findings:
        findings.append(
            Finding(
                severity=Severity.WARNING,
                category=Category.MATERIALIZATION_DRIFT,
                wp_id=None,
                message=msg,
                recommended_action=(
                    "Run 'spec-kitty agent status materialize' to regenerate "
                    "status.json from the canonical event log."
                ),
            )
        )

    # Derived-view drift
    try:
        status_path = feature_dir / SNAPSHOT_FILENAME
        if status_path.exists():
            snapshot = json.loads(status_path.read_text(encoding="utf-8"))
            from specify_cli.status.phase import resolve_phase

            phase, _ = resolve_phase(feature_dir.parent.parent, feature_dir.name)
            view_findings = validate_derived_views(
                feature_dir,
                snapshot.get("work_packages", {}),
                phase,
            )
            for msg in view_findings:
                findings.append(
                    Finding(
                        severity=Severity.WARNING,
                        category=Category.DERIVED_VIEW_DRIFT,
                        wp_id=None,
                        message=msg,
                        recommended_action=(
                            "Run 'spec-kitty agent status materialize' to "
                            "regenerate derived views from status.json."
                        ),
                    )
                )
    except Exception:
        logger.debug("Could not check derived-view drift", exc_info=False)

    return findings

x_check_drift__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_drift__mutmut_1': x_check_drift__mutmut_1, 
    'x_check_drift__mutmut_2': x_check_drift__mutmut_2, 
    'x_check_drift__mutmut_3': x_check_drift__mutmut_3, 
    'x_check_drift__mutmut_4': x_check_drift__mutmut_4, 
    'x_check_drift__mutmut_5': x_check_drift__mutmut_5, 
    'x_check_drift__mutmut_6': x_check_drift__mutmut_6, 
    'x_check_drift__mutmut_7': x_check_drift__mutmut_7, 
    'x_check_drift__mutmut_8': x_check_drift__mutmut_8, 
    'x_check_drift__mutmut_9': x_check_drift__mutmut_9, 
    'x_check_drift__mutmut_10': x_check_drift__mutmut_10, 
    'x_check_drift__mutmut_11': x_check_drift__mutmut_11, 
    'x_check_drift__mutmut_12': x_check_drift__mutmut_12, 
    'x_check_drift__mutmut_13': x_check_drift__mutmut_13, 
    'x_check_drift__mutmut_14': x_check_drift__mutmut_14, 
    'x_check_drift__mutmut_15': x_check_drift__mutmut_15, 
    'x_check_drift__mutmut_16': x_check_drift__mutmut_16, 
    'x_check_drift__mutmut_17': x_check_drift__mutmut_17, 
    'x_check_drift__mutmut_18': x_check_drift__mutmut_18, 
    'x_check_drift__mutmut_19': x_check_drift__mutmut_19, 
    'x_check_drift__mutmut_20': x_check_drift__mutmut_20, 
    'x_check_drift__mutmut_21': x_check_drift__mutmut_21, 
    'x_check_drift__mutmut_22': x_check_drift__mutmut_22, 
    'x_check_drift__mutmut_23': x_check_drift__mutmut_23, 
    'x_check_drift__mutmut_24': x_check_drift__mutmut_24, 
    'x_check_drift__mutmut_25': x_check_drift__mutmut_25, 
    'x_check_drift__mutmut_26': x_check_drift__mutmut_26, 
    'x_check_drift__mutmut_27': x_check_drift__mutmut_27, 
    'x_check_drift__mutmut_28': x_check_drift__mutmut_28, 
    'x_check_drift__mutmut_29': x_check_drift__mutmut_29, 
    'x_check_drift__mutmut_30': x_check_drift__mutmut_30, 
    'x_check_drift__mutmut_31': x_check_drift__mutmut_31, 
    'x_check_drift__mutmut_32': x_check_drift__mutmut_32, 
    'x_check_drift__mutmut_33': x_check_drift__mutmut_33, 
    'x_check_drift__mutmut_34': x_check_drift__mutmut_34, 
    'x_check_drift__mutmut_35': x_check_drift__mutmut_35, 
    'x_check_drift__mutmut_36': x_check_drift__mutmut_36, 
    'x_check_drift__mutmut_37': x_check_drift__mutmut_37, 
    'x_check_drift__mutmut_38': x_check_drift__mutmut_38, 
    'x_check_drift__mutmut_39': x_check_drift__mutmut_39, 
    'x_check_drift__mutmut_40': x_check_drift__mutmut_40, 
    'x_check_drift__mutmut_41': x_check_drift__mutmut_41, 
    'x_check_drift__mutmut_42': x_check_drift__mutmut_42, 
    'x_check_drift__mutmut_43': x_check_drift__mutmut_43, 
    'x_check_drift__mutmut_44': x_check_drift__mutmut_44, 
    'x_check_drift__mutmut_45': x_check_drift__mutmut_45, 
    'x_check_drift__mutmut_46': x_check_drift__mutmut_46, 
    'x_check_drift__mutmut_47': x_check_drift__mutmut_47, 
    'x_check_drift__mutmut_48': x_check_drift__mutmut_48, 
    'x_check_drift__mutmut_49': x_check_drift__mutmut_49, 
    'x_check_drift__mutmut_50': x_check_drift__mutmut_50, 
    'x_check_drift__mutmut_51': x_check_drift__mutmut_51, 
    'x_check_drift__mutmut_52': x_check_drift__mutmut_52, 
    'x_check_drift__mutmut_53': x_check_drift__mutmut_53, 
    'x_check_drift__mutmut_54': x_check_drift__mutmut_54, 
    'x_check_drift__mutmut_55': x_check_drift__mutmut_55, 
    'x_check_drift__mutmut_56': x_check_drift__mutmut_56, 
    'x_check_drift__mutmut_57': x_check_drift__mutmut_57, 
    'x_check_drift__mutmut_58': x_check_drift__mutmut_58, 
    'x_check_drift__mutmut_59': x_check_drift__mutmut_59, 
    'x_check_drift__mutmut_60': x_check_drift__mutmut_60, 
    'x_check_drift__mutmut_61': x_check_drift__mutmut_61, 
    'x_check_drift__mutmut_62': x_check_drift__mutmut_62, 
    'x_check_drift__mutmut_63': x_check_drift__mutmut_63, 
    'x_check_drift__mutmut_64': x_check_drift__mutmut_64, 
    'x_check_drift__mutmut_65': x_check_drift__mutmut_65, 
    'x_check_drift__mutmut_66': x_check_drift__mutmut_66
}
x_check_drift__mutmut_orig.__name__ = 'x_check_drift'


def run_doctor(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    args = [feature_dir, feature_slug, repo_root]# type: ignore
    kwargs = {'stale_claimed_days': stale_claimed_days, 'stale_in_progress_days': stale_in_progress_days}# type: ignore
    return _mutmut_trampoline(x_run_doctor__mutmut_orig, x_run_doctor__mutmut_mutants, args, kwargs, None)


def x_run_doctor__mutmut_orig(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_1(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 8,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_2(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 15,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_3(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_4(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            None
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_5(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = None

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_6(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=None)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_7(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = None

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_8(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(None, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_9(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, None)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_10(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_11(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, )

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_12(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            None
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_13(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                None,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_14(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                None,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_15(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=None,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_16(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=None,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_17(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_18(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_19(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_20(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_21(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            None
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_22(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(None, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_23(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, None, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_24(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, None)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_25(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(feature_slug, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_26(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, snapshot)
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_27(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, )
        )
        result.findings.extend(check_drift(feature_dir))

    return result


def x_run_doctor__mutmut_28(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(None)

    return result


def x_run_doctor__mutmut_29(
    feature_dir: Path,
    feature_slug: str,
    repo_root: Path,
    *,
    stale_claimed_days: int = 7,
    stale_in_progress_days: int = 14,
) -> DoctorResult:
    """Run all health checks for a feature.

    This is the main entry point. It loads the snapshot (from status.json
    or by reducing the event log), then runs all checks.

    Args:
        feature_dir: Path to the feature's kitty-specs directory.
        feature_slug: Feature identifier (e.g., "034-feature-name").
        repo_root: Path to the repository root.
        stale_claimed_days: Days before a claimed WP is flagged as stale.
        stale_in_progress_days: Days before an in_progress WP is flagged.

    Returns:
        DoctorResult with all findings.

    Raises:
        FileNotFoundError: If feature_dir does not exist.
    """
    if not feature_dir.exists():
        raise FileNotFoundError(
            f"Feature directory does not exist: {feature_dir}"
        )

    result = DoctorResult(feature_slug=feature_slug)

    # Load snapshot (from status.json or reduce from events)
    snapshot = _load_or_reduce_snapshot(feature_dir, feature_slug)

    if snapshot:
        result.findings.extend(
            check_stale_claims(
                feature_dir,
                snapshot,
                claimed_threshold_days=stale_claimed_days,
                in_progress_threshold_days=stale_in_progress_days,
            )
        )
        result.findings.extend(
            check_orphan_workspaces(repo_root, feature_slug, snapshot)
        )
        result.findings.extend(check_drift(None))

    return result

x_run_doctor__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_run_doctor__mutmut_1': x_run_doctor__mutmut_1, 
    'x_run_doctor__mutmut_2': x_run_doctor__mutmut_2, 
    'x_run_doctor__mutmut_3': x_run_doctor__mutmut_3, 
    'x_run_doctor__mutmut_4': x_run_doctor__mutmut_4, 
    'x_run_doctor__mutmut_5': x_run_doctor__mutmut_5, 
    'x_run_doctor__mutmut_6': x_run_doctor__mutmut_6, 
    'x_run_doctor__mutmut_7': x_run_doctor__mutmut_7, 
    'x_run_doctor__mutmut_8': x_run_doctor__mutmut_8, 
    'x_run_doctor__mutmut_9': x_run_doctor__mutmut_9, 
    'x_run_doctor__mutmut_10': x_run_doctor__mutmut_10, 
    'x_run_doctor__mutmut_11': x_run_doctor__mutmut_11, 
    'x_run_doctor__mutmut_12': x_run_doctor__mutmut_12, 
    'x_run_doctor__mutmut_13': x_run_doctor__mutmut_13, 
    'x_run_doctor__mutmut_14': x_run_doctor__mutmut_14, 
    'x_run_doctor__mutmut_15': x_run_doctor__mutmut_15, 
    'x_run_doctor__mutmut_16': x_run_doctor__mutmut_16, 
    'x_run_doctor__mutmut_17': x_run_doctor__mutmut_17, 
    'x_run_doctor__mutmut_18': x_run_doctor__mutmut_18, 
    'x_run_doctor__mutmut_19': x_run_doctor__mutmut_19, 
    'x_run_doctor__mutmut_20': x_run_doctor__mutmut_20, 
    'x_run_doctor__mutmut_21': x_run_doctor__mutmut_21, 
    'x_run_doctor__mutmut_22': x_run_doctor__mutmut_22, 
    'x_run_doctor__mutmut_23': x_run_doctor__mutmut_23, 
    'x_run_doctor__mutmut_24': x_run_doctor__mutmut_24, 
    'x_run_doctor__mutmut_25': x_run_doctor__mutmut_25, 
    'x_run_doctor__mutmut_26': x_run_doctor__mutmut_26, 
    'x_run_doctor__mutmut_27': x_run_doctor__mutmut_27, 
    'x_run_doctor__mutmut_28': x_run_doctor__mutmut_28, 
    'x_run_doctor__mutmut_29': x_run_doctor__mutmut_29
}
x_run_doctor__mutmut_orig.__name__ = 'x_run_doctor'
