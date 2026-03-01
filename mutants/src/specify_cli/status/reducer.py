"""Deterministic reducer for status event logs.

Replays a list of StatusEvent records into a StatusSnapshot, applying
deduplication, deterministic sorting, and rollback-aware conflict
resolution for concurrent events from parallel worktrees.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import Lane, StatusEvent, StatusSnapshot
from .store import read_events

SNAPSHOT_FILENAME = "status.json"
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


def _now_utc() -> str:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__now_utc__mutmut_orig, x__now_utc__mutmut_mutants, args, kwargs, None)


def x__now_utc__mutmut_orig() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def x__now_utc__mutmut_1() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(None).isoformat()

x__now_utc__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__now_utc__mutmut_1': x__now_utc__mutmut_1
}
x__now_utc__mutmut_orig.__name__ = 'x__now_utc'


def _is_rollback_event(event: StatusEvent) -> bool:
    args = [event]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__is_rollback_event__mutmut_orig, x__is_rollback_event__mutmut_mutants, args, kwargs, None)


def x__is_rollback_event__mutmut_orig(event: StatusEvent) -> bool:
    """Check if an event represents a reviewer rollback.

    A rollback is a transition from for_review back to in_progress
    with a review reference (indicating a reviewer requested changes).
    """
    return (
        event.from_lane == Lane.FOR_REVIEW
        and event.to_lane == Lane.IN_PROGRESS
        and event.review_ref is not None
    )


def x__is_rollback_event__mutmut_1(event: StatusEvent) -> bool:
    """Check if an event represents a reviewer rollback.

    A rollback is a transition from for_review back to in_progress
    with a review reference (indicating a reviewer requested changes).
    """
    return (
        event.from_lane == Lane.FOR_REVIEW
        and event.to_lane == Lane.IN_PROGRESS or event.review_ref is not None
    )


def x__is_rollback_event__mutmut_2(event: StatusEvent) -> bool:
    """Check if an event represents a reviewer rollback.

    A rollback is a transition from for_review back to in_progress
    with a review reference (indicating a reviewer requested changes).
    """
    return (
        event.from_lane == Lane.FOR_REVIEW or event.to_lane == Lane.IN_PROGRESS
        and event.review_ref is not None
    )


def x__is_rollback_event__mutmut_3(event: StatusEvent) -> bool:
    """Check if an event represents a reviewer rollback.

    A rollback is a transition from for_review back to in_progress
    with a review reference (indicating a reviewer requested changes).
    """
    return (
        event.from_lane != Lane.FOR_REVIEW
        and event.to_lane == Lane.IN_PROGRESS
        and event.review_ref is not None
    )


def x__is_rollback_event__mutmut_4(event: StatusEvent) -> bool:
    """Check if an event represents a reviewer rollback.

    A rollback is a transition from for_review back to in_progress
    with a review reference (indicating a reviewer requested changes).
    """
    return (
        event.from_lane == Lane.FOR_REVIEW
        and event.to_lane != Lane.IN_PROGRESS
        and event.review_ref is not None
    )


def x__is_rollback_event__mutmut_5(event: StatusEvent) -> bool:
    """Check if an event represents a reviewer rollback.

    A rollback is a transition from for_review back to in_progress
    with a review reference (indicating a reviewer requested changes).
    """
    return (
        event.from_lane == Lane.FOR_REVIEW
        and event.to_lane == Lane.IN_PROGRESS
        and event.review_ref is None
    )

x__is_rollback_event__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__is_rollback_event__mutmut_1': x__is_rollback_event__mutmut_1, 
    'x__is_rollback_event__mutmut_2': x__is_rollback_event__mutmut_2, 
    'x__is_rollback_event__mutmut_3': x__is_rollback_event__mutmut_3, 
    'x__is_rollback_event__mutmut_4': x__is_rollback_event__mutmut_4, 
    'x__is_rollback_event__mutmut_5': x__is_rollback_event__mutmut_5
}
x__is_rollback_event__mutmut_orig.__name__ = 'x__is_rollback_event'


def _wp_state_from_event(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    args = [event, previous]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__wp_state_from_event__mutmut_orig, x__wp_state_from_event__mutmut_mutants, args, kwargs, None)


def x__wp_state_from_event__mutmut_orig(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_1(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = None
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_2(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 1
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_3(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_4(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = None

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_5(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get(None, 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_6(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", None)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_7(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get(0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_8(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", )

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_9(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("XXforce_countXX", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_10(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("FORCE_COUNT", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_11(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 1)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_12(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "XXlaneXX": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_13(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "LANE": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_14(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(None),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_15(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "XXactorXX": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_16(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "ACTOR": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_17(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "XXlast_transition_atXX": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_18(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "LAST_TRANSITION_AT": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_19(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "XXlast_event_idXX": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_20(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "LAST_EVENT_ID": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_21(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "XXforce_countXX": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_22(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "FORCE_COUNT": prior_force_count + (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_23(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count - (1 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_24(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (2 if event.force else 0),
    }


def x__wp_state_from_event__mutmut_25(
    event: StatusEvent,
    previous: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a WP state dict from an event, optionally carrying forward
    the force_count from the previous state.
    """
    prior_force_count = 0
    if previous is not None:
        prior_force_count = previous.get("force_count", 0)

    return {
        "lane": str(event.to_lane),
        "actor": event.actor,
        "last_transition_at": event.at,
        "last_event_id": event.event_id,
        "force_count": prior_force_count + (1 if event.force else 1),
    }

