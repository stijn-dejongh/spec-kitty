"""History parser for reconstructing transition chains from WP frontmatter.

Provides pure functions that convert raw frontmatter history[] arrays
into normalized, deduplicated transition chains suitable for creating
canonical StatusEvent records. This module performs NO I/O — it only
transforms data structures.

Exports:
    NormalizedHistoryEntry - Intermediate representation of a history entry
    Transition - A single lane-to-lane transition
    TransitionChain - Ordered list of transitions with metadata
    build_transition_chain() - Main entry point for reconstruction
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from .models import DoneEvidence, ReviewApproval
from .transitions import resolve_lane_alias

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


@dataclass(frozen=True)
class NormalizedHistoryEntry:
    """A single history entry with alias-resolved lane and extracted fields."""

    timestamp: str  # ISO 8601 UTC
    lane: str  # Canonical lane (never an alias)
    actor: str  # Agent identifier or "migration"


@dataclass(frozen=True)
class Transition:
    """A single lane-to-lane transition derived from adjacent history entries."""

    from_lane: str
    to_lane: str
    timestamp: str  # Timestamp of the transition (from target entry)
    actor: str  # Actor who caused the transition
    evidence: DoneEvidence | None = None


@dataclass
class TransitionChain:
    """Ordered list of transitions reconstructed from frontmatter history."""

    transitions: list[Transition]
    history_entries: int  # Number of raw history entries parsed
    has_evidence: bool  # Whether any transition has DoneEvidence


def normalize_entries(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    args = [history]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_normalize_entries__mutmut_orig, x_normalize_entries__mutmut_mutants, args, kwargs, None)


def x_normalize_entries__mutmut_orig(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_1(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = None
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_2(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_3(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning(None, entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_4(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", None)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_5(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning(entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_6(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", )
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_7(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("XXSkipping non-dict history entry: %rXX", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_8(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_9(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("SKIPPING NON-DICT HISTORY ENTRY: %R", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_10(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            break

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_11(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = None
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_12(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get(None)
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_13(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("XXlaneXX")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_14(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("LANE")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_15(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_16(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning(None, entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_17(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", None)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_18(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning(entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_19(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", )
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_20(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("XXSkipping history entry with missing lane: %rXX", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_21(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_22(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("SKIPPING HISTORY ENTRY WITH MISSING LANE: %R", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_23(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            break

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_24(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = None
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_25(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(None)
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_26(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(None).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_27(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = None
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_28(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) and datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_29(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(None) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_30(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get(None, "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_31(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", None)) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_32(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_33(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", )) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_34(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("XXtimestampXX", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_35(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("TIMESTAMP", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_36(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "XXXX")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_37(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            None
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_38(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = None

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_39(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) and "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_40(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(None) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_41(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get(None, "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_42(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", None)) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_43(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_44(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", )) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_45(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("XXagentXX", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_46(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("AGENT", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_47(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "XXXX")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_48(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "XXmigrationXX"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_49(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "MIGRATION"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_50(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            None
        )
    return entries


def x_normalize_entries__mutmut_51(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=None, lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_52(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=None, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_53(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, actor=None)
        )
    return entries


def x_normalize_entries__mutmut_54(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(lane=lane, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_55(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, actor=actor)
        )
    return entries


def x_normalize_entries__mutmut_56(history: list[dict[str, Any]]) -> list[NormalizedHistoryEntry]:
    """Convert raw Format A history entries into NormalizedHistoryEntry objects.

    Resolves lane aliases, extracts timestamps and actors, and skips
    malformed entries gracefully.

    Args:
        history: List of raw history dicts from frontmatter.

    Returns:
        List of NormalizedHistoryEntry in original order.
    """
    entries: list[NormalizedHistoryEntry] = []
    for entry in history:
        if not isinstance(entry, dict):
            logger.warning("Skipping non-dict history entry: %r", entry)
            continue

        raw_lane = entry.get("lane")
        if not raw_lane:
            logger.warning("Skipping history entry with missing lane: %r", entry)
            continue

        lane = resolve_lane_alias(str(raw_lane).strip())
        timestamp = str(entry.get("timestamp", "")) or datetime.now(
            timezone.utc
        ).isoformat()
        actor = str(entry.get("agent", "")) or "migration"

        entries.append(
            NormalizedHistoryEntry(timestamp=timestamp, lane=lane, )
        )
    return entries

x_normalize_entries__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_normalize_entries__mutmut_1': x_normalize_entries__mutmut_1, 
    'x_normalize_entries__mutmut_2': x_normalize_entries__mutmut_2, 
    'x_normalize_entries__mutmut_3': x_normalize_entries__mutmut_3, 
    'x_normalize_entries__mutmut_4': x_normalize_entries__mutmut_4, 
    'x_normalize_entries__mutmut_5': x_normalize_entries__mutmut_5, 
    'x_normalize_entries__mutmut_6': x_normalize_entries__mutmut_6, 
    'x_normalize_entries__mutmut_7': x_normalize_entries__mutmut_7, 
    'x_normalize_entries__mutmut_8': x_normalize_entries__mutmut_8, 
    'x_normalize_entries__mutmut_9': x_normalize_entries__mutmut_9, 
    'x_normalize_entries__mutmut_10': x_normalize_entries__mutmut_10, 
    'x_normalize_entries__mutmut_11': x_normalize_entries__mutmut_11, 
    'x_normalize_entries__mutmut_12': x_normalize_entries__mutmut_12, 
    'x_normalize_entries__mutmut_13': x_normalize_entries__mutmut_13, 
    'x_normalize_entries__mutmut_14': x_normalize_entries__mutmut_14, 
    'x_normalize_entries__mutmut_15': x_normalize_entries__mutmut_15, 
    'x_normalize_entries__mutmut_16': x_normalize_entries__mutmut_16, 
    'x_normalize_entries__mutmut_17': x_normalize_entries__mutmut_17, 
    'x_normalize_entries__mutmut_18': x_normalize_entries__mutmut_18, 
    'x_normalize_entries__mutmut_19': x_normalize_entries__mutmut_19, 
    'x_normalize_entries__mutmut_20': x_normalize_entries__mutmut_20, 
    'x_normalize_entries__mutmut_21': x_normalize_entries__mutmut_21, 
    'x_normalize_entries__mutmut_22': x_normalize_entries__mutmut_22, 
    'x_normalize_entries__mutmut_23': x_normalize_entries__mutmut_23, 
    'x_normalize_entries__mutmut_24': x_normalize_entries__mutmut_24, 
    'x_normalize_entries__mutmut_25': x_normalize_entries__mutmut_25, 
    'x_normalize_entries__mutmut_26': x_normalize_entries__mutmut_26, 
    'x_normalize_entries__mutmut_27': x_normalize_entries__mutmut_27, 
    'x_normalize_entries__mutmut_28': x_normalize_entries__mutmut_28, 
    'x_normalize_entries__mutmut_29': x_normalize_entries__mutmut_29, 
    'x_normalize_entries__mutmut_30': x_normalize_entries__mutmut_30, 
    'x_normalize_entries__mutmut_31': x_normalize_entries__mutmut_31, 
    'x_normalize_entries__mutmut_32': x_normalize_entries__mutmut_32, 
    'x_normalize_entries__mutmut_33': x_normalize_entries__mutmut_33, 
    'x_normalize_entries__mutmut_34': x_normalize_entries__mutmut_34, 
    'x_normalize_entries__mutmut_35': x_normalize_entries__mutmut_35, 
    'x_normalize_entries__mutmut_36': x_normalize_entries__mutmut_36, 
    'x_normalize_entries__mutmut_37': x_normalize_entries__mutmut_37, 
    'x_normalize_entries__mutmut_38': x_normalize_entries__mutmut_38, 
    'x_normalize_entries__mutmut_39': x_normalize_entries__mutmut_39, 
    'x_normalize_entries__mutmut_40': x_normalize_entries__mutmut_40, 
    'x_normalize_entries__mutmut_41': x_normalize_entries__mutmut_41, 
    'x_normalize_entries__mutmut_42': x_normalize_entries__mutmut_42, 
    'x_normalize_entries__mutmut_43': x_normalize_entries__mutmut_43, 
    'x_normalize_entries__mutmut_44': x_normalize_entries__mutmut_44, 
    'x_normalize_entries__mutmut_45': x_normalize_entries__mutmut_45, 
    'x_normalize_entries__mutmut_46': x_normalize_entries__mutmut_46, 
    'x_normalize_entries__mutmut_47': x_normalize_entries__mutmut_47, 
    'x_normalize_entries__mutmut_48': x_normalize_entries__mutmut_48, 
    'x_normalize_entries__mutmut_49': x_normalize_entries__mutmut_49, 
    'x_normalize_entries__mutmut_50': x_normalize_entries__mutmut_50, 
    'x_normalize_entries__mutmut_51': x_normalize_entries__mutmut_51, 
    'x_normalize_entries__mutmut_52': x_normalize_entries__mutmut_52, 
    'x_normalize_entries__mutmut_53': x_normalize_entries__mutmut_53, 
    'x_normalize_entries__mutmut_54': x_normalize_entries__mutmut_54, 
    'x_normalize_entries__mutmut_55': x_normalize_entries__mutmut_55, 
    'x_normalize_entries__mutmut_56': x_normalize_entries__mutmut_56
}
x_normalize_entries__mutmut_orig.__name__ = 'x_normalize_entries'


def collapse_duplicates(
    entries: list[NormalizedHistoryEntry],
) -> list[NormalizedHistoryEntry]:
    args = [entries]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_collapse_duplicates__mutmut_orig, x_collapse_duplicates__mutmut_mutants, args, kwargs, None)


def x_collapse_duplicates__mutmut_orig(
    entries: list[NormalizedHistoryEntry],
) -> list[NormalizedHistoryEntry]:
    """Remove consecutive entries with the same lane.

    Always keeps the first entry. For consecutive duplicates, only the
    first occurrence is retained.

    Args:
        entries: Normalized history entries.

    Returns:
        Collapsed list with no consecutive duplicate lanes.
    """
    if not entries:
        return []

    collapsed: list[NormalizedHistoryEntry] = [entries[0]]
    for entry in entries[1:]:
        if entry.lane != collapsed[-1].lane:
            collapsed.append(entry)
    return collapsed


def x_collapse_duplicates__mutmut_1(
    entries: list[NormalizedHistoryEntry],
) -> list[NormalizedHistoryEntry]:
    """Remove consecutive entries with the same lane.

    Always keeps the first entry. For consecutive duplicates, only the
    first occurrence is retained.

    Args:
        entries: Normalized history entries.

    Returns:
        Collapsed list with no consecutive duplicate lanes.
    """
    if entries:
        return []

    collapsed: list[NormalizedHistoryEntry] = [entries[0]]
    for entry in entries[1:]:
        if entry.lane != collapsed[-1].lane:
            collapsed.append(entry)
    return collapsed


def x_collapse_duplicates__mutmut_2(
    entries: list[NormalizedHistoryEntry],
) -> list[NormalizedHistoryEntry]:
    """Remove consecutive entries with the same lane.

    Always keeps the first entry. For consecutive duplicates, only the
    first occurrence is retained.

    Args:
        entries: Normalized history entries.

    Returns:
        Collapsed list with no consecutive duplicate lanes.
    """
    if not entries:
        return []

    collapsed: list[NormalizedHistoryEntry] = None
    for entry in entries[1:]:
        if entry.lane != collapsed[-1].lane:
            collapsed.append(entry)
    return collapsed


def x_collapse_duplicates__mutmut_3(
    entries: list[NormalizedHistoryEntry],
) -> list[NormalizedHistoryEntry]:
    """Remove consecutive entries with the same lane.

    Always keeps the first entry. For consecutive duplicates, only the
    first occurrence is retained.

    Args:
        entries: Normalized history entries.

    Returns:
        Collapsed list with no consecutive duplicate lanes.
    """
    if not entries:
        return []

    collapsed: list[NormalizedHistoryEntry] = [entries[1]]
    for entry in entries[1:]:
        if entry.lane != collapsed[-1].lane:
            collapsed.append(entry)
    return collapsed


def x_collapse_duplicates__mutmut_4(
    entries: list[NormalizedHistoryEntry],
) -> list[NormalizedHistoryEntry]:
    """Remove consecutive entries with the same lane.

    Always keeps the first entry. For consecutive duplicates, only the
    first occurrence is retained.

    Args:
        entries: Normalized history entries.

    Returns:
        Collapsed list with no consecutive duplicate lanes.
    """
    if not entries:
        return []

    collapsed: list[NormalizedHistoryEntry] = [entries[0]]
    for entry in entries[2:]:
        if entry.lane != collapsed[-1].lane:
            collapsed.append(entry)
    return collapsed


def x_collapse_duplicates__mutmut_5(
    entries: list[NormalizedHistoryEntry],
) -> list[NormalizedHistoryEntry]:
    """Remove consecutive entries with the same lane.

    Always keeps the first entry. For consecutive duplicates, only the
    first occurrence is retained.

    Args:
        entries: Normalized history entries.

    Returns:
        Collapsed list with no consecutive duplicate lanes.
    """
    if not entries:
        return []

    collapsed: list[NormalizedHistoryEntry] = [entries[0]]
    for entry in entries[1:]:
        if entry.lane == collapsed[-1].lane:
            collapsed.append(entry)
    return collapsed


def x_collapse_duplicates__mutmut_6(
    entries: list[NormalizedHistoryEntry],
) -> list[NormalizedHistoryEntry]:
    """Remove consecutive entries with the same lane.

    Always keeps the first entry. For consecutive duplicates, only the
    first occurrence is retained.

    Args:
        entries: Normalized history entries.

    Returns:
        Collapsed list with no consecutive duplicate lanes.
    """
    if not entries:
        return []

    collapsed: list[NormalizedHistoryEntry] = [entries[0]]
    for entry in entries[1:]:
        if entry.lane != collapsed[+1].lane:
            collapsed.append(entry)
    return collapsed


def x_collapse_duplicates__mutmut_7(
    entries: list[NormalizedHistoryEntry],
) -> list[NormalizedHistoryEntry]:
    """Remove consecutive entries with the same lane.

    Always keeps the first entry. For consecutive duplicates, only the
    first occurrence is retained.

    Args:
        entries: Normalized history entries.

    Returns:
        Collapsed list with no consecutive duplicate lanes.
    """
    if not entries:
        return []

    collapsed: list[NormalizedHistoryEntry] = [entries[0]]
    for entry in entries[1:]:
        if entry.lane != collapsed[-2].lane:
            collapsed.append(entry)
    return collapsed


def x_collapse_duplicates__mutmut_8(
    entries: list[NormalizedHistoryEntry],
) -> list[NormalizedHistoryEntry]:
    """Remove consecutive entries with the same lane.

    Always keeps the first entry. For consecutive duplicates, only the
    first occurrence is retained.

    Args:
        entries: Normalized history entries.

    Returns:
        Collapsed list with no consecutive duplicate lanes.
    """
    if not entries:
        return []

    collapsed: list[NormalizedHistoryEntry] = [entries[0]]
    for entry in entries[1:]:
        if entry.lane != collapsed[-1].lane:
            collapsed.append(None)
    return collapsed

x_collapse_duplicates__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_collapse_duplicates__mutmut_1': x_collapse_duplicates__mutmut_1, 
    'x_collapse_duplicates__mutmut_2': x_collapse_duplicates__mutmut_2, 
    'x_collapse_duplicates__mutmut_3': x_collapse_duplicates__mutmut_3, 
    'x_collapse_duplicates__mutmut_4': x_collapse_duplicates__mutmut_4, 
    'x_collapse_duplicates__mutmut_5': x_collapse_duplicates__mutmut_5, 
    'x_collapse_duplicates__mutmut_6': x_collapse_duplicates__mutmut_6, 
    'x_collapse_duplicates__mutmut_7': x_collapse_duplicates__mutmut_7, 
    'x_collapse_duplicates__mutmut_8': x_collapse_duplicates__mutmut_8
}
x_collapse_duplicates__mutmut_orig.__name__ = 'x_collapse_duplicates'


def pair_transitions(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    args = [entries]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_pair_transitions__mutmut_orig, x_pair_transitions__mutmut_mutants, args, kwargs, None)


def x_pair_transitions__mutmut_orig(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_1(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) <= 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_2(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 3:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_3(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = None
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_4(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(None):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_5(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) + 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_6(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 2):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_7(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            None
        )
    return transitions


def x_pair_transitions__mutmut_8(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=None,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_9(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=None,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_10(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=None,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_11(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 1].timestamp,
                actor=None,
            )
        )
    return transitions


def x_pair_transitions__mutmut_12(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_13(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_14(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_15(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 1].timestamp,
                )
        )
    return transitions


def x_pair_transitions__mutmut_16(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i - 1].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_17(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 2].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_18(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i - 1].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_19(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 2].timestamp,
                actor=entries[i + 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_20(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i - 1].actor,
            )
        )
    return transitions


def x_pair_transitions__mutmut_21(entries: list[NormalizedHistoryEntry]) -> list[Transition]:
    """Convert normalized entries into transitions by pairing adjacent entries.

    Each transition uses the target entry's timestamp and actor (the agent
    who caused the transition TO the new lane).

    Args:
        entries: Normalized, collapsed history entries.

    Returns:
        List of Transition objects. Empty if fewer than 2 entries.
    """
    if len(entries) < 2:
        return []

    transitions: list[Transition] = []
    for i in range(len(entries) - 1):
        transitions.append(
            Transition(
                from_lane=entries[i].lane,
                to_lane=entries[i + 1].lane,
                timestamp=entries[i + 1].timestamp,
                actor=entries[i + 2].actor,
            )
        )
    return transitions

x_pair_transitions__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_pair_transitions__mutmut_1': x_pair_transitions__mutmut_1, 
    'x_pair_transitions__mutmut_2': x_pair_transitions__mutmut_2, 
    'x_pair_transitions__mutmut_3': x_pair_transitions__mutmut_3, 
    'x_pair_transitions__mutmut_4': x_pair_transitions__mutmut_4, 
    'x_pair_transitions__mutmut_5': x_pair_transitions__mutmut_5, 
    'x_pair_transitions__mutmut_6': x_pair_transitions__mutmut_6, 
    'x_pair_transitions__mutmut_7': x_pair_transitions__mutmut_7, 
    'x_pair_transitions__mutmut_8': x_pair_transitions__mutmut_8, 
    'x_pair_transitions__mutmut_9': x_pair_transitions__mutmut_9, 
    'x_pair_transitions__mutmut_10': x_pair_transitions__mutmut_10, 
    'x_pair_transitions__mutmut_11': x_pair_transitions__mutmut_11, 
    'x_pair_transitions__mutmut_12': x_pair_transitions__mutmut_12, 
    'x_pair_transitions__mutmut_13': x_pair_transitions__mutmut_13, 
    'x_pair_transitions__mutmut_14': x_pair_transitions__mutmut_14, 
    'x_pair_transitions__mutmut_15': x_pair_transitions__mutmut_15, 
    'x_pair_transitions__mutmut_16': x_pair_transitions__mutmut_16, 
    'x_pair_transitions__mutmut_17': x_pair_transitions__mutmut_17, 
    'x_pair_transitions__mutmut_18': x_pair_transitions__mutmut_18, 
    'x_pair_transitions__mutmut_19': x_pair_transitions__mutmut_19, 
    'x_pair_transitions__mutmut_20': x_pair_transitions__mutmut_20, 
    'x_pair_transitions__mutmut_21': x_pair_transitions__mutmut_21
}
x_pair_transitions__mutmut_orig.__name__ = 'x_pair_transitions'


def gap_fill(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    args = [transitions, last_history_lane, current_lane, fallback_timestamp]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_gap_fill__mutmut_orig, x_gap_fill__mutmut_mutants, args, kwargs, None)


def x_gap_fill__mutmut_orig(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_1(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is not None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_2(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane != "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_3(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "XXplannedXX":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_4(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "PLANNED":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_5(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane=None,
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_6(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=None,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_7(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=None,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_8(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor=None,
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_9(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_10(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_11(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_12(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_13(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="XXplannedXX",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_14(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="PLANNED",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_15(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="XXmigrationXX",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_16(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="MIGRATION",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_17(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane != current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_18(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = None
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_19(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(None)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_20(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        None
    )
    return result


def x_gap_fill__mutmut_21(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=None,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_22(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=None,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_23(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=None,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_24(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor=None,
        )
    )
    return result


def x_gap_fill__mutmut_25(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_26(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            timestamp=fallback_timestamp,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_27(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            actor="migration",
        )
    )
    return result


def x_gap_fill__mutmut_28(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            )
    )
    return result


def x_gap_fill__mutmut_29(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="XXmigrationXX",
        )
    )
    return result


def x_gap_fill__mutmut_30(
    transitions: list[Transition],
    last_history_lane: str | None,
    current_lane: str,
    fallback_timestamp: str,
) -> list[Transition]:
    """Add a gap-fill transition if the last history lane differs from current.

    Handles 4 cases:
    1. No history, current is planned: return empty (no transitions needed)
    2. No history, current is not planned: bootstrap planned -> current
    3. Last history matches current: return transitions unchanged
    4. Last history differs from current: append gap-fill transition

    Args:
        transitions: Existing transitions from history pairs.
        last_history_lane: Lane of the last collapsed history entry, or None.
        current_lane: Current frontmatter lane (alias-resolved).
        fallback_timestamp: Timestamp to use for the gap-fill transition.

    Returns:
        Updated list of transitions.
    """
    if last_history_lane is None:
        if current_lane == "planned":
            return []
        return [
            Transition(
                from_lane="planned",
                to_lane=current_lane,
                timestamp=fallback_timestamp,
                actor="migration",
            )
        ]

    if last_history_lane == current_lane:
        return transitions

    result = list(transitions)
    result.append(
        Transition(
            from_lane=last_history_lane,
            to_lane=current_lane,
            timestamp=fallback_timestamp,
            actor="MIGRATION",
        )
    )
    return result

x_gap_fill__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_gap_fill__mutmut_1': x_gap_fill__mutmut_1, 
    'x_gap_fill__mutmut_2': x_gap_fill__mutmut_2, 
    'x_gap_fill__mutmut_3': x_gap_fill__mutmut_3, 
    'x_gap_fill__mutmut_4': x_gap_fill__mutmut_4, 
    'x_gap_fill__mutmut_5': x_gap_fill__mutmut_5, 
    'x_gap_fill__mutmut_6': x_gap_fill__mutmut_6, 
    'x_gap_fill__mutmut_7': x_gap_fill__mutmut_7, 
    'x_gap_fill__mutmut_8': x_gap_fill__mutmut_8, 
    'x_gap_fill__mutmut_9': x_gap_fill__mutmut_9, 
    'x_gap_fill__mutmut_10': x_gap_fill__mutmut_10, 
    'x_gap_fill__mutmut_11': x_gap_fill__mutmut_11, 
    'x_gap_fill__mutmut_12': x_gap_fill__mutmut_12, 
    'x_gap_fill__mutmut_13': x_gap_fill__mutmut_13, 
    'x_gap_fill__mutmut_14': x_gap_fill__mutmut_14, 
    'x_gap_fill__mutmut_15': x_gap_fill__mutmut_15, 
    'x_gap_fill__mutmut_16': x_gap_fill__mutmut_16, 
    'x_gap_fill__mutmut_17': x_gap_fill__mutmut_17, 
    'x_gap_fill__mutmut_18': x_gap_fill__mutmut_18, 
    'x_gap_fill__mutmut_19': x_gap_fill__mutmut_19, 
    'x_gap_fill__mutmut_20': x_gap_fill__mutmut_20, 
    'x_gap_fill__mutmut_21': x_gap_fill__mutmut_21, 
    'x_gap_fill__mutmut_22': x_gap_fill__mutmut_22, 
    'x_gap_fill__mutmut_23': x_gap_fill__mutmut_23, 
    'x_gap_fill__mutmut_24': x_gap_fill__mutmut_24, 
    'x_gap_fill__mutmut_25': x_gap_fill__mutmut_25, 
    'x_gap_fill__mutmut_26': x_gap_fill__mutmut_26, 
    'x_gap_fill__mutmut_27': x_gap_fill__mutmut_27, 
    'x_gap_fill__mutmut_28': x_gap_fill__mutmut_28, 
    'x_gap_fill__mutmut_29': x_gap_fill__mutmut_29, 
    'x_gap_fill__mutmut_30': x_gap_fill__mutmut_30
}
x_gap_fill__mutmut_orig.__name__ = 'x_gap_fill'


def extract_done_evidence(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    args = [frontmatter, wp_id]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_extract_done_evidence__mutmut_orig, x_extract_done_evidence__mutmut_mutants, args, kwargs, None)


def x_extract_done_evidence__mutmut_orig(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_1(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = None
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_2(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get(None)
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_3(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("XXreview_statusXX")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_4(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("REVIEW_STATUS")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_5(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = None

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_6(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get(None)

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_7(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("XXreviewed_byXX")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_8(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("REVIEWED_BY")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_9(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by or str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_10(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" or reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_11(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status != "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_12(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "XXapprovedXX" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_13(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "APPROVED" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_14(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(None).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_15(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=None
        )
    return None


def x_extract_done_evidence__mutmut_16(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=None,
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_17(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict=None,
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_18(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                reference=None,
            )
        )
    return None


def x_extract_done_evidence__mutmut_19(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_20(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_21(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="approved",
                )
        )
    return None


def x_extract_done_evidence__mutmut_22(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(None).strip(),
                verdict="approved",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_23(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="XXapprovedXX",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None


def x_extract_done_evidence__mutmut_24(frontmatter: dict[str, Any], wp_id: str) -> DoneEvidence | None:
    """Build DoneEvidence from frontmatter review fields.

    Only produces evidence when review_status is "approved" AND
    reviewed_by is non-empty.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID for the reference field.

    Returns:
        DoneEvidence if review approval is present, None otherwise.
    """
    review_status = frontmatter.get("review_status")
    reviewed_by = frontmatter.get("reviewed_by")

    if review_status == "approved" and reviewed_by and str(reviewed_by).strip():
        return DoneEvidence(
            review=ReviewApproval(
                reviewer=str(reviewed_by).strip(),
                verdict="APPROVED",
                reference=f"frontmatter-migration:{wp_id}",
            )
        )
    return None

x_extract_done_evidence__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_extract_done_evidence__mutmut_1': x_extract_done_evidence__mutmut_1, 
    'x_extract_done_evidence__mutmut_2': x_extract_done_evidence__mutmut_2, 
    'x_extract_done_evidence__mutmut_3': x_extract_done_evidence__mutmut_3, 
    'x_extract_done_evidence__mutmut_4': x_extract_done_evidence__mutmut_4, 
    'x_extract_done_evidence__mutmut_5': x_extract_done_evidence__mutmut_5, 
    'x_extract_done_evidence__mutmut_6': x_extract_done_evidence__mutmut_6, 
    'x_extract_done_evidence__mutmut_7': x_extract_done_evidence__mutmut_7, 
    'x_extract_done_evidence__mutmut_8': x_extract_done_evidence__mutmut_8, 
    'x_extract_done_evidence__mutmut_9': x_extract_done_evidence__mutmut_9, 
    'x_extract_done_evidence__mutmut_10': x_extract_done_evidence__mutmut_10, 
    'x_extract_done_evidence__mutmut_11': x_extract_done_evidence__mutmut_11, 
    'x_extract_done_evidence__mutmut_12': x_extract_done_evidence__mutmut_12, 
    'x_extract_done_evidence__mutmut_13': x_extract_done_evidence__mutmut_13, 
    'x_extract_done_evidence__mutmut_14': x_extract_done_evidence__mutmut_14, 
    'x_extract_done_evidence__mutmut_15': x_extract_done_evidence__mutmut_15, 
    'x_extract_done_evidence__mutmut_16': x_extract_done_evidence__mutmut_16, 
    'x_extract_done_evidence__mutmut_17': x_extract_done_evidence__mutmut_17, 
    'x_extract_done_evidence__mutmut_18': x_extract_done_evidence__mutmut_18, 
    'x_extract_done_evidence__mutmut_19': x_extract_done_evidence__mutmut_19, 
    'x_extract_done_evidence__mutmut_20': x_extract_done_evidence__mutmut_20, 
    'x_extract_done_evidence__mutmut_21': x_extract_done_evidence__mutmut_21, 
    'x_extract_done_evidence__mutmut_22': x_extract_done_evidence__mutmut_22, 
    'x_extract_done_evidence__mutmut_23': x_extract_done_evidence__mutmut_23, 
    'x_extract_done_evidence__mutmut_24': x_extract_done_evidence__mutmut_24
}
x_extract_done_evidence__mutmut_orig.__name__ = 'x_extract_done_evidence'


def build_transition_chain(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    args = [frontmatter, wp_id]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_build_transition_chain__mutmut_orig, x_build_transition_chain__mutmut_mutants, args, kwargs, None)


def x_build_transition_chain__mutmut_orig(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_1(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = None
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_2(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get(None, [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_3(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", None)
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_4(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get([])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_5(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", )
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_6(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("XXhistoryXX", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_7(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("HISTORY", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_8(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_9(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = None

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_10(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = None
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_11(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() and "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_12(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(None).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_13(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get(None, "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_14(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", None)).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_15(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_16(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", )).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_17(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("XXlaneXX", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_18(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("LANE", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_19(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "XXplannedXX")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_20(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "PLANNED")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_21(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "XXplannedXX"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_22(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "PLANNED"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_23(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = None

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_24(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(None)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_25(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = None

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_26(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(None)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_27(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = None

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_28(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(None)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_29(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = None

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_30(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(None)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_31(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_32(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[+1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_33(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-2].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_34(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = None
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_35(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[+1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_36(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-2].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_37(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = None

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_38(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(None).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_39(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = None

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_40(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        None, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_41(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, None, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_42(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, None, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_43(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, None
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_44(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_45(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_46(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_47(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_48(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = None
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_49(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(None, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_50(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, None)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_51(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_52(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, )
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_53(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = None

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_54(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = True

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_55(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_56(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = None
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_57(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane != "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_58(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "XXdoneXX":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_59(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "DONE":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_60(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    None
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_61(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=None,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_62(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=None,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_63(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=None,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_64(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=None,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_65(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=None,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_66(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_67(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_68(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_69(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_70(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_71(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = None
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_72(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = False
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_73(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(None)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_74(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = None

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_75(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=None,
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_76(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=None,
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_77(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        has_evidence=None,
    )


def x_build_transition_chain__mutmut_78(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        history_entries=len(history),
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_79(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        has_evidence=has_evidence,
    )


def x_build_transition_chain__mutmut_80(
    frontmatter: dict[str, Any],
    wp_id: str,
) -> TransitionChain:
    """Reconstruct a full transition chain from WP frontmatter.

    Main entry point that orchestrates: normalize -> collapse -> pair ->
    gap_fill -> attach evidence.

    Args:
        frontmatter: Full WP frontmatter dict.
        wp_id: Work package ID.

    Returns:
        TransitionChain with all reconstructed transitions.
    """
    history: list[dict[str, Any]] = frontmatter.get("history", [])
    if not isinstance(history, list):
        history = []

    raw_lane = str(frontmatter.get("lane", "planned")).strip() or "planned"
    current_lane = resolve_lane_alias(raw_lane)

    # Step 1: Normalize
    normalized = normalize_entries(history)

    # Step 2: Collapse consecutive duplicates
    collapsed = collapse_duplicates(normalized)

    # Step 3: Pair into transitions
    transitions = pair_transitions(collapsed)

    # Step 4: Gap-fill to current lane
    last_history_lane = collapsed[-1].lane if collapsed else None
    if collapsed:
        fallback_timestamp = collapsed[-1].timestamp
    else:
        fallback_timestamp = datetime.now(timezone.utc).isoformat()

    final_transitions = gap_fill(
        transitions, last_history_lane, current_lane, fallback_timestamp
    )

    # Step 5: Attach DoneEvidence to transitions targeting "done"
    evidence = extract_done_evidence(frontmatter, wp_id)
    has_evidence = False

    if evidence is not None:
        updated: list[Transition] = []
        for t in final_transitions:
            if t.to_lane == "done":
                updated.append(
                    Transition(
                        from_lane=t.from_lane,
                        to_lane=t.to_lane,
                        timestamp=t.timestamp,
                        actor=t.actor,
                        evidence=evidence,
                    )
                )
                has_evidence = True
            else:
                updated.append(t)
        final_transitions = updated

    return TransitionChain(
        transitions=final_transitions,
        history_entries=len(history),
        )

x_build_transition_chain__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_build_transition_chain__mutmut_1': x_build_transition_chain__mutmut_1, 
    'x_build_transition_chain__mutmut_2': x_build_transition_chain__mutmut_2, 
    'x_build_transition_chain__mutmut_3': x_build_transition_chain__mutmut_3, 
    'x_build_transition_chain__mutmut_4': x_build_transition_chain__mutmut_4, 
    'x_build_transition_chain__mutmut_5': x_build_transition_chain__mutmut_5, 
    'x_build_transition_chain__mutmut_6': x_build_transition_chain__mutmut_6, 
    'x_build_transition_chain__mutmut_7': x_build_transition_chain__mutmut_7, 
    'x_build_transition_chain__mutmut_8': x_build_transition_chain__mutmut_8, 
    'x_build_transition_chain__mutmut_9': x_build_transition_chain__mutmut_9, 
    'x_build_transition_chain__mutmut_10': x_build_transition_chain__mutmut_10, 
    'x_build_transition_chain__mutmut_11': x_build_transition_chain__mutmut_11, 
    'x_build_transition_chain__mutmut_12': x_build_transition_chain__mutmut_12, 
    'x_build_transition_chain__mutmut_13': x_build_transition_chain__mutmut_13, 
    'x_build_transition_chain__mutmut_14': x_build_transition_chain__mutmut_14, 
    'x_build_transition_chain__mutmut_15': x_build_transition_chain__mutmut_15, 
    'x_build_transition_chain__mutmut_16': x_build_transition_chain__mutmut_16, 
    'x_build_transition_chain__mutmut_17': x_build_transition_chain__mutmut_17, 
    'x_build_transition_chain__mutmut_18': x_build_transition_chain__mutmut_18, 
    'x_build_transition_chain__mutmut_19': x_build_transition_chain__mutmut_19, 
    'x_build_transition_chain__mutmut_20': x_build_transition_chain__mutmut_20, 
    'x_build_transition_chain__mutmut_21': x_build_transition_chain__mutmut_21, 
    'x_build_transition_chain__mutmut_22': x_build_transition_chain__mutmut_22, 
    'x_build_transition_chain__mutmut_23': x_build_transition_chain__mutmut_23, 
    'x_build_transition_chain__mutmut_24': x_build_transition_chain__mutmut_24, 
    'x_build_transition_chain__mutmut_25': x_build_transition_chain__mutmut_25, 
    'x_build_transition_chain__mutmut_26': x_build_transition_chain__mutmut_26, 
    'x_build_transition_chain__mutmut_27': x_build_transition_chain__mutmut_27, 
    'x_build_transition_chain__mutmut_28': x_build_transition_chain__mutmut_28, 
    'x_build_transition_chain__mutmut_29': x_build_transition_chain__mutmut_29, 
    'x_build_transition_chain__mutmut_30': x_build_transition_chain__mutmut_30, 
    'x_build_transition_chain__mutmut_31': x_build_transition_chain__mutmut_31, 
    'x_build_transition_chain__mutmut_32': x_build_transition_chain__mutmut_32, 
    'x_build_transition_chain__mutmut_33': x_build_transition_chain__mutmut_33, 
    'x_build_transition_chain__mutmut_34': x_build_transition_chain__mutmut_34, 
    'x_build_transition_chain__mutmut_35': x_build_transition_chain__mutmut_35, 
    'x_build_transition_chain__mutmut_36': x_build_transition_chain__mutmut_36, 
    'x_build_transition_chain__mutmut_37': x_build_transition_chain__mutmut_37, 
    'x_build_transition_chain__mutmut_38': x_build_transition_chain__mutmut_38, 
    'x_build_transition_chain__mutmut_39': x_build_transition_chain__mutmut_39, 
    'x_build_transition_chain__mutmut_40': x_build_transition_chain__mutmut_40, 
    'x_build_transition_chain__mutmut_41': x_build_transition_chain__mutmut_41, 
    'x_build_transition_chain__mutmut_42': x_build_transition_chain__mutmut_42, 
    'x_build_transition_chain__mutmut_43': x_build_transition_chain__mutmut_43, 
    'x_build_transition_chain__mutmut_44': x_build_transition_chain__mutmut_44, 
    'x_build_transition_chain__mutmut_45': x_build_transition_chain__mutmut_45, 
    'x_build_transition_chain__mutmut_46': x_build_transition_chain__mutmut_46, 
    'x_build_transition_chain__mutmut_47': x_build_transition_chain__mutmut_47, 
    'x_build_transition_chain__mutmut_48': x_build_transition_chain__mutmut_48, 
    'x_build_transition_chain__mutmut_49': x_build_transition_chain__mutmut_49, 
    'x_build_transition_chain__mutmut_50': x_build_transition_chain__mutmut_50, 
    'x_build_transition_chain__mutmut_51': x_build_transition_chain__mutmut_51, 
    'x_build_transition_chain__mutmut_52': x_build_transition_chain__mutmut_52, 
    'x_build_transition_chain__mutmut_53': x_build_transition_chain__mutmut_53, 
    'x_build_transition_chain__mutmut_54': x_build_transition_chain__mutmut_54, 
    'x_build_transition_chain__mutmut_55': x_build_transition_chain__mutmut_55, 
    'x_build_transition_chain__mutmut_56': x_build_transition_chain__mutmut_56, 
    'x_build_transition_chain__mutmut_57': x_build_transition_chain__mutmut_57, 
    'x_build_transition_chain__mutmut_58': x_build_transition_chain__mutmut_58, 
    'x_build_transition_chain__mutmut_59': x_build_transition_chain__mutmut_59, 
    'x_build_transition_chain__mutmut_60': x_build_transition_chain__mutmut_60, 
    'x_build_transition_chain__mutmut_61': x_build_transition_chain__mutmut_61, 
    'x_build_transition_chain__mutmut_62': x_build_transition_chain__mutmut_62, 
    'x_build_transition_chain__mutmut_63': x_build_transition_chain__mutmut_63, 
    'x_build_transition_chain__mutmut_64': x_build_transition_chain__mutmut_64, 
    'x_build_transition_chain__mutmut_65': x_build_transition_chain__mutmut_65, 
    'x_build_transition_chain__mutmut_66': x_build_transition_chain__mutmut_66, 
    'x_build_transition_chain__mutmut_67': x_build_transition_chain__mutmut_67, 
    'x_build_transition_chain__mutmut_68': x_build_transition_chain__mutmut_68, 
    'x_build_transition_chain__mutmut_69': x_build_transition_chain__mutmut_69, 
    'x_build_transition_chain__mutmut_70': x_build_transition_chain__mutmut_70, 
    'x_build_transition_chain__mutmut_71': x_build_transition_chain__mutmut_71, 
    'x_build_transition_chain__mutmut_72': x_build_transition_chain__mutmut_72, 
    'x_build_transition_chain__mutmut_73': x_build_transition_chain__mutmut_73, 
    'x_build_transition_chain__mutmut_74': x_build_transition_chain__mutmut_74, 
    'x_build_transition_chain__mutmut_75': x_build_transition_chain__mutmut_75, 
    'x_build_transition_chain__mutmut_76': x_build_transition_chain__mutmut_76, 
    'x_build_transition_chain__mutmut_77': x_build_transition_chain__mutmut_77, 
    'x_build_transition_chain__mutmut_78': x_build_transition_chain__mutmut_78, 
    'x_build_transition_chain__mutmut_79': x_build_transition_chain__mutmut_79, 
    'x_build_transition_chain__mutmut_80': x_build_transition_chain__mutmut_80
}
x_build_transition_chain__mutmut_orig.__name__ = 'x_build_transition_chain'
