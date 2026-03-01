"""Status emit orchestration pipeline.

Single entry point for ALL state changes in the canonical status model.
Validates a transition, appends an event to the JSONL log, materializes
a status snapshot, updates legacy compatibility views, and emits SaaS
telemetry.

Pipeline order (critical -- do not reorder):
    1. resolve_lane_alias(to_lane)
    2. Derive from_lane from last event for this WP (or "planned")
    3. validate_transition(from_lane, resolved_lane, ...)
    4. Create StatusEvent with ULID event_id
    5. store.append_event(feature_dir, event)
    6. reducer.materialize(feature_dir)
    7. legacy_bridge.update_all_views(feature_dir, snapshot)  [try/except]
    8. _saas_fan_out(event, feature_slug, repo_root)
    9. Return the event
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ulid as _ulid_mod

from .models import (
    DoneEvidence,
    Lane,
    RepoEvidence,
    ReviewApproval,
    StatusEvent,
    VerificationResult,
)
from .transitions import resolve_lane_alias, validate_transition
from . import store as _store
from . import reducer as _reducer

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

class TransitionError(Exception):
    """Raised when a status transition is invalid."""


def _generate_ulid() -> str:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__generate_ulid__mutmut_orig, x__generate_ulid__mutmut_mutants, args, kwargs, None)


def x__generate_ulid__mutmut_orig() -> str:
    """Generate a new ULID string."""
    if hasattr(_ulid_mod, "new"):
        return _ulid_mod.new().str
    return str(_ulid_mod.ULID())


def x__generate_ulid__mutmut_1() -> str:
    """Generate a new ULID string."""
    if hasattr(None, "new"):
        return _ulid_mod.new().str
    return str(_ulid_mod.ULID())


def x__generate_ulid__mutmut_2() -> str:
    """Generate a new ULID string."""
    if hasattr(_ulid_mod, None):
        return _ulid_mod.new().str
    return str(_ulid_mod.ULID())


def x__generate_ulid__mutmut_3() -> str:
    """Generate a new ULID string."""
    if hasattr("new"):
        return _ulid_mod.new().str
    return str(_ulid_mod.ULID())


def x__generate_ulid__mutmut_4() -> str:
    """Generate a new ULID string."""
    if hasattr(_ulid_mod, ):
        return _ulid_mod.new().str
    return str(_ulid_mod.ULID())


def x__generate_ulid__mutmut_5() -> str:
    """Generate a new ULID string."""
    if hasattr(_ulid_mod, "XXnewXX"):
        return _ulid_mod.new().str
    return str(_ulid_mod.ULID())


def x__generate_ulid__mutmut_6() -> str:
    """Generate a new ULID string."""
    if hasattr(_ulid_mod, "NEW"):
        return _ulid_mod.new().str
    return str(_ulid_mod.ULID())


def x__generate_ulid__mutmut_7() -> str:
    """Generate a new ULID string."""
    if hasattr(_ulid_mod, "new"):
        return _ulid_mod.new().str
    return str(None)

x__generate_ulid__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__generate_ulid__mutmut_1': x__generate_ulid__mutmut_1, 
    'x__generate_ulid__mutmut_2': x__generate_ulid__mutmut_2, 
    'x__generate_ulid__mutmut_3': x__generate_ulid__mutmut_3, 
    'x__generate_ulid__mutmut_4': x__generate_ulid__mutmut_4, 
    'x__generate_ulid__mutmut_5': x__generate_ulid__mutmut_5, 
    'x__generate_ulid__mutmut_6': x__generate_ulid__mutmut_6, 
    'x__generate_ulid__mutmut_7': x__generate_ulid__mutmut_7
}
x__generate_ulid__mutmut_orig.__name__ = 'x__generate_ulid'


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


def _derive_from_lane(feature_dir: Path, wp_id: str) -> str:
    args = [feature_dir, wp_id]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__derive_from_lane__mutmut_orig, x__derive_from_lane__mutmut_mutants, args, kwargs, None)


def x__derive_from_lane__mutmut_orig(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_1(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = None
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_2(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(None)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_3(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_4(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "XXplannedXX"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_5(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "PLANNED"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_6(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = None
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_7(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(None)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_8(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = None
    if wp_state is None:
        return "planned"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_9(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(None)
    if wp_state is None:
        return "planned"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_10(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is not None:
        return "planned"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_11(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "XXplannedXX"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_12(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "PLANNED"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_13(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = None
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_14(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = wp_state.get(None)
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_15(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = wp_state.get("XXlaneXX")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_16(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = wp_state.get("LANE")
    if isinstance(lane, str):
        return lane
    return "planned"


def x__derive_from_lane__mutmut_17(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "XXplannedXX"


def x__derive_from_lane__mutmut_18(feature_dir: Path, wp_id: str) -> str:
    """Derive the current lane for a WP from canonical reduced state.

    The event log may not be append-ordered by logical transition time,
    so we must reduce the full log to determine the current lane
    deterministically.
    """
    events = _store.read_events(feature_dir)
    if not events:
        return "planned"

    snapshot = _reducer.reduce(events)
    wp_state = snapshot.work_packages.get(wp_id)
    if wp_state is None:
        return "planned"

    lane = wp_state.get("lane")
    if isinstance(lane, str):
        return lane
    return "PLANNED"

x__derive_from_lane__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__derive_from_lane__mutmut_1': x__derive_from_lane__mutmut_1, 
    'x__derive_from_lane__mutmut_2': x__derive_from_lane__mutmut_2, 
    'x__derive_from_lane__mutmut_3': x__derive_from_lane__mutmut_3, 
    'x__derive_from_lane__mutmut_4': x__derive_from_lane__mutmut_4, 
    'x__derive_from_lane__mutmut_5': x__derive_from_lane__mutmut_5, 
    'x__derive_from_lane__mutmut_6': x__derive_from_lane__mutmut_6, 
    'x__derive_from_lane__mutmut_7': x__derive_from_lane__mutmut_7, 
    'x__derive_from_lane__mutmut_8': x__derive_from_lane__mutmut_8, 
    'x__derive_from_lane__mutmut_9': x__derive_from_lane__mutmut_9, 
    'x__derive_from_lane__mutmut_10': x__derive_from_lane__mutmut_10, 
    'x__derive_from_lane__mutmut_11': x__derive_from_lane__mutmut_11, 
    'x__derive_from_lane__mutmut_12': x__derive_from_lane__mutmut_12, 
    'x__derive_from_lane__mutmut_13': x__derive_from_lane__mutmut_13, 
    'x__derive_from_lane__mutmut_14': x__derive_from_lane__mutmut_14, 
    'x__derive_from_lane__mutmut_15': x__derive_from_lane__mutmut_15, 
    'x__derive_from_lane__mutmut_16': x__derive_from_lane__mutmut_16, 
    'x__derive_from_lane__mutmut_17': x__derive_from_lane__mutmut_17, 
    'x__derive_from_lane__mutmut_18': x__derive_from_lane__mutmut_18
}
x__derive_from_lane__mutmut_orig.__name__ = 'x__derive_from_lane'


def _build_done_evidence(evidence: dict[str, Any]) -> DoneEvidence:
    args = [evidence]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__build_done_evidence__mutmut_orig, x__build_done_evidence__mutmut_mutants, args, kwargs, None)


def x__build_done_evidence__mutmut_orig(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_1(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = None
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_2(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get(None)
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_3(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("XXreviewXX")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_4(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("REVIEW")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_5(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_6(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            None
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_7(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "XXMoving to done requires evidence with review.reviewer XX"
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_8(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_9(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "MOVING TO DONE REQUIRES EVIDENCE WITH REVIEW.REVIEWER "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_10(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "XXreview.verdict, and review.referenceXX"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_11(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "REVIEW.VERDICT, AND REVIEW.REFERENCE"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_12(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = None
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_13(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get(None)
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_14(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("XXreviewerXX")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_15(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("REVIEWER")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_16(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = None
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_17(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get(None)
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_18(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("XXverdictXX")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_19(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("VERDICT")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_20(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = None
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_21(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get(None)
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_22(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("XXreferenceXX")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_23(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("REFERENCE")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_24(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference and not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_25(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict and not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_26(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer and not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_27(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_28(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_29(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_30(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_31(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(None).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_32(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            None
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_33(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "XXMoving to done requires evidence with review.reviewer XX"
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_34(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_35(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "MOVING TO DONE REQUIRES EVIDENCE WITH REVIEW.REVIEWER "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_36(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "XXreview.verdict, and review.referenceXX"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_37(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "REVIEW.VERDICT, AND REVIEW.REFERENCE"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_38(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = None

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_39(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=None,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_40(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=None,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_41(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=None,
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_42(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_43(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_44(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_45(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(None),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_46(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = None
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_47(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get(None, [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_48(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", None)
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_49(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get([])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_50(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", )
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_51(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("XXreposXX", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_52(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("REPOS", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_53(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = None

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_54(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get(None, [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_55(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", None)
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_56(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get([])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_57(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", )
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_58(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("XXverificationXX", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_59(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("VERIFICATION", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_60(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=None,
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_61(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=None,
        verification=verification,
    )


def x__build_done_evidence__mutmut_62(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        verification=None,
    )


def x__build_done_evidence__mutmut_63(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        repos=repos,
        verification=verification,
    )


def x__build_done_evidence__mutmut_64(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        verification=verification,
    )


def x__build_done_evidence__mutmut_65(evidence: dict[str, Any]) -> DoneEvidence:
    """Build a DoneEvidence dataclass from a raw dict.

    Raises TransitionError if the evidence dict is missing required
    fields (review.reviewer, review.verdict, review.reference).
    """
    review_data = evidence.get("review")
    if not isinstance(review_data, dict):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )
    reviewer = review_data.get("reviewer")
    verdict = review_data.get("verdict")
    reference = review_data.get("reference")
    if (
        not reviewer
        or not verdict
        or not reference
        or not str(reference).strip()
    ):
        raise TransitionError(
            "Moving to done requires evidence with review.reviewer "
            "review.verdict, and review.reference"
        )

    review_approval = ReviewApproval(
        reviewer=reviewer,
        verdict=verdict,
        reference=str(reference),
    )

    repos = [
        RepoEvidence(**r) for r in evidence.get("repos", [])
    ]
    verification = [
        VerificationResult(**v) for v in evidence.get("verification", [])
    ]

    return DoneEvidence(
        review=review_approval,
        repos=repos,
        )

x__build_done_evidence__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__build_done_evidence__mutmut_1': x__build_done_evidence__mutmut_1, 
    'x__build_done_evidence__mutmut_2': x__build_done_evidence__mutmut_2, 
    'x__build_done_evidence__mutmut_3': x__build_done_evidence__mutmut_3, 
    'x__build_done_evidence__mutmut_4': x__build_done_evidence__mutmut_4, 
    'x__build_done_evidence__mutmut_5': x__build_done_evidence__mutmut_5, 
    'x__build_done_evidence__mutmut_6': x__build_done_evidence__mutmut_6, 
    'x__build_done_evidence__mutmut_7': x__build_done_evidence__mutmut_7, 
    'x__build_done_evidence__mutmut_8': x__build_done_evidence__mutmut_8, 
    'x__build_done_evidence__mutmut_9': x__build_done_evidence__mutmut_9, 
    'x__build_done_evidence__mutmut_10': x__build_done_evidence__mutmut_10, 
    'x__build_done_evidence__mutmut_11': x__build_done_evidence__mutmut_11, 
    'x__build_done_evidence__mutmut_12': x__build_done_evidence__mutmut_12, 
    'x__build_done_evidence__mutmut_13': x__build_done_evidence__mutmut_13, 
    'x__build_done_evidence__mutmut_14': x__build_done_evidence__mutmut_14, 
    'x__build_done_evidence__mutmut_15': x__build_done_evidence__mutmut_15, 
    'x__build_done_evidence__mutmut_16': x__build_done_evidence__mutmut_16, 
    'x__build_done_evidence__mutmut_17': x__build_done_evidence__mutmut_17, 
    'x__build_done_evidence__mutmut_18': x__build_done_evidence__mutmut_18, 
    'x__build_done_evidence__mutmut_19': x__build_done_evidence__mutmut_19, 
    'x__build_done_evidence__mutmut_20': x__build_done_evidence__mutmut_20, 
    'x__build_done_evidence__mutmut_21': x__build_done_evidence__mutmut_21, 
    'x__build_done_evidence__mutmut_22': x__build_done_evidence__mutmut_22, 
    'x__build_done_evidence__mutmut_23': x__build_done_evidence__mutmut_23, 
    'x__build_done_evidence__mutmut_24': x__build_done_evidence__mutmut_24, 
    'x__build_done_evidence__mutmut_25': x__build_done_evidence__mutmut_25, 
    'x__build_done_evidence__mutmut_26': x__build_done_evidence__mutmut_26, 
    'x__build_done_evidence__mutmut_27': x__build_done_evidence__mutmut_27, 
    'x__build_done_evidence__mutmut_28': x__build_done_evidence__mutmut_28, 
    'x__build_done_evidence__mutmut_29': x__build_done_evidence__mutmut_29, 
    'x__build_done_evidence__mutmut_30': x__build_done_evidence__mutmut_30, 
    'x__build_done_evidence__mutmut_31': x__build_done_evidence__mutmut_31, 
    'x__build_done_evidence__mutmut_32': x__build_done_evidence__mutmut_32, 
    'x__build_done_evidence__mutmut_33': x__build_done_evidence__mutmut_33, 
    'x__build_done_evidence__mutmut_34': x__build_done_evidence__mutmut_34, 
    'x__build_done_evidence__mutmut_35': x__build_done_evidence__mutmut_35, 
    'x__build_done_evidence__mutmut_36': x__build_done_evidence__mutmut_36, 
    'x__build_done_evidence__mutmut_37': x__build_done_evidence__mutmut_37, 
    'x__build_done_evidence__mutmut_38': x__build_done_evidence__mutmut_38, 
    'x__build_done_evidence__mutmut_39': x__build_done_evidence__mutmut_39, 
    'x__build_done_evidence__mutmut_40': x__build_done_evidence__mutmut_40, 
    'x__build_done_evidence__mutmut_41': x__build_done_evidence__mutmut_41, 
    'x__build_done_evidence__mutmut_42': x__build_done_evidence__mutmut_42, 
    'x__build_done_evidence__mutmut_43': x__build_done_evidence__mutmut_43, 
    'x__build_done_evidence__mutmut_44': x__build_done_evidence__mutmut_44, 
    'x__build_done_evidence__mutmut_45': x__build_done_evidence__mutmut_45, 
    'x__build_done_evidence__mutmut_46': x__build_done_evidence__mutmut_46, 
    'x__build_done_evidence__mutmut_47': x__build_done_evidence__mutmut_47, 
    'x__build_done_evidence__mutmut_48': x__build_done_evidence__mutmut_48, 
    'x__build_done_evidence__mutmut_49': x__build_done_evidence__mutmut_49, 
    'x__build_done_evidence__mutmut_50': x__build_done_evidence__mutmut_50, 
    'x__build_done_evidence__mutmut_51': x__build_done_evidence__mutmut_51, 
    'x__build_done_evidence__mutmut_52': x__build_done_evidence__mutmut_52, 
    'x__build_done_evidence__mutmut_53': x__build_done_evidence__mutmut_53, 
    'x__build_done_evidence__mutmut_54': x__build_done_evidence__mutmut_54, 
    'x__build_done_evidence__mutmut_55': x__build_done_evidence__mutmut_55, 
    'x__build_done_evidence__mutmut_56': x__build_done_evidence__mutmut_56, 
    'x__build_done_evidence__mutmut_57': x__build_done_evidence__mutmut_57, 
    'x__build_done_evidence__mutmut_58': x__build_done_evidence__mutmut_58, 
    'x__build_done_evidence__mutmut_59': x__build_done_evidence__mutmut_59, 
    'x__build_done_evidence__mutmut_60': x__build_done_evidence__mutmut_60, 
    'x__build_done_evidence__mutmut_61': x__build_done_evidence__mutmut_61, 
    'x__build_done_evidence__mutmut_62': x__build_done_evidence__mutmut_62, 
    'x__build_done_evidence__mutmut_63': x__build_done_evidence__mutmut_63, 
    'x__build_done_evidence__mutmut_64': x__build_done_evidence__mutmut_64, 
    'x__build_done_evidence__mutmut_65': x__build_done_evidence__mutmut_65
}
x__build_done_evidence__mutmut_orig.__name__ = 'x__build_done_evidence'


def _infer_subtasks_complete(feature_dir: Path, wp_id: str) -> bool:
    args = [feature_dir, wp_id]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__infer_subtasks_complete__mutmut_orig, x__infer_subtasks_complete__mutmut_mutants, args, kwargs, None)


def x__infer_subtasks_complete__mutmut_orig(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_1(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = None
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_2(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir * "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_3(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "XXtasks.mdXX"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_4(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "TASKS.MD"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_5(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_6(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return False
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_7(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = None
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_8(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding=None)
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_9(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="XXutf-8XX")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_10(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="UTF-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_11(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = None
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_12(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = None
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_13(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = True
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_14(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = None

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_15(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = True

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_16(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(None, line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_17(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", None):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_18(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_19(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", ):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_20(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(None)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_21(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = None
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_22(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = False
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_23(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            break
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_24(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section or re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_25(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(None, line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_26(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", None):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_27(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_28(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", ):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_29(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"XX^##\s+XX", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_30(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            return
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_31(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_32(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            break
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_33(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(None, line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_34(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", None):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_35(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_36(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", ):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_37(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"XX^\s*-\s*\[\s*\]\s+XX", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_38(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = None
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_39(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = False
            break
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_40(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            return
    if not in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_41(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if in_wp_section:
        return True
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_42(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return False
    return not unchecked_found


def x__infer_subtasks_complete__mutmut_43(feature_dir: Path, wp_id: str) -> bool:
    """Infer subtask completion from tasks.md checkboxes for a WP section."""
    tasks_path = feature_dir / "tasks.md"
    if not tasks_path.exists():
        return True
    content = tasks_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_wp_section = False
    unchecked_found = False

    for line in lines:
        if re.search(rf"^##.*\b{re.escape(wp_id)}\b", line):
            in_wp_section = True
            continue
        if in_wp_section and re.search(r"^##\s+", line):
            break
        if not in_wp_section:
            continue
        if re.match(r"^\s*-\s*\[\s*\]\s+", line):
            unchecked_found = True
            break
    if not in_wp_section:
        return True
    return unchecked_found

x__infer_subtasks_complete__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__infer_subtasks_complete__mutmut_1': x__infer_subtasks_complete__mutmut_1, 
    'x__infer_subtasks_complete__mutmut_2': x__infer_subtasks_complete__mutmut_2, 
    'x__infer_subtasks_complete__mutmut_3': x__infer_subtasks_complete__mutmut_3, 
    'x__infer_subtasks_complete__mutmut_4': x__infer_subtasks_complete__mutmut_4, 
    'x__infer_subtasks_complete__mutmut_5': x__infer_subtasks_complete__mutmut_5, 
    'x__infer_subtasks_complete__mutmut_6': x__infer_subtasks_complete__mutmut_6, 
    'x__infer_subtasks_complete__mutmut_7': x__infer_subtasks_complete__mutmut_7, 
    'x__infer_subtasks_complete__mutmut_8': x__infer_subtasks_complete__mutmut_8, 
    'x__infer_subtasks_complete__mutmut_9': x__infer_subtasks_complete__mutmut_9, 
    'x__infer_subtasks_complete__mutmut_10': x__infer_subtasks_complete__mutmut_10, 
    'x__infer_subtasks_complete__mutmut_11': x__infer_subtasks_complete__mutmut_11, 
    'x__infer_subtasks_complete__mutmut_12': x__infer_subtasks_complete__mutmut_12, 
    'x__infer_subtasks_complete__mutmut_13': x__infer_subtasks_complete__mutmut_13, 
    'x__infer_subtasks_complete__mutmut_14': x__infer_subtasks_complete__mutmut_14, 
    'x__infer_subtasks_complete__mutmut_15': x__infer_subtasks_complete__mutmut_15, 
    'x__infer_subtasks_complete__mutmut_16': x__infer_subtasks_complete__mutmut_16, 
    'x__infer_subtasks_complete__mutmut_17': x__infer_subtasks_complete__mutmut_17, 
    'x__infer_subtasks_complete__mutmut_18': x__infer_subtasks_complete__mutmut_18, 
    'x__infer_subtasks_complete__mutmut_19': x__infer_subtasks_complete__mutmut_19, 
    'x__infer_subtasks_complete__mutmut_20': x__infer_subtasks_complete__mutmut_20, 
    'x__infer_subtasks_complete__mutmut_21': x__infer_subtasks_complete__mutmut_21, 
    'x__infer_subtasks_complete__mutmut_22': x__infer_subtasks_complete__mutmut_22, 
    'x__infer_subtasks_complete__mutmut_23': x__infer_subtasks_complete__mutmut_23, 
    'x__infer_subtasks_complete__mutmut_24': x__infer_subtasks_complete__mutmut_24, 
    'x__infer_subtasks_complete__mutmut_25': x__infer_subtasks_complete__mutmut_25, 
    'x__infer_subtasks_complete__mutmut_26': x__infer_subtasks_complete__mutmut_26, 
    'x__infer_subtasks_complete__mutmut_27': x__infer_subtasks_complete__mutmut_27, 
    'x__infer_subtasks_complete__mutmut_28': x__infer_subtasks_complete__mutmut_28, 
    'x__infer_subtasks_complete__mutmut_29': x__infer_subtasks_complete__mutmut_29, 
    'x__infer_subtasks_complete__mutmut_30': x__infer_subtasks_complete__mutmut_30, 
    'x__infer_subtasks_complete__mutmut_31': x__infer_subtasks_complete__mutmut_31, 
    'x__infer_subtasks_complete__mutmut_32': x__infer_subtasks_complete__mutmut_32, 
    'x__infer_subtasks_complete__mutmut_33': x__infer_subtasks_complete__mutmut_33, 
    'x__infer_subtasks_complete__mutmut_34': x__infer_subtasks_complete__mutmut_34, 
    'x__infer_subtasks_complete__mutmut_35': x__infer_subtasks_complete__mutmut_35, 
    'x__infer_subtasks_complete__mutmut_36': x__infer_subtasks_complete__mutmut_36, 
    'x__infer_subtasks_complete__mutmut_37': x__infer_subtasks_complete__mutmut_37, 
    'x__infer_subtasks_complete__mutmut_38': x__infer_subtasks_complete__mutmut_38, 
    'x__infer_subtasks_complete__mutmut_39': x__infer_subtasks_complete__mutmut_39, 
    'x__infer_subtasks_complete__mutmut_40': x__infer_subtasks_complete__mutmut_40, 
    'x__infer_subtasks_complete__mutmut_41': x__infer_subtasks_complete__mutmut_41, 
    'x__infer_subtasks_complete__mutmut_42': x__infer_subtasks_complete__mutmut_42, 
    'x__infer_subtasks_complete__mutmut_43': x__infer_subtasks_complete__mutmut_43
}
x__infer_subtasks_complete__mutmut_orig.__name__ = 'x__infer_subtasks_complete'


def _infer_implementation_evidence(feature_dir: Path, wp_id: str) -> bool:
    args = [feature_dir, wp_id]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__infer_implementation_evidence__mutmut_orig, x__infer_implementation_evidence__mutmut_mutants, args, kwargs, None)


def x__infer_implementation_evidence__mutmut_orig(feature_dir: Path, wp_id: str) -> bool:
    """Infer implementation evidence from prior canonical events for this WP."""
    for event in _store.read_events(feature_dir):
        if event.wp_id == wp_id:
            return True
    return False


def x__infer_implementation_evidence__mutmut_1(feature_dir: Path, wp_id: str) -> bool:
    """Infer implementation evidence from prior canonical events for this WP."""
    for event in _store.read_events(None):
        if event.wp_id == wp_id:
            return True
    return False


def x__infer_implementation_evidence__mutmut_2(feature_dir: Path, wp_id: str) -> bool:
    """Infer implementation evidence from prior canonical events for this WP."""
    for event in _store.read_events(feature_dir):
        if event.wp_id != wp_id:
            return True
    return False


def x__infer_implementation_evidence__mutmut_3(feature_dir: Path, wp_id: str) -> bool:
    """Infer implementation evidence from prior canonical events for this WP."""
    for event in _store.read_events(feature_dir):
        if event.wp_id == wp_id:
            return False
    return False


def x__infer_implementation_evidence__mutmut_4(feature_dir: Path, wp_id: str) -> bool:
    """Infer implementation evidence from prior canonical events for this WP."""
    for event in _store.read_events(feature_dir):
        if event.wp_id == wp_id:
            return True
    return True

x__infer_implementation_evidence__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__infer_implementation_evidence__mutmut_1': x__infer_implementation_evidence__mutmut_1, 
    'x__infer_implementation_evidence__mutmut_2': x__infer_implementation_evidence__mutmut_2, 
    'x__infer_implementation_evidence__mutmut_3': x__infer_implementation_evidence__mutmut_3, 
    'x__infer_implementation_evidence__mutmut_4': x__infer_implementation_evidence__mutmut_4
}
x__infer_implementation_evidence__mutmut_orig.__name__ = 'x__infer_implementation_evidence'


def emit_status_transition(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    args = [feature_dir, feature_slug, wp_id, to_lane, actor]# type: ignore
    kwargs = {'force': force, 'reason': reason, 'evidence': evidence, 'review_ref': review_ref, 'workspace_context': workspace_context, 'subtasks_complete': subtasks_complete, 'implementation_evidence_present': implementation_evidence_present, 'execution_mode': execution_mode, 'repo_root': repo_root, 'policy_metadata': policy_metadata}# type: ignore
    return _mutmut_trampoline(x_emit_status_transition__mutmut_orig, x_emit_status_transition__mutmut_mutants, args, kwargs, None)


def x_emit_status_transition__mutmut_orig(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_1(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = True,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_2(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "XXworktreeXX",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_3(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "WORKTREE",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_4(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = None

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_5(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(None)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_6(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = None

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_7(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(None, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_8(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, None)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_9(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_10(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, )

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_11(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is not None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_12(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = None
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_13(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_14(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = None
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_15(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress" or resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_16(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None or from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_17(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is not None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_18(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane != "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_19(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "XXin_progressXX"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_20(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "IN_PROGRESS"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_21(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane != "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_22(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "XXfor_reviewXX"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_23(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "FOR_REVIEW"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_24(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = None
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_25(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(None, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_26(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, None)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_27(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_28(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, )
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_29(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress" or resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_30(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None or from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_31(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is not None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_32(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane != "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_33(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "XXin_progressXX"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_34(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "IN_PROGRESS"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_35(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane != "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_36(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "XXfor_reviewXX"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_37(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "FOR_REVIEW"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_38(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = None

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_39(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            None, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_40(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, None
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_41(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_42(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_43(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = ""
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_44(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_45(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = None

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_46(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(None)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_47(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = None
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_48(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        None,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_49(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        None,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_50(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=None,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_51(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=None,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_52(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=None,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_53(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=None,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_54(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=None,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_55(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=None,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_56(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=None,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_57(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=None,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_58(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_59(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_60(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_61(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_62(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_63(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_64(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_65(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_66(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_67(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_68(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_69(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(None)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_70(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = None

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_71(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=None,
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_72(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=None,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_73(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=None,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_74(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=None,
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_75(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=None,
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_76(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=None,
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_77(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=None,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_78(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=None,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_79(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=None,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_80(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=None,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_81(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=None,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_82(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=None,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_83(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=None,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_84(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_85(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_86(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_87(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_88(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_89(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_90(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_91(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_92(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_93(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_94(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_95(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_96(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_97(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(None),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_98(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(None),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_99(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(None, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_100(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, None)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_101(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_102(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, )

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_103(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = None
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_104(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(None)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_105(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            None,
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_106(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            None,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_107(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_108(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_109(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "XXMaterialization failed after event %s was persisted; XX"
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_110(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_111(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "MATERIALIZATION FAILED AFTER EVENT %S WAS PERSISTED; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_112(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "XXrun 'status materialize' to recoverXX",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_113(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "RUN 'STATUS MATERIALIZE' TO RECOVER",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_114(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = ""

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_115(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_116(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(None, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_117(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, None)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_118(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_119(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, )
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_120(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                None,
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_121(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                None,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_122(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_123(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_124(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "XXLegacy bridge update failed for event %s; XX"
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_125(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_126(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "LEGACY BRIDGE UPDATE FAILED FOR EVENT %S; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_127(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "XXcanonical log and snapshot are unaffectedXX",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_128(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "CANONICAL LOG AND SNAPSHOT ARE UNAFFECTED",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_129(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(None, feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_130(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, None, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_131(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, None, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_132(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, policy_metadata=None)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_133(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(feature_slug, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_134(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, repo_root, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_135(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, policy_metadata=policy_metadata)

    # Step 9: Return the event
    return event


def x_emit_status_transition__mutmut_136(
    feature_dir: Path,
    feature_slug: str,
    wp_id: str,
    to_lane: str,
    actor: str,
    *,
    force: bool = False,
    reason: str | None = None,
    evidence: dict | None = None,
    review_ref: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    execution_mode: str = "worktree",
    repo_root: Path | None = None,
    policy_metadata: dict | None = None,
) -> StatusEvent:
    """Central orchestration function for all status state changes.

    Performs the entire pipeline: validate, persist event, materialize
    snapshot, update legacy views, and emit SaaS telemetry.

    Validation failures raise TransitionError BEFORE any data is
    persisted. SaaS failures never block canonical persistence.

    Args:
        feature_dir: Path to the kitty-specs feature directory.
        feature_slug: Feature identifier (e.g. "034-feature-name").
        wp_id: Work package identifier (e.g. "WP01").
        to_lane: Target lane (canonical or alias).
        actor: Identity of the actor performing the transition.
        force: If True, bypass guard conditions (requires actor + reason).
        reason: Reason for the transition (required for force and some guards).
        evidence: Evidence dict for done transitions.
        review_ref: Review feedback reference (required for for_review -> in_progress).
        workspace_context: Active workspace context identifier.
        subtasks_complete: Whether subtasks are complete for review handoff.
        implementation_evidence_present: Whether implementation evidence is present.
        execution_mode: "worktree" or "direct_repo".
        repo_root: Repository root for SaaS fan-out (optional).
        policy_metadata: Orchestrator policy metadata dict (optional).

    Returns:
        The persisted StatusEvent.

    Raises:
        TransitionError: If the transition is invalid.
        specify_cli.status.store.StoreError: If the event log is corrupted.
    """
    # Step 1: Resolve alias
    resolved_lane = resolve_lane_alias(to_lane)

    # Step 2: Derive from_lane from last event for this WP
    from_lane = _derive_from_lane(feature_dir, wp_id)

    if workspace_context is None:
        context_root = repo_root if repo_root is not None else feature_dir
        workspace_context = f"{execution_mode}:{context_root}"
    if (
        subtasks_complete is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        subtasks_complete = _infer_subtasks_complete(feature_dir, wp_id)
    if (
        implementation_evidence_present is None
        and from_lane == "in_progress"
        and resolved_lane == "for_review"
    ):
        implementation_evidence_present = _infer_implementation_evidence(
            feature_dir, wp_id
        )

    # Step 3: Validate the transition
    # Build DoneEvidence early so we can pass it to validate_transition
    done_evidence: DoneEvidence | None = None
    if evidence is not None:
        done_evidence = _build_done_evidence(evidence)

    ok, error_msg = validate_transition(
        from_lane,
        resolved_lane,
        force=force,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
    )
    if not ok:
        raise TransitionError(error_msg)

    # Step 4: Create StatusEvent with ULID event_id
    event = StatusEvent(
        event_id=_generate_ulid(),
        feature_slug=feature_slug,
        wp_id=wp_id,
        from_lane=Lane(from_lane),
        to_lane=Lane(resolved_lane),
        at=_now_utc(),
        actor=actor,
        force=force,
        execution_mode=execution_mode,
        reason=reason,
        review_ref=review_ref,
        evidence=done_evidence,
        policy_metadata=policy_metadata,
    )

    # Step 5: Persist event to JSONL log
    _store.append_event(feature_dir, event)

    # Step 6: Materialize snapshot from event log
    try:
        snapshot = _reducer.materialize(feature_dir)
    except Exception:
        logger.warning(
            "Materialization failed after event %s was persisted; "
            "run 'status materialize' to recover",
            event.event_id,
        )
        snapshot = None

    # Step 7: Update legacy bridge views (WP06 may not be merged yet)
    if snapshot is not None:
        try:
            from specify_cli.status.legacy_bridge import update_all_views

            update_all_views(feature_dir, snapshot)
        except ImportError:
            pass  # WP06 not yet available
        except Exception:
            logger.warning(
                "Legacy bridge update failed for event %s; "
                "canonical log and snapshot are unaffected",
                event.event_id,
            )

    # Step 8: SaaS fan-out (never blocks canonical persistence)
    _saas_fan_out(event, feature_slug, repo_root, )

    # Step 9: Return the event
    return event

x_emit_status_transition__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_emit_status_transition__mutmut_1': x_emit_status_transition__mutmut_1, 
    'x_emit_status_transition__mutmut_2': x_emit_status_transition__mutmut_2, 
    'x_emit_status_transition__mutmut_3': x_emit_status_transition__mutmut_3, 
    'x_emit_status_transition__mutmut_4': x_emit_status_transition__mutmut_4, 
    'x_emit_status_transition__mutmut_5': x_emit_status_transition__mutmut_5, 
    'x_emit_status_transition__mutmut_6': x_emit_status_transition__mutmut_6, 
    'x_emit_status_transition__mutmut_7': x_emit_status_transition__mutmut_7, 
    'x_emit_status_transition__mutmut_8': x_emit_status_transition__mutmut_8, 
    'x_emit_status_transition__mutmut_9': x_emit_status_transition__mutmut_9, 
    'x_emit_status_transition__mutmut_10': x_emit_status_transition__mutmut_10, 
    'x_emit_status_transition__mutmut_11': x_emit_status_transition__mutmut_11, 
    'x_emit_status_transition__mutmut_12': x_emit_status_transition__mutmut_12, 
    'x_emit_status_transition__mutmut_13': x_emit_status_transition__mutmut_13, 
    'x_emit_status_transition__mutmut_14': x_emit_status_transition__mutmut_14, 
    'x_emit_status_transition__mutmut_15': x_emit_status_transition__mutmut_15, 
    'x_emit_status_transition__mutmut_16': x_emit_status_transition__mutmut_16, 
    'x_emit_status_transition__mutmut_17': x_emit_status_transition__mutmut_17, 
    'x_emit_status_transition__mutmut_18': x_emit_status_transition__mutmut_18, 
    'x_emit_status_transition__mutmut_19': x_emit_status_transition__mutmut_19, 
    'x_emit_status_transition__mutmut_20': x_emit_status_transition__mutmut_20, 
    'x_emit_status_transition__mutmut_21': x_emit_status_transition__mutmut_21, 
    'x_emit_status_transition__mutmut_22': x_emit_status_transition__mutmut_22, 
    'x_emit_status_transition__mutmut_23': x_emit_status_transition__mutmut_23, 
    'x_emit_status_transition__mutmut_24': x_emit_status_transition__mutmut_24, 
    'x_emit_status_transition__mutmut_25': x_emit_status_transition__mutmut_25, 
    'x_emit_status_transition__mutmut_26': x_emit_status_transition__mutmut_26, 
    'x_emit_status_transition__mutmut_27': x_emit_status_transition__mutmut_27, 
    'x_emit_status_transition__mutmut_28': x_emit_status_transition__mutmut_28, 
    'x_emit_status_transition__mutmut_29': x_emit_status_transition__mutmut_29, 
    'x_emit_status_transition__mutmut_30': x_emit_status_transition__mutmut_30, 
    'x_emit_status_transition__mutmut_31': x_emit_status_transition__mutmut_31, 
    'x_emit_status_transition__mutmut_32': x_emit_status_transition__mutmut_32, 
    'x_emit_status_transition__mutmut_33': x_emit_status_transition__mutmut_33, 
    'x_emit_status_transition__mutmut_34': x_emit_status_transition__mutmut_34, 
    'x_emit_status_transition__mutmut_35': x_emit_status_transition__mutmut_35, 
    'x_emit_status_transition__mutmut_36': x_emit_status_transition__mutmut_36, 
    'x_emit_status_transition__mutmut_37': x_emit_status_transition__mutmut_37, 
    'x_emit_status_transition__mutmut_38': x_emit_status_transition__mutmut_38, 
    'x_emit_status_transition__mutmut_39': x_emit_status_transition__mutmut_39, 
    'x_emit_status_transition__mutmut_40': x_emit_status_transition__mutmut_40, 
    'x_emit_status_transition__mutmut_41': x_emit_status_transition__mutmut_41, 
    'x_emit_status_transition__mutmut_42': x_emit_status_transition__mutmut_42, 
    'x_emit_status_transition__mutmut_43': x_emit_status_transition__mutmut_43, 
    'x_emit_status_transition__mutmut_44': x_emit_status_transition__mutmut_44, 
    'x_emit_status_transition__mutmut_45': x_emit_status_transition__mutmut_45, 
    'x_emit_status_transition__mutmut_46': x_emit_status_transition__mutmut_46, 
    'x_emit_status_transition__mutmut_47': x_emit_status_transition__mutmut_47, 
    'x_emit_status_transition__mutmut_48': x_emit_status_transition__mutmut_48, 
    'x_emit_status_transition__mutmut_49': x_emit_status_transition__mutmut_49, 
    'x_emit_status_transition__mutmut_50': x_emit_status_transition__mutmut_50, 
    'x_emit_status_transition__mutmut_51': x_emit_status_transition__mutmut_51, 
    'x_emit_status_transition__mutmut_52': x_emit_status_transition__mutmut_52, 
    'x_emit_status_transition__mutmut_53': x_emit_status_transition__mutmut_53, 
    'x_emit_status_transition__mutmut_54': x_emit_status_transition__mutmut_54, 
    'x_emit_status_transition__mutmut_55': x_emit_status_transition__mutmut_55, 
    'x_emit_status_transition__mutmut_56': x_emit_status_transition__mutmut_56, 
    'x_emit_status_transition__mutmut_57': x_emit_status_transition__mutmut_57, 
    'x_emit_status_transition__mutmut_58': x_emit_status_transition__mutmut_58, 
    'x_emit_status_transition__mutmut_59': x_emit_status_transition__mutmut_59, 
    'x_emit_status_transition__mutmut_60': x_emit_status_transition__mutmut_60, 
    'x_emit_status_transition__mutmut_61': x_emit_status_transition__mutmut_61, 
    'x_emit_status_transition__mutmut_62': x_emit_status_transition__mutmut_62, 
    'x_emit_status_transition__mutmut_63': x_emit_status_transition__mutmut_63, 
    'x_emit_status_transition__mutmut_64': x_emit_status_transition__mutmut_64, 
    'x_emit_status_transition__mutmut_65': x_emit_status_transition__mutmut_65, 
    'x_emit_status_transition__mutmut_66': x_emit_status_transition__mutmut_66, 
    'x_emit_status_transition__mutmut_67': x_emit_status_transition__mutmut_67, 
    'x_emit_status_transition__mutmut_68': x_emit_status_transition__mutmut_68, 
    'x_emit_status_transition__mutmut_69': x_emit_status_transition__mutmut_69, 
    'x_emit_status_transition__mutmut_70': x_emit_status_transition__mutmut_70, 
    'x_emit_status_transition__mutmut_71': x_emit_status_transition__mutmut_71, 
    'x_emit_status_transition__mutmut_72': x_emit_status_transition__mutmut_72, 
    'x_emit_status_transition__mutmut_73': x_emit_status_transition__mutmut_73, 
    'x_emit_status_transition__mutmut_74': x_emit_status_transition__mutmut_74, 
    'x_emit_status_transition__mutmut_75': x_emit_status_transition__mutmut_75, 
    'x_emit_status_transition__mutmut_76': x_emit_status_transition__mutmut_76, 
    'x_emit_status_transition__mutmut_77': x_emit_status_transition__mutmut_77, 
    'x_emit_status_transition__mutmut_78': x_emit_status_transition__mutmut_78, 
    'x_emit_status_transition__mutmut_79': x_emit_status_transition__mutmut_79, 
    'x_emit_status_transition__mutmut_80': x_emit_status_transition__mutmut_80, 
    'x_emit_status_transition__mutmut_81': x_emit_status_transition__mutmut_81, 
    'x_emit_status_transition__mutmut_82': x_emit_status_transition__mutmut_82, 
    'x_emit_status_transition__mutmut_83': x_emit_status_transition__mutmut_83, 
    'x_emit_status_transition__mutmut_84': x_emit_status_transition__mutmut_84, 
    'x_emit_status_transition__mutmut_85': x_emit_status_transition__mutmut_85, 
    'x_emit_status_transition__mutmut_86': x_emit_status_transition__mutmut_86, 
    'x_emit_status_transition__mutmut_87': x_emit_status_transition__mutmut_87, 
    'x_emit_status_transition__mutmut_88': x_emit_status_transition__mutmut_88, 
    'x_emit_status_transition__mutmut_89': x_emit_status_transition__mutmut_89, 
    'x_emit_status_transition__mutmut_90': x_emit_status_transition__mutmut_90, 
    'x_emit_status_transition__mutmut_91': x_emit_status_transition__mutmut_91, 
    'x_emit_status_transition__mutmut_92': x_emit_status_transition__mutmut_92, 
    'x_emit_status_transition__mutmut_93': x_emit_status_transition__mutmut_93, 
    'x_emit_status_transition__mutmut_94': x_emit_status_transition__mutmut_94, 
    'x_emit_status_transition__mutmut_95': x_emit_status_transition__mutmut_95, 
    'x_emit_status_transition__mutmut_96': x_emit_status_transition__mutmut_96, 
    'x_emit_status_transition__mutmut_97': x_emit_status_transition__mutmut_97, 
    'x_emit_status_transition__mutmut_98': x_emit_status_transition__mutmut_98, 
    'x_emit_status_transition__mutmut_99': x_emit_status_transition__mutmut_99, 
    'x_emit_status_transition__mutmut_100': x_emit_status_transition__mutmut_100, 
    'x_emit_status_transition__mutmut_101': x_emit_status_transition__mutmut_101, 
    'x_emit_status_transition__mutmut_102': x_emit_status_transition__mutmut_102, 
    'x_emit_status_transition__mutmut_103': x_emit_status_transition__mutmut_103, 
    'x_emit_status_transition__mutmut_104': x_emit_status_transition__mutmut_104, 
    'x_emit_status_transition__mutmut_105': x_emit_status_transition__mutmut_105, 
    'x_emit_status_transition__mutmut_106': x_emit_status_transition__mutmut_106, 
    'x_emit_status_transition__mutmut_107': x_emit_status_transition__mutmut_107, 
    'x_emit_status_transition__mutmut_108': x_emit_status_transition__mutmut_108, 
    'x_emit_status_transition__mutmut_109': x_emit_status_transition__mutmut_109, 
    'x_emit_status_transition__mutmut_110': x_emit_status_transition__mutmut_110, 
    'x_emit_status_transition__mutmut_111': x_emit_status_transition__mutmut_111, 
    'x_emit_status_transition__mutmut_112': x_emit_status_transition__mutmut_112, 
    'x_emit_status_transition__mutmut_113': x_emit_status_transition__mutmut_113, 
    'x_emit_status_transition__mutmut_114': x_emit_status_transition__mutmut_114, 
    'x_emit_status_transition__mutmut_115': x_emit_status_transition__mutmut_115, 
    'x_emit_status_transition__mutmut_116': x_emit_status_transition__mutmut_116, 
    'x_emit_status_transition__mutmut_117': x_emit_status_transition__mutmut_117, 
    'x_emit_status_transition__mutmut_118': x_emit_status_transition__mutmut_118, 
    'x_emit_status_transition__mutmut_119': x_emit_status_transition__mutmut_119, 
    'x_emit_status_transition__mutmut_120': x_emit_status_transition__mutmut_120, 
    'x_emit_status_transition__mutmut_121': x_emit_status_transition__mutmut_121, 
    'x_emit_status_transition__mutmut_122': x_emit_status_transition__mutmut_122, 
    'x_emit_status_transition__mutmut_123': x_emit_status_transition__mutmut_123, 
    'x_emit_status_transition__mutmut_124': x_emit_status_transition__mutmut_124, 
    'x_emit_status_transition__mutmut_125': x_emit_status_transition__mutmut_125, 
    'x_emit_status_transition__mutmut_126': x_emit_status_transition__mutmut_126, 
    'x_emit_status_transition__mutmut_127': x_emit_status_transition__mutmut_127, 
    'x_emit_status_transition__mutmut_128': x_emit_status_transition__mutmut_128, 
    'x_emit_status_transition__mutmut_129': x_emit_status_transition__mutmut_129, 
    'x_emit_status_transition__mutmut_130': x_emit_status_transition__mutmut_130, 
    'x_emit_status_transition__mutmut_131': x_emit_status_transition__mutmut_131, 
    'x_emit_status_transition__mutmut_132': x_emit_status_transition__mutmut_132, 
    'x_emit_status_transition__mutmut_133': x_emit_status_transition__mutmut_133, 
    'x_emit_status_transition__mutmut_134': x_emit_status_transition__mutmut_134, 
    'x_emit_status_transition__mutmut_135': x_emit_status_transition__mutmut_135, 
    'x_emit_status_transition__mutmut_136': x_emit_status_transition__mutmut_136
}
x_emit_status_transition__mutmut_orig.__name__ = 'x_emit_status_transition'


def _saas_fan_out(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    args = [event, feature_slug, repo_root]# type: ignore
    kwargs = {'policy_metadata': policy_metadata}# type: ignore
    return _mutmut_trampoline(x__saas_fan_out__mutmut_orig, x__saas_fan_out__mutmut_mutants, args, kwargs, None)


def x__saas_fan_out__mutmut_orig(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_1(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=None,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_2(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=None,
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_3(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=None,
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_4(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=None,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_5(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=None,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_6(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=None,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_7(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_8(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_9(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_10(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_11(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_12(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_13(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(None),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_14(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(None),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_15(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            None,
            event.event_id,
        )


def x__saas_fan_out__mutmut_16(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            None,
        )


def x__saas_fan_out__mutmut_17(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            event.event_id,
        )


def x__saas_fan_out__mutmut_18(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SaaS fan-out failed for event %s; canonical log unaffected",
            )


def x__saas_fan_out__mutmut_19(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "XXSaaS fan-out failed for event %s; canonical log unaffectedXX",
            event.event_id,
        )


def x__saas_fan_out__mutmut_20(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "saas fan-out failed for event %s; canonical log unaffected",
            event.event_id,
        )


def x__saas_fan_out__mutmut_21(
    event: StatusEvent,
    feature_slug: str,
    repo_root: Path | None,
    *,
    policy_metadata: dict | None = None,
) -> None:
    """Conditionally emit a SaaS telemetry event via the sync pipeline.

    Uses try/except ImportError to handle the 0.1x branch where
    the sync module does not exist. A broad Exception catch ensures
    SaaS failures NEVER block canonical persistence.
    """
    try:
        from specify_cli.sync.events import emit_wp_status_changed

        emit_wp_status_changed(
            wp_id=event.wp_id,
            from_lane=str(event.from_lane),
            to_lane=str(event.to_lane),
            actor=event.actor,
            feature_slug=feature_slug,
            policy_metadata=policy_metadata,
        )
    except ImportError:
        pass  # SaaS sync not available (0.1x branch)
    except Exception:
        logger.warning(
            "SAAS FAN-OUT FAILED FOR EVENT %S; CANONICAL LOG UNAFFECTED",
            event.event_id,
        )

x__saas_fan_out__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__saas_fan_out__mutmut_1': x__saas_fan_out__mutmut_1, 
    'x__saas_fan_out__mutmut_2': x__saas_fan_out__mutmut_2, 
    'x__saas_fan_out__mutmut_3': x__saas_fan_out__mutmut_3, 
    'x__saas_fan_out__mutmut_4': x__saas_fan_out__mutmut_4, 
    'x__saas_fan_out__mutmut_5': x__saas_fan_out__mutmut_5, 
    'x__saas_fan_out__mutmut_6': x__saas_fan_out__mutmut_6, 
    'x__saas_fan_out__mutmut_7': x__saas_fan_out__mutmut_7, 
    'x__saas_fan_out__mutmut_8': x__saas_fan_out__mutmut_8, 
    'x__saas_fan_out__mutmut_9': x__saas_fan_out__mutmut_9, 
    'x__saas_fan_out__mutmut_10': x__saas_fan_out__mutmut_10, 
    'x__saas_fan_out__mutmut_11': x__saas_fan_out__mutmut_11, 
    'x__saas_fan_out__mutmut_12': x__saas_fan_out__mutmut_12, 
    'x__saas_fan_out__mutmut_13': x__saas_fan_out__mutmut_13, 
    'x__saas_fan_out__mutmut_14': x__saas_fan_out__mutmut_14, 
    'x__saas_fan_out__mutmut_15': x__saas_fan_out__mutmut_15, 
    'x__saas_fan_out__mutmut_16': x__saas_fan_out__mutmut_16, 
    'x__saas_fan_out__mutmut_17': x__saas_fan_out__mutmut_17, 
    'x__saas_fan_out__mutmut_18': x__saas_fan_out__mutmut_18, 
    'x__saas_fan_out__mutmut_19': x__saas_fan_out__mutmut_19, 
    'x__saas_fan_out__mutmut_20': x__saas_fan_out__mutmut_20, 
    'x__saas_fan_out__mutmut_21': x__saas_fan_out__mutmut_21
}
x__saas_fan_out__mutmut_orig.__name__ = 'x__saas_fan_out'