x__wp_state_from_event__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__wp_state_from_event__mutmut_1': x__wp_state_from_event__mutmut_1, 
    'x__wp_state_from_event__mutmut_2': x__wp_state_from_event__mutmut_2, 
    'x__wp_state_from_event__mutmut_3': x__wp_state_from_event__mutmut_3, 
    'x__wp_state_from_event__mutmut_4': x__wp_state_from_event__mutmut_4, 
    'x__wp_state_from_event__mutmut_5': x__wp_state_from_event__mutmut_5, 
    'x__wp_state_from_event__mutmut_6': x__wp_state_from_event__mutmut_6, 
    'x__wp_state_from_event__mutmut_7': x__wp_state_from_event__mutmut_7, 
    'x__wp_state_from_event__mutmut_8': x__wp_state_from_event__mutmut_8, 
    'x__wp_state_from_event__mutmut_9': x__wp_state_from_event__mutmut_9, 
    'x__wp_state_from_event__mutmut_10': x__wp_state_from_event__mutmut_10, 
    'x__wp_state_from_event__mutmut_11': x__wp_state_from_event__mutmut_11, 
    'x__wp_state_from_event__mutmut_12': x__wp_state_from_event__mutmut_12, 
    'x__wp_state_from_event__mutmut_13': x__wp_state_from_event__mutmut_13, 
    'x__wp_state_from_event__mutmut_14': x__wp_state_from_event__mutmut_14, 
    'x__wp_state_from_event__mutmut_15': x__wp_state_from_event__mutmut_15, 
    'x__wp_state_from_event__mutmut_16': x__wp_state_from_event__mutmut_16, 
    'x__wp_state_from_event__mutmut_17': x__wp_state_from_event__mutmut_17, 
    'x__wp_state_from_event__mutmut_18': x__wp_state_from_event__mutmut_18, 
    'x__wp_state_from_event__mutmut_19': x__wp_state_from_event__mutmut_19, 
    'x__wp_state_from_event__mutmut_20': x__wp_state_from_event__mutmut_20, 
    'x__wp_state_from_event__mutmut_21': x__wp_state_from_event__mutmut_21, 
    'x__wp_state_from_event__mutmut_22': x__wp_state_from_event__mutmut_22, 
    'x__wp_state_from_event__mutmut_23': x__wp_state_from_event__mutmut_23, 
    'x__wp_state_from_event__mutmut_24': x__wp_state_from_event__mutmut_24, 
    'x__wp_state_from_event__mutmut_25': x__wp_state_from_event__mutmut_25
}
x__wp_state_from_event__mutmut_orig.__name__ = 'x__wp_state_from_event'


def _should_apply_event(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    args = [current_state, new_event, all_events]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__should_apply_event__mutmut_orig, x__should_apply_event__mutmut_mutants, args, kwargs, None)


def x__should_apply_event__mutmut_orig(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_1(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is not None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_2(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return False

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_3(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = None
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_4(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get(None)
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_5(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("XXlast_event_idXX")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_6(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("LAST_EVENT_ID")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_7(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = None

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_8(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get(None)

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_9(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("XXlast_transition_atXX")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_10(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("LAST_TRANSITION_AT")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_11(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp != new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_12(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(None):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_13(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = ""
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_14(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id != current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_15(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = None
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_16(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    return
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_17(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None or not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_18(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_19(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_20(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                None
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_21(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return False  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_22(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_23(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = ""
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_24(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id != current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_25(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = None
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_26(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    return
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_27(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None or _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_28(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_29(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                None
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_30(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_31(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(None):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_32(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return True  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return True


def x__should_apply_event__mutmut_33(
    current_state: dict[str, Any] | None,
    new_event: StatusEvent,
    all_events: list[StatusEvent],
) -> bool:
    """Determine whether new_event should be applied given the current state.

    Implements rollback-aware precedence: if the current state was set by
    a forward transition and a concurrent rollback event exists for the
    same WP, the rollback wins.

    If there is no current state, the event always applies.
    If events are not concurrent (different timestamps), the later one
    wins naturally through sort order.
    """
    if current_state is None:
        return True

    current_event_id = current_state.get("last_event_id")
    current_timestamp = current_state.get("last_transition_at")

    # If this event has the same timestamp as the current state's event,
    # they are concurrent. Check rollback precedence.
    if current_timestamp == new_event.at:
        # If the new event is a rollback, it beats a forward transition
        if _is_rollback_event(new_event):
            # Check if the current state was set by a non-rollback event
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and not _is_rollback_event(
                current_setter
            ):
                return True  # Rollback beats forward

        # If the current state was set by a rollback, don't let a
        # concurrent forward event override it
        if current_event_id is not None:
            current_setter = None
            for ev in all_events:
                if ev.event_id == current_event_id:
                    current_setter = ev
                    break
            if current_setter is not None and _is_rollback_event(
                current_setter
            ):
                if not _is_rollback_event(new_event):
                    return False  # Forward does not beat rollback

    # Default: apply the event (later in sort order wins)
    return False

x__should_apply_event__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__should_apply_event__mutmut_1': x__should_apply_event__mutmut_1, 
    'x__should_apply_event__mutmut_2': x__should_apply_event__mutmut_2, 
    'x__should_apply_event__mutmut_3': x__should_apply_event__mutmut_3, 
    'x__should_apply_event__mutmut_4': x__should_apply_event__mutmut_4, 
    'x__should_apply_event__mutmut_5': x__should_apply_event__mutmut_5, 
    'x__should_apply_event__mutmut_6': x__should_apply_event__mutmut_6, 
    'x__should_apply_event__mutmut_7': x__should_apply_event__mutmut_7, 
    'x__should_apply_event__mutmut_8': x__should_apply_event__mutmut_8, 
    'x__should_apply_event__mutmut_9': x__should_apply_event__mutmut_9, 
    'x__should_apply_event__mutmut_10': x__should_apply_event__mutmut_10, 
    'x__should_apply_event__mutmut_11': x__should_apply_event__mutmut_11, 
    'x__should_apply_event__mutmut_12': x__should_apply_event__mutmut_12, 
    'x__should_apply_event__mutmut_13': x__should_apply_event__mutmut_13, 
    'x__should_apply_event__mutmut_14': x__should_apply_event__mutmut_14, 
    'x__should_apply_event__mutmut_15': x__should_apply_event__mutmut_15, 
    'x__should_apply_event__mutmut_16': x__should_apply_event__mutmut_16, 
    'x__should_apply_event__mutmut_17': x__should_apply_event__mutmut_17, 
    'x__should_apply_event__mutmut_18': x__should_apply_event__mutmut_18, 
    'x__should_apply_event__mutmut_19': x__should_apply_event__mutmut_19, 
    'x__should_apply_event__mutmut_20': x__should_apply_event__mutmut_20, 
    'x__should_apply_event__mutmut_21': x__should_apply_event__mutmut_21, 
    'x__should_apply_event__mutmut_22': x__should_apply_event__mutmut_22, 
    'x__should_apply_event__mutmut_23': x__should_apply_event__mutmut_23, 
    'x__should_apply_event__mutmut_24': x__should_apply_event__mutmut_24, 
    'x__should_apply_event__mutmut_25': x__should_apply_event__mutmut_25, 
    'x__should_apply_event__mutmut_26': x__should_apply_event__mutmut_26, 
    'x__should_apply_event__mutmut_27': x__should_apply_event__mutmut_27, 
    'x__should_apply_event__mutmut_28': x__should_apply_event__mutmut_28, 
    'x__should_apply_event__mutmut_29': x__should_apply_event__mutmut_29, 
    'x__should_apply_event__mutmut_30': x__should_apply_event__mutmut_30, 
    'x__should_apply_event__mutmut_31': x__should_apply_event__mutmut_31, 
    'x__should_apply_event__mutmut_32': x__should_apply_event__mutmut_32, 
    'x__should_apply_event__mutmut_33': x__should_apply_event__mutmut_33
}
x__should_apply_event__mutmut_orig.__name__ = 'x__should_apply_event'


def reduce(events: list[StatusEvent]) -> StatusSnapshot:
    args = [events]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_reduce__mutmut_orig, x_reduce__mutmut_mutants, args, kwargs, None)


def x_reduce__mutmut_orig(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_1(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_2(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug=None,
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_3(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=None,
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_4(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=None,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_5(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages=None,
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_6(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary=None,
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_7(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_8(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_9(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_10(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_11(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_12(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_13(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="XXXX",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_14(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=1,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_15(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 1 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_16(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = None
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_17(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = None
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_18(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_19(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(None)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_20(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(None)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_21(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = None

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_22(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(None, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_23(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=None)

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_24(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_25(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, )

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_26(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: None)

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_27(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = None
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_28(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = None

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_29(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[1].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_30(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = None
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_31(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(None)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_32(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(None, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_33(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, None, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_34(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, None):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_35(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_36(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_37(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, ):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_38(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = None

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_39(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(None, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_40(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, None)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_41(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_42(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, )

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_43(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = None
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_44(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 1 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_45(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = None
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_46(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["XXlaneXX"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_47(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["LANE"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_48(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val not in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_49(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] = 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_50(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] -= 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_51(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 2

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_52(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=None,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_53(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=None,
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_54(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=None,
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_55(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=None,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_56(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=None,
        summary=summary,
    )


def x_reduce__mutmut_57(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=None,
    )


def x_reduce__mutmut_58(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_59(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_60(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_61(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_62(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        summary=summary,
    )


def x_reduce__mutmut_63(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-1].event_id,
        work_packages=wp_states,
        )


def x_reduce__mutmut_64(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[+1].event_id,
        work_packages=wp_states,
        summary=summary,
    )


def x_reduce__mutmut_65(events: list[StatusEvent]) -> StatusSnapshot:
    """Deterministically reduce a list of events into a snapshot.

    Algorithm:
    1. Deduplicate by event_id (keep first occurrence)
    2. Sort by (at, event_id) ascending
    3. Iterate and track current lane per WP
    4. Apply rollback-aware precedence for concurrent events
    5. Build summary counts for all 7 lanes

    Empty events returns a snapshot with feature_slug="", all zero
    counts, and no work packages.
    """
    if not events:
        return StatusSnapshot(
            feature_slug="",
            materialized_at=_now_utc(),
            event_count=0,
            last_event_id=None,
            work_packages={},
            summary={lane.value: 0 for lane in Lane},
        )

    # Step 1: Deduplicate by event_id (keep first occurrence)
    seen_ids: set[str] = set()
    unique_events: list[StatusEvent] = []
    for event in events:
        if event.event_id not in seen_ids:
            seen_ids.add(event.event_id)
            unique_events.append(event)

    # Step 2: Sort by (at, event_id) ascending
    sorted_events = sorted(unique_events, key=lambda e: (e.at, e.event_id))

    # Step 3 & 4: Iterate and apply events with rollback-aware precedence
    wp_states: dict[str, dict[str, Any]] = {}
    feature_slug = sorted_events[0].feature_slug

    for event in sorted_events:
        current = wp_states.get(event.wp_id)
        if _should_apply_event(current, event, sorted_events):
            wp_states[event.wp_id] = _wp_state_from_event(event, current)

    # Step 5: Build summary counts
    summary: dict[str, int] = {lane.value: 0 for lane in Lane}
    for wp_state in wp_states.values():
        lane_val = wp_state["lane"]
        if lane_val in summary:
            summary[lane_val] += 1

    return StatusSnapshot(
        feature_slug=feature_slug,
        materialized_at=_now_utc(),
        event_count=len(sorted_events),
        last_event_id=sorted_events[-2].event_id,
        work_packages=wp_states,
        summary=summary,
    )

x_reduce__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_reduce__mutmut_1': x_reduce__mutmut_1, 
    'x_reduce__mutmut_2': x_reduce__mutmut_2, 
    'x_reduce__mutmut_3': x_reduce__mutmut_3, 
    'x_reduce__mutmut_4': x_reduce__mutmut_4, 
    'x_reduce__mutmut_5': x_reduce__mutmut_5, 
    'x_reduce__mutmut_6': x_reduce__mutmut_6, 
    'x_reduce__mutmut_7': x_reduce__mutmut_7, 
    'x_reduce__mutmut_8': x_reduce__mutmut_8, 
    'x_reduce__mutmut_9': x_reduce__mutmut_9, 
    'x_reduce__mutmut_10': x_reduce__mutmut_10, 
    'x_reduce__mutmut_11': x_reduce__mutmut_11, 
    'x_reduce__mutmut_12': x_reduce__mutmut_12, 
    'x_reduce__mutmut_13': x_reduce__mutmut_13, 
    'x_reduce__mutmut_14': x_reduce__mutmut_14, 
    'x_reduce__mutmut_15': x_reduce__mutmut_15, 
    'x_reduce__mutmut_16': x_reduce__mutmut_16, 
    'x_reduce__mutmut_17': x_reduce__mutmut_17, 
    'x_reduce__mutmut_18': x_reduce__mutmut_18, 
    'x_reduce__mutmut_19': x_reduce__mutmut_19, 
    'x_reduce__mutmut_20': x_reduce__mutmut_20, 
    'x_reduce__mutmut_21': x_reduce__mutmut_21, 
    'x_reduce__mutmut_22': x_reduce__mutmut_22, 
    'x_reduce__mutmut_23': x_reduce__mutmut_23, 
    'x_reduce__mutmut_24': x_reduce__mutmut_24, 
    'x_reduce__mutmut_25': x_reduce__mutmut_25, 
    'x_reduce__mutmut_26': x_reduce__mutmut_26, 
    'x_reduce__mutmut_27': x_reduce__mutmut_27, 
    'x_reduce__mutmut_28': x_reduce__mutmut_28, 
    'x_reduce__mutmut_29': x_reduce__mutmut_29, 
    'x_reduce__mutmut_30': x_reduce__mutmut_30, 
    'x_reduce__mutmut_31': x_reduce__mutmut_31, 
    'x_reduce__mutmut_32': x_reduce__mutmut_32, 
    'x_reduce__mutmut_33': x_reduce__mutmut_33, 
    'x_reduce__mutmut_34': x_reduce__mutmut_34, 
    'x_reduce__mutmut_35': x_reduce__mutmut_35, 
    'x_reduce__mutmut_36': x_reduce__mutmut_36, 
    'x_reduce__mutmut_37': x_reduce__mutmut_37, 
    'x_reduce__mutmut_38': x_reduce__mutmut_38, 
    'x_reduce__mutmut_39': x_reduce__mutmut_39, 
    'x_reduce__mutmut_40': x_reduce__mutmut_40, 
    'x_reduce__mutmut_41': x_reduce__mutmut_41, 
    'x_reduce__mutmut_42': x_reduce__mutmut_42, 
    'x_reduce__mutmut_43': x_reduce__mutmut_43, 
    'x_reduce__mutmut_44': x_reduce__mutmut_44, 
    'x_reduce__mutmut_45': x_reduce__mutmut_45, 
    'x_reduce__mutmut_46': x_reduce__mutmut_46, 
    'x_reduce__mutmut_47': x_reduce__mutmut_47, 
    'x_reduce__mutmut_48': x_reduce__mutmut_48, 
    'x_reduce__mutmut_49': x_reduce__mutmut_49, 
    'x_reduce__mutmut_50': x_reduce__mutmut_50, 
    'x_reduce__mutmut_51': x_reduce__mutmut_51, 
    'x_reduce__mutmut_52': x_reduce__mutmut_52, 
    'x_reduce__mutmut_53': x_reduce__mutmut_53, 
    'x_reduce__mutmut_54': x_reduce__mutmut_54, 
    'x_reduce__mutmut_55': x_reduce__mutmut_55, 
    'x_reduce__mutmut_56': x_reduce__mutmut_56, 
    'x_reduce__mutmut_57': x_reduce__mutmut_57, 
    'x_reduce__mutmut_58': x_reduce__mutmut_58, 
    'x_reduce__mutmut_59': x_reduce__mutmut_59, 
    'x_reduce__mutmut_60': x_reduce__mutmut_60, 
    'x_reduce__mutmut_61': x_reduce__mutmut_61, 
    'x_reduce__mutmut_62': x_reduce__mutmut_62, 
    'x_reduce__mutmut_63': x_reduce__mutmut_63, 
    'x_reduce__mutmut_64': x_reduce__mutmut_64, 
    'x_reduce__mutmut_65': x_reduce__mutmut_65
}
x_reduce__mutmut_orig.__name__ = 'x_reduce'


def materialize_to_json(snapshot: StatusSnapshot) -> str:
    args = [snapshot]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_materialize_to_json__mutmut_orig, x_materialize_to_json__mutmut_mutants, args, kwargs, None)


def x_materialize_to_json__mutmut_orig(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            snapshot.to_dict(),
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


def x_materialize_to_json__mutmut_1(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            snapshot.to_dict(),
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
        ) - "\n"
    )


def x_materialize_to_json__mutmut_2(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            None,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


def x_materialize_to_json__mutmut_3(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            snapshot.to_dict(),
            sort_keys=None,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


def x_materialize_to_json__mutmut_4(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            snapshot.to_dict(),
            sort_keys=True,
            indent=None,
            ensure_ascii=False,
        )
        + "\n"
    )


def x_materialize_to_json__mutmut_5(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            snapshot.to_dict(),
            sort_keys=True,
            indent=2,
            ensure_ascii=None,
        )
        + "\n"
    )


def x_materialize_to_json__mutmut_6(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


def x_materialize_to_json__mutmut_7(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            snapshot.to_dict(),
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


def x_materialize_to_json__mutmut_8(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            snapshot.to_dict(),
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n"
    )


def x_materialize_to_json__mutmut_9(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            snapshot.to_dict(),
            sort_keys=True,
            indent=2,
            )
        + "\n"
    )


def x_materialize_to_json__mutmut_10(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            snapshot.to_dict(),
            sort_keys=False,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


def x_materialize_to_json__mutmut_11(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            snapshot.to_dict(),
            sort_keys=True,
            indent=3,
            ensure_ascii=False,
        )
        + "\n"
    )


def x_materialize_to_json__mutmut_12(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            snapshot.to_dict(),
            sort_keys=True,
            indent=2,
            ensure_ascii=True,
        )
        + "\n"
    )


def x_materialize_to_json__mutmut_13(snapshot: StatusSnapshot) -> str:
    """Serialize a snapshot to a deterministic JSON string.

    Uses ``sort_keys=True``, ``indent=2``, and ``ensure_ascii=False``
    for human-readable, byte-identical output across platforms.
    Returns the JSON string with a trailing newline.
    """
    return (
        json.dumps(
            snapshot.to_dict(),
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
        )
        + "XX\nXX"
    )

x_materialize_to_json__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_materialize_to_json__mutmut_1': x_materialize_to_json__mutmut_1, 
    'x_materialize_to_json__mutmut_2': x_materialize_to_json__mutmut_2, 
    'x_materialize_to_json__mutmut_3': x_materialize_to_json__mutmut_3, 
    'x_materialize_to_json__mutmut_4': x_materialize_to_json__mutmut_4, 
    'x_materialize_to_json__mutmut_5': x_materialize_to_json__mutmut_5, 
    'x_materialize_to_json__mutmut_6': x_materialize_to_json__mutmut_6, 
    'x_materialize_to_json__mutmut_7': x_materialize_to_json__mutmut_7, 
    'x_materialize_to_json__mutmut_8': x_materialize_to_json__mutmut_8, 
    'x_materialize_to_json__mutmut_9': x_materialize_to_json__mutmut_9, 
    'x_materialize_to_json__mutmut_10': x_materialize_to_json__mutmut_10, 
    'x_materialize_to_json__mutmut_11': x_materialize_to_json__mutmut_11, 
    'x_materialize_to_json__mutmut_12': x_materialize_to_json__mutmut_12, 
    'x_materialize_to_json__mutmut_13': x_materialize_to_json__mutmut_13
}
x_materialize_to_json__mutmut_orig.__name__ = 'x_materialize_to_json'


def materialize(feature_dir: Path) -> StatusSnapshot:
    args = [feature_dir]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_materialize__mutmut_orig, x_materialize__mutmut_mutants, args, kwargs, None)


def x_materialize__mutmut_orig(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_1(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = None
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_2(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(None)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_3(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = None
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_4(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(None)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_5(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = None

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_6(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(None)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_7(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = None
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_8(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir * SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_9(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = None

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_10(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir * (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_11(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME - ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_12(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + "XX.tmpXX")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_13(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".TMP")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_14(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=None, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_15(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=None)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_16(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_17(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, )
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_18(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=False, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_19(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=False)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_20(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(None, encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_21(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding=None)
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_22(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(encoding="utf-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_23(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, )
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_24(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="XXutf-8XX")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_25(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="UTF-8")
    os.replace(str(tmp_path), str(out_path))

    return snapshot


def x_materialize__mutmut_26(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(None, str(out_path))

    return snapshot


def x_materialize__mutmut_27(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), None)

    return snapshot


def x_materialize__mutmut_28(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(out_path))

    return snapshot


def x_materialize__mutmut_29(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), )

    return snapshot


def x_materialize__mutmut_30(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(None), str(out_path))

    return snapshot


def x_materialize__mutmut_31(feature_dir: Path) -> StatusSnapshot:
    """Read events, reduce to snapshot, and write status.json atomically.

    Writes to a temporary file first, then uses ``os.replace`` for an
    atomic rename to avoid partial writes.

    Returns the materialized snapshot.
    """
    events = read_events(feature_dir)
    snapshot = reduce(events)
    json_str = materialize_to_json(snapshot)

    out_path = feature_dir / SNAPSHOT_FILENAME
    tmp_path = feature_dir / (SNAPSHOT_FILENAME + ".tmp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_str, encoding="utf-8")
    os.replace(str(tmp_path), str(None))

    return snapshot

x_materialize__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_materialize__mutmut_1': x_materialize__mutmut_1, 
    'x_materialize__mutmut_2': x_materialize__mutmut_2, 
    'x_materialize__mutmut_3': x_materialize__mutmut_3, 
    'x_materialize__mutmut_4': x_materialize__mutmut_4, 
    'x_materialize__mutmut_5': x_materialize__mutmut_5, 
    'x_materialize__mutmut_6': x_materialize__mutmut_6, 
    'x_materialize__mutmut_7': x_materialize__mutmut_7, 
    'x_materialize__mutmut_8': x_materialize__mutmut_8, 
    'x_materialize__mutmut_9': x_materialize__mutmut_9, 
    'x_materialize__mutmut_10': x_materialize__mutmut_10, 
    'x_materialize__mutmut_11': x_materialize__mutmut_11, 
    'x_materialize__mutmut_12': x_materialize__mutmut_12, 
    'x_materialize__mutmut_13': x_materialize__mutmut_13, 
    'x_materialize__mutmut_14': x_materialize__mutmut_14, 
    'x_materialize__mutmut_15': x_materialize__mutmut_15, 
    'x_materialize__mutmut_16': x_materialize__mutmut_16, 
    'x_materialize__mutmut_17': x_materialize__mutmut_17, 
    'x_materialize__mutmut_18': x_materialize__mutmut_18, 
    'x_materialize__mutmut_19': x_materialize__mutmut_19, 
    'x_materialize__mutmut_20': x_materialize__mutmut_20, 
    'x_materialize__mutmut_21': x_materialize__mutmut_21, 
    'x_materialize__mutmut_22': x_materialize__mutmut_22, 
    'x_materialize__mutmut_23': x_materialize__mutmut_23, 
    'x_materialize__mutmut_24': x_materialize__mutmut_24, 
    'x_materialize__mutmut_25': x_materialize__mutmut_25, 
    'x_materialize__mutmut_26': x_materialize__mutmut_26, 
    'x_materialize__mutmut_27': x_materialize__mutmut_27, 
    'x_materialize__mutmut_28': x_materialize__mutmut_28, 
    'x_materialize__mutmut_29': x_materialize__mutmut_29, 
    'x_materialize__mutmut_30': x_materialize__mutmut_30, 
    'x_materialize__mutmut_31': x_materialize__mutmut_31
}
x_materialize__mutmut_orig.__name__ = 'x_materialize'
