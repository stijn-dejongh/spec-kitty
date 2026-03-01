"""Checkpoint/resume mechanism for cross-session conflict resolution (WP07).

This module implements event-sourced checkpoint/resume that enables:
1. Persisting minimal state before the generation gate blocks
2. Verifying input hash on resume to detect context changes
3. Restoring execution from the checkpoint cursor

Architecture:
- StepCheckpoint: Frozen dataclass with mission/run/step IDs, strictness,
  scope refs, input hash, cursor, retry token
- compute_input_hash(): Deterministic SHA256 of sorted JSON inputs
- verify_input_hash(): Compare checkpoint vs current context
- handle_context_change(): Prompt user if hash differs
- load_checkpoint(): Retrieve latest checkpoint from event log
- parse_checkpoint_event(): Reconstruct StepCheckpoint from event payload
"""

from __future__ import annotations

import hashlib
import json
import logging
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from specify_cli.glossary.scope import GlossaryScope
from specify_cli.glossary.strictness import Strictness

logger = logging.getLogger(__name__)

# Valid cursor values representing execution stages
VALID_CURSORS = frozenset({"pre_generation_gate", "post_clarification", "post_gate"})
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
class ScopeRef:
    """Reference to a specific glossary scope version."""

    scope: GlossaryScope
    version_id: str  # e.g., "v3", "2026-02-16-001"


@dataclass(frozen=True)
class StepCheckpoint:
    """Minimal state for resuming step execution after conflict resolution.

    All fields are immutable (frozen dataclass). The input_hash is a SHA256
    digest that allows detecting if the execution context has changed since
    the checkpoint was created. The retry_token is a UUID for idempotency.
    """

    mission_id: str
    run_id: str
    step_id: str
    strictness: Strictness
    scope_refs: tuple[ScopeRef, ...]  # tuple for immutability
    input_hash: str  # SHA256 hex digest (64 chars)
    cursor: str  # Execution stage (e.g., "pre_generation_gate")
    retry_token: str  # UUID v4 string (36 chars)
    timestamp: datetime

    def __post_init__(self) -> None:
        """Validate checkpoint fields."""
        # Validate hash format (64 hex chars for SHA256)
        if len(self.input_hash) != 64 or not all(
            c in "0123456789abcdef" for c in self.input_hash
        ):
            raise ValueError(f"Invalid input_hash format: {self.input_hash}")

        # Validate retry token is UUID format (36 chars with hyphens)
        if len(self.retry_token) != 36:
            raise ValueError(f"Invalid retry_token format: {self.retry_token}")

        # Validate cursor is known stage
        if self.cursor not in VALID_CURSORS:
            raise ValueError(f"Unknown cursor value: {self.cursor}")


def compute_input_hash(inputs: dict[str, Any]) -> str:
    args = [inputs]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_compute_input_hash__mutmut_orig, x_compute_input_hash__mutmut_mutants, args, kwargs, None)


def x_compute_input_hash__mutmut_orig(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = json.dumps(inputs, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def x_compute_input_hash__mutmut_1(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = None
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def x_compute_input_hash__mutmut_2(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = json.dumps(None, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def x_compute_input_hash__mutmut_3(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = json.dumps(inputs, sort_keys=None, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def x_compute_input_hash__mutmut_4(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = json.dumps(inputs, sort_keys=True, ensure_ascii=None)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def x_compute_input_hash__mutmut_5(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = json.dumps(sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def x_compute_input_hash__mutmut_6(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = json.dumps(inputs, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def x_compute_input_hash__mutmut_7(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = json.dumps(inputs, sort_keys=True, )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def x_compute_input_hash__mutmut_8(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = json.dumps(inputs, sort_keys=False, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def x_compute_input_hash__mutmut_9(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = json.dumps(inputs, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def x_compute_input_hash__mutmut_10(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = json.dumps(inputs, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(None).hexdigest()


def x_compute_input_hash__mutmut_11(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = json.dumps(inputs, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode(None)).hexdigest()


def x_compute_input_hash__mutmut_12(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = json.dumps(inputs, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("XXutf-8XX")).hexdigest()


def x_compute_input_hash__mutmut_13(inputs: dict[str, Any]) -> str:
    """Compute deterministic SHA256 hash of step inputs.

    Uses json.dumps with sort_keys=True for deterministic serialization.
    The same inputs always produce the same hash regardless of insertion order.

    Args:
        inputs: Step input dictionary (any JSON-serializable structure)

    Returns:
        64-character lowercase hex string (SHA256 hash)
    """
    canonical = json.dumps(inputs, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("UTF-8")).hexdigest()

x_compute_input_hash__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_compute_input_hash__mutmut_1': x_compute_input_hash__mutmut_1, 
    'x_compute_input_hash__mutmut_2': x_compute_input_hash__mutmut_2, 
    'x_compute_input_hash__mutmut_3': x_compute_input_hash__mutmut_3, 
    'x_compute_input_hash__mutmut_4': x_compute_input_hash__mutmut_4, 
    'x_compute_input_hash__mutmut_5': x_compute_input_hash__mutmut_5, 
    'x_compute_input_hash__mutmut_6': x_compute_input_hash__mutmut_6, 
    'x_compute_input_hash__mutmut_7': x_compute_input_hash__mutmut_7, 
    'x_compute_input_hash__mutmut_8': x_compute_input_hash__mutmut_8, 
    'x_compute_input_hash__mutmut_9': x_compute_input_hash__mutmut_9, 
    'x_compute_input_hash__mutmut_10': x_compute_input_hash__mutmut_10, 
    'x_compute_input_hash__mutmut_11': x_compute_input_hash__mutmut_11, 
    'x_compute_input_hash__mutmut_12': x_compute_input_hash__mutmut_12, 
    'x_compute_input_hash__mutmut_13': x_compute_input_hash__mutmut_13
}
x_compute_input_hash__mutmut_orig.__name__ = 'x_compute_input_hash'


def create_checkpoint(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    args = [mission_id, run_id, step_id, strictness, scope_refs, inputs, cursor]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_create_checkpoint__mutmut_orig, x_create_checkpoint__mutmut_mutants, args, kwargs, None)


def x_create_checkpoint__mutmut_orig(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_1(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=None,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_2(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=None,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_3(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=None,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_4(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=None,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_5(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=None,
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_6(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=None,
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_7(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=None,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_8(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=None,
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_9(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=None,
    )


def x_create_checkpoint__mutmut_10(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_11(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_12(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_13(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_14(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_15(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_16(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_17(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_18(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        )


def x_create_checkpoint__mutmut_19(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(None),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_20(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(None),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_21(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(None),
        timestamp=datetime.now(timezone.utc),
    )


def x_create_checkpoint__mutmut_22(
    mission_id: str,
    run_id: str,
    step_id: str,
    strictness: Strictness,
    scope_refs: list[ScopeRef],
    inputs: dict[str, Any],
    cursor: str,
) -> StepCheckpoint:
    """Create a new checkpoint with computed input hash and fresh retry token.

    Args:
        mission_id: Mission identifier
        run_id: Run instance identifier
        step_id: Step identifier
        strictness: Resolved strictness mode
        scope_refs: Active glossary scope versions
        inputs: Step input dictionary (hashed for context verification)
        cursor: Execution stage (e.g., "pre_generation_gate")

    Returns:
        StepCheckpoint instance ready for event emission
    """
    return StepCheckpoint(
        mission_id=mission_id,
        run_id=run_id,
        step_id=step_id,
        strictness=strictness,
        scope_refs=tuple(scope_refs),
        input_hash=compute_input_hash(inputs),
        cursor=cursor,
        retry_token=str(uuid.uuid4()),
        timestamp=datetime.now(None),
    )

x_create_checkpoint__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_create_checkpoint__mutmut_1': x_create_checkpoint__mutmut_1, 
    'x_create_checkpoint__mutmut_2': x_create_checkpoint__mutmut_2, 
    'x_create_checkpoint__mutmut_3': x_create_checkpoint__mutmut_3, 
    'x_create_checkpoint__mutmut_4': x_create_checkpoint__mutmut_4, 
    'x_create_checkpoint__mutmut_5': x_create_checkpoint__mutmut_5, 
    'x_create_checkpoint__mutmut_6': x_create_checkpoint__mutmut_6, 
    'x_create_checkpoint__mutmut_7': x_create_checkpoint__mutmut_7, 
    'x_create_checkpoint__mutmut_8': x_create_checkpoint__mutmut_8, 
    'x_create_checkpoint__mutmut_9': x_create_checkpoint__mutmut_9, 
    'x_create_checkpoint__mutmut_10': x_create_checkpoint__mutmut_10, 
    'x_create_checkpoint__mutmut_11': x_create_checkpoint__mutmut_11, 
    'x_create_checkpoint__mutmut_12': x_create_checkpoint__mutmut_12, 
    'x_create_checkpoint__mutmut_13': x_create_checkpoint__mutmut_13, 
    'x_create_checkpoint__mutmut_14': x_create_checkpoint__mutmut_14, 
    'x_create_checkpoint__mutmut_15': x_create_checkpoint__mutmut_15, 
    'x_create_checkpoint__mutmut_16': x_create_checkpoint__mutmut_16, 
    'x_create_checkpoint__mutmut_17': x_create_checkpoint__mutmut_17, 
    'x_create_checkpoint__mutmut_18': x_create_checkpoint__mutmut_18, 
    'x_create_checkpoint__mutmut_19': x_create_checkpoint__mutmut_19, 
    'x_create_checkpoint__mutmut_20': x_create_checkpoint__mutmut_20, 
    'x_create_checkpoint__mutmut_21': x_create_checkpoint__mutmut_21, 
    'x_create_checkpoint__mutmut_22': x_create_checkpoint__mutmut_22
}
x_create_checkpoint__mutmut_orig.__name__ = 'x_create_checkpoint'


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def load_checkpoint(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    args = [project_root, step_id, mission_id, retry_token]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_load_checkpoint__mutmut_orig, x_load_checkpoint__mutmut_mutants, args, kwargs, None)


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_orig(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_1(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = None
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_2(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" * "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_3(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" * "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_4(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root * ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_5(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / "XX.kittifyXX" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_6(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".KITTIFY" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_7(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "XXeventsXX" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_8(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "EVENTS" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_9(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "XXglossaryXX"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_10(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "GLOSSARY"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_11(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_12(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info(None, step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_13(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", None)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_14(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info(step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_15(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", )
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_16(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("XXNo glossary events directory for step=%sXX", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_17(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("no glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_18(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("NO GLOSSARY EVENTS DIRECTORY FOR STEP=%S", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_19(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = ""

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_20(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob(None):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_21(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("XX*.events.jsonlXX"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_22(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.EVENTS.JSONL"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_23(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(None, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_24(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type=None):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_25(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_26(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, ):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_27(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="XXStepCheckpointedXX"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_28(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="stepcheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_29(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="STEPCHECKPOINTED"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_30(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get(None) != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_31(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("XXstep_idXX") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_32(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("STEP_ID") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_33(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") == step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_34(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                break
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_35(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None or event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_36(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_37(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get(None) != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_38(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("XXmission_idXX") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_39(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("MISSION_ID") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_40(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") == mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_41(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                break
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_42(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None or event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_43(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_44(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get(None) != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_45(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("XXretry_tokenXX") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_46(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("RETRY_TOKEN") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_47(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") == retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_48(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                break

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_49(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = None
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_50(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(None)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_51(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    None, event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_52(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", None, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_53(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, None
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_54(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_55(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_56(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_57(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "XXInvalid checkpoint event in %s: %sXX", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_58(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_59(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "INVALID CHECKPOINT EVENT IN %S: %S", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_60(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                break

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_61(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None and checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_62(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is not None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_63(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp >= latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_64(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = None

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_65(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_66(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            None,
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_67(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            None,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_68(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            None,
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_69(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            None,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_70(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_71(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_72(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_73(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_74(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "XXLoaded checkpoint for step=%s mission=%s cursor=%sXX",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_75(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_76(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "LOADED CHECKPOINT FOR STEP=%S MISSION=%S CURSOR=%S",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_77(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id and "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_78(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "XX*XX",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_79(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            None,
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_80(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            None,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_81(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            None,
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_82(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            None,
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_83(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_84(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_85(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_86(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_87(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "XXNo checkpoint found for step=%s mission=%s retry_token=%sXX",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_88(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "no checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_89(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "NO CHECKPOINT FOUND FOR STEP=%S MISSION=%S RETRY_TOKEN=%S",
            step_id,
            mission_id or "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_90(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id and "*",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_91(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "XX*XX",
            "set" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_92(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "XXsetXX" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_93(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "SET" if retry_token else "unset",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_94(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "XXunsetXX",
        )

    return latest


# ---------------------------------------------------------------------------
# T032: Checkpoint loading from event log
# ---------------------------------------------------------------------------


def x_load_checkpoint__mutmut_95(
    project_root: Path,
    step_id: str,
    mission_id: str | None = None,
    retry_token: str | None = None,
) -> Optional[StepCheckpoint]:
    """Load latest checkpoint for step_id from event log.

    Reads StepCheckpointed events from event log and returns the most recent
    checkpoint for the given step_id. Scans all mission event logs in the
    glossary events directory.

    Args:
        project_root: Repository root (contains .kittify/events/)
        step_id: Step identifier to load checkpoint for
        mission_id: Optional mission identifier filter (recommended)
        retry_token: Optional retry token filter (exact-match resume)

    Returns:
        Latest StepCheckpoint for step_id, or None if not found
    """
    from .events import read_events

    events_dir = project_root / ".kittify" / "events" / "glossary"
    if not events_dir.exists():
        logger.info("No glossary events directory for step=%s", step_id)
        return None

    latest: Optional[StepCheckpoint] = None

    # Scan all mission event logs in the glossary events directory
    for event_log_path in events_dir.glob("*.events.jsonl"):
        for event_payload in read_events(event_log_path, event_type="StepCheckpointed"):
            if event_payload.get("step_id") != step_id:
                continue
            if mission_id is not None and event_payload.get("mission_id") != mission_id:
                continue
            if retry_token is not None and event_payload.get("retry_token") != retry_token:
                continue

            try:
                checkpoint = parse_checkpoint_event(event_payload)
            except ValueError as exc:
                logger.warning(
                    "Invalid checkpoint event in %s: %s", event_log_path.name, exc
                )
                continue

            if latest is None or checkpoint.timestamp > latest.timestamp:
                latest = checkpoint

    if latest is not None:
        logger.info(
            "Loaded checkpoint for step=%s mission=%s cursor=%s",
            step_id,
            mission_id or "*",
            latest.cursor,
        )
    else:
        logger.info(
            "No checkpoint found for step=%s mission=%s retry_token=%s",
            step_id,
            mission_id or "*",
            "set" if retry_token else "UNSET",
        )

    return latest

x_load_checkpoint__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_load_checkpoint__mutmut_1': x_load_checkpoint__mutmut_1, 
    'x_load_checkpoint__mutmut_2': x_load_checkpoint__mutmut_2, 
    'x_load_checkpoint__mutmut_3': x_load_checkpoint__mutmut_3, 
    'x_load_checkpoint__mutmut_4': x_load_checkpoint__mutmut_4, 
    'x_load_checkpoint__mutmut_5': x_load_checkpoint__mutmut_5, 
    'x_load_checkpoint__mutmut_6': x_load_checkpoint__mutmut_6, 
    'x_load_checkpoint__mutmut_7': x_load_checkpoint__mutmut_7, 
    'x_load_checkpoint__mutmut_8': x_load_checkpoint__mutmut_8, 
    'x_load_checkpoint__mutmut_9': x_load_checkpoint__mutmut_9, 
    'x_load_checkpoint__mutmut_10': x_load_checkpoint__mutmut_10, 
    'x_load_checkpoint__mutmut_11': x_load_checkpoint__mutmut_11, 
    'x_load_checkpoint__mutmut_12': x_load_checkpoint__mutmut_12, 
    'x_load_checkpoint__mutmut_13': x_load_checkpoint__mutmut_13, 
    'x_load_checkpoint__mutmut_14': x_load_checkpoint__mutmut_14, 
    'x_load_checkpoint__mutmut_15': x_load_checkpoint__mutmut_15, 
    'x_load_checkpoint__mutmut_16': x_load_checkpoint__mutmut_16, 
    'x_load_checkpoint__mutmut_17': x_load_checkpoint__mutmut_17, 
    'x_load_checkpoint__mutmut_18': x_load_checkpoint__mutmut_18, 
    'x_load_checkpoint__mutmut_19': x_load_checkpoint__mutmut_19, 
    'x_load_checkpoint__mutmut_20': x_load_checkpoint__mutmut_20, 
    'x_load_checkpoint__mutmut_21': x_load_checkpoint__mutmut_21, 
    'x_load_checkpoint__mutmut_22': x_load_checkpoint__mutmut_22, 
    'x_load_checkpoint__mutmut_23': x_load_checkpoint__mutmut_23, 
    'x_load_checkpoint__mutmut_24': x_load_checkpoint__mutmut_24, 
    'x_load_checkpoint__mutmut_25': x_load_checkpoint__mutmut_25, 
    'x_load_checkpoint__mutmut_26': x_load_checkpoint__mutmut_26, 
    'x_load_checkpoint__mutmut_27': x_load_checkpoint__mutmut_27, 
    'x_load_checkpoint__mutmut_28': x_load_checkpoint__mutmut_28, 
    'x_load_checkpoint__mutmut_29': x_load_checkpoint__mutmut_29, 
    'x_load_checkpoint__mutmut_30': x_load_checkpoint__mutmut_30, 
    'x_load_checkpoint__mutmut_31': x_load_checkpoint__mutmut_31, 
    'x_load_checkpoint__mutmut_32': x_load_checkpoint__mutmut_32, 
    'x_load_checkpoint__mutmut_33': x_load_checkpoint__mutmut_33, 
    'x_load_checkpoint__mutmut_34': x_load_checkpoint__mutmut_34, 
    'x_load_checkpoint__mutmut_35': x_load_checkpoint__mutmut_35, 
    'x_load_checkpoint__mutmut_36': x_load_checkpoint__mutmut_36, 
    'x_load_checkpoint__mutmut_37': x_load_checkpoint__mutmut_37, 
    'x_load_checkpoint__mutmut_38': x_load_checkpoint__mutmut_38, 
    'x_load_checkpoint__mutmut_39': x_load_checkpoint__mutmut_39, 
    'x_load_checkpoint__mutmut_40': x_load_checkpoint__mutmut_40, 
    'x_load_checkpoint__mutmut_41': x_load_checkpoint__mutmut_41, 
    'x_load_checkpoint__mutmut_42': x_load_checkpoint__mutmut_42, 
    'x_load_checkpoint__mutmut_43': x_load_checkpoint__mutmut_43, 
    'x_load_checkpoint__mutmut_44': x_load_checkpoint__mutmut_44, 
    'x_load_checkpoint__mutmut_45': x_load_checkpoint__mutmut_45, 
    'x_load_checkpoint__mutmut_46': x_load_checkpoint__mutmut_46, 
    'x_load_checkpoint__mutmut_47': x_load_checkpoint__mutmut_47, 
    'x_load_checkpoint__mutmut_48': x_load_checkpoint__mutmut_48, 
    'x_load_checkpoint__mutmut_49': x_load_checkpoint__mutmut_49, 
    'x_load_checkpoint__mutmut_50': x_load_checkpoint__mutmut_50, 
    'x_load_checkpoint__mutmut_51': x_load_checkpoint__mutmut_51, 
    'x_load_checkpoint__mutmut_52': x_load_checkpoint__mutmut_52, 
    'x_load_checkpoint__mutmut_53': x_load_checkpoint__mutmut_53, 
    'x_load_checkpoint__mutmut_54': x_load_checkpoint__mutmut_54, 
    'x_load_checkpoint__mutmut_55': x_load_checkpoint__mutmut_55, 
    'x_load_checkpoint__mutmut_56': x_load_checkpoint__mutmut_56, 
    'x_load_checkpoint__mutmut_57': x_load_checkpoint__mutmut_57, 
    'x_load_checkpoint__mutmut_58': x_load_checkpoint__mutmut_58, 
    'x_load_checkpoint__mutmut_59': x_load_checkpoint__mutmut_59, 
    'x_load_checkpoint__mutmut_60': x_load_checkpoint__mutmut_60, 
    'x_load_checkpoint__mutmut_61': x_load_checkpoint__mutmut_61, 
    'x_load_checkpoint__mutmut_62': x_load_checkpoint__mutmut_62, 
    'x_load_checkpoint__mutmut_63': x_load_checkpoint__mutmut_63, 
    'x_load_checkpoint__mutmut_64': x_load_checkpoint__mutmut_64, 
    'x_load_checkpoint__mutmut_65': x_load_checkpoint__mutmut_65, 
    'x_load_checkpoint__mutmut_66': x_load_checkpoint__mutmut_66, 
    'x_load_checkpoint__mutmut_67': x_load_checkpoint__mutmut_67, 
    'x_load_checkpoint__mutmut_68': x_load_checkpoint__mutmut_68, 
    'x_load_checkpoint__mutmut_69': x_load_checkpoint__mutmut_69, 
    'x_load_checkpoint__mutmut_70': x_load_checkpoint__mutmut_70, 
    'x_load_checkpoint__mutmut_71': x_load_checkpoint__mutmut_71, 
    'x_load_checkpoint__mutmut_72': x_load_checkpoint__mutmut_72, 
    'x_load_checkpoint__mutmut_73': x_load_checkpoint__mutmut_73, 
    'x_load_checkpoint__mutmut_74': x_load_checkpoint__mutmut_74, 
    'x_load_checkpoint__mutmut_75': x_load_checkpoint__mutmut_75, 
    'x_load_checkpoint__mutmut_76': x_load_checkpoint__mutmut_76, 
    'x_load_checkpoint__mutmut_77': x_load_checkpoint__mutmut_77, 
    'x_load_checkpoint__mutmut_78': x_load_checkpoint__mutmut_78, 
    'x_load_checkpoint__mutmut_79': x_load_checkpoint__mutmut_79, 
    'x_load_checkpoint__mutmut_80': x_load_checkpoint__mutmut_80, 
    'x_load_checkpoint__mutmut_81': x_load_checkpoint__mutmut_81, 
    'x_load_checkpoint__mutmut_82': x_load_checkpoint__mutmut_82, 
    'x_load_checkpoint__mutmut_83': x_load_checkpoint__mutmut_83, 
    'x_load_checkpoint__mutmut_84': x_load_checkpoint__mutmut_84, 
    'x_load_checkpoint__mutmut_85': x_load_checkpoint__mutmut_85, 
    'x_load_checkpoint__mutmut_86': x_load_checkpoint__mutmut_86, 
    'x_load_checkpoint__mutmut_87': x_load_checkpoint__mutmut_87, 
    'x_load_checkpoint__mutmut_88': x_load_checkpoint__mutmut_88, 
    'x_load_checkpoint__mutmut_89': x_load_checkpoint__mutmut_89, 
    'x_load_checkpoint__mutmut_90': x_load_checkpoint__mutmut_90, 
    'x_load_checkpoint__mutmut_91': x_load_checkpoint__mutmut_91, 
    'x_load_checkpoint__mutmut_92': x_load_checkpoint__mutmut_92, 
    'x_load_checkpoint__mutmut_93': x_load_checkpoint__mutmut_93, 
    'x_load_checkpoint__mutmut_94': x_load_checkpoint__mutmut_94, 
    'x_load_checkpoint__mutmut_95': x_load_checkpoint__mutmut_95
}
x_load_checkpoint__mutmut_orig.__name__ = 'x_load_checkpoint'


def parse_checkpoint_event(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    args = [event_payload]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_parse_checkpoint_event__mutmut_orig, x_parse_checkpoint_event__mutmut_mutants, args, kwargs, None)


def x_parse_checkpoint_event__mutmut_orig(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_1(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=None,
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_2(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=None,
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_3(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=None,
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_4(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=None,
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_5(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=None,
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_6(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=None,
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_7(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=None,
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_8(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=None,
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_9(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=None,
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_10(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_11(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_12(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_13(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_14(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_15(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_16(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_17(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_18(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_19(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["XXmission_idXX"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_20(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["MISSION_ID"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_21(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["XXrun_idXX"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_22(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["RUN_ID"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_23(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["XXstep_idXX"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_24(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["STEP_ID"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_25(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(None),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_26(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["XXstrictnessXX"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_27(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["STRICTNESS"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_28(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                None
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_29(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=None,
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_30(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=None,
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_31(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_32(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_33(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(None),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_34(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["XXscopeXX"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_35(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["SCOPE"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_36(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["XXversion_idXX"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_37(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["VERSION_ID"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_38(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get(None, [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_39(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", None)
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_40(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get([])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_41(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", )
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_42(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("XXscope_refsXX", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_43(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("SCOPE_REFS", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_44(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["XXinput_hashXX"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_45(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["INPUT_HASH"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_46(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["XXcursorXX"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_47(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["CURSOR"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_48(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["XXretry_tokenXX"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_49(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["RETRY_TOKEN"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_50(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(None),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_51(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["XXtimestampXX"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_52(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["TIMESTAMP"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid checkpoint event payload: {e}") from e


def x_parse_checkpoint_event__mutmut_53(
    event_payload: dict[str, Any],
) -> StepCheckpoint:
    """Parse StepCheckpointed event payload into StepCheckpoint instance.

    Args:
        event_payload: Event dictionary from event log

    Returns:
        Parsed StepCheckpoint instance

    Raises:
        ValueError: If payload is missing required fields or has invalid format
    """
    try:
        return StepCheckpoint(
            mission_id=event_payload["mission_id"],
            run_id=event_payload["run_id"],
            step_id=event_payload["step_id"],
            strictness=Strictness(event_payload["strictness"]),
            scope_refs=tuple(
                ScopeRef(
                    scope=GlossaryScope(ref["scope"]),
                    version_id=ref["version_id"],
                )
                for ref in event_payload.get("scope_refs", [])
            ),
            input_hash=event_payload["input_hash"],
            cursor=event_payload["cursor"],
            retry_token=event_payload["retry_token"],
            timestamp=datetime.fromisoformat(event_payload["timestamp"]),
        )
    except (KeyError, ValueError) as e:
        raise ValueError(None) from e

x_parse_checkpoint_event__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_parse_checkpoint_event__mutmut_1': x_parse_checkpoint_event__mutmut_1, 
    'x_parse_checkpoint_event__mutmut_2': x_parse_checkpoint_event__mutmut_2, 
    'x_parse_checkpoint_event__mutmut_3': x_parse_checkpoint_event__mutmut_3, 
    'x_parse_checkpoint_event__mutmut_4': x_parse_checkpoint_event__mutmut_4, 
    'x_parse_checkpoint_event__mutmut_5': x_parse_checkpoint_event__mutmut_5, 
    'x_parse_checkpoint_event__mutmut_6': x_parse_checkpoint_event__mutmut_6, 
    'x_parse_checkpoint_event__mutmut_7': x_parse_checkpoint_event__mutmut_7, 
    'x_parse_checkpoint_event__mutmut_8': x_parse_checkpoint_event__mutmut_8, 
    'x_parse_checkpoint_event__mutmut_9': x_parse_checkpoint_event__mutmut_9, 
    'x_parse_checkpoint_event__mutmut_10': x_parse_checkpoint_event__mutmut_10, 
    'x_parse_checkpoint_event__mutmut_11': x_parse_checkpoint_event__mutmut_11, 
    'x_parse_checkpoint_event__mutmut_12': x_parse_checkpoint_event__mutmut_12, 
    'x_parse_checkpoint_event__mutmut_13': x_parse_checkpoint_event__mutmut_13, 
    'x_parse_checkpoint_event__mutmut_14': x_parse_checkpoint_event__mutmut_14, 
    'x_parse_checkpoint_event__mutmut_15': x_parse_checkpoint_event__mutmut_15, 
    'x_parse_checkpoint_event__mutmut_16': x_parse_checkpoint_event__mutmut_16, 
    'x_parse_checkpoint_event__mutmut_17': x_parse_checkpoint_event__mutmut_17, 
    'x_parse_checkpoint_event__mutmut_18': x_parse_checkpoint_event__mutmut_18, 
    'x_parse_checkpoint_event__mutmut_19': x_parse_checkpoint_event__mutmut_19, 
    'x_parse_checkpoint_event__mutmut_20': x_parse_checkpoint_event__mutmut_20, 
    'x_parse_checkpoint_event__mutmut_21': x_parse_checkpoint_event__mutmut_21, 
    'x_parse_checkpoint_event__mutmut_22': x_parse_checkpoint_event__mutmut_22, 
    'x_parse_checkpoint_event__mutmut_23': x_parse_checkpoint_event__mutmut_23, 
    'x_parse_checkpoint_event__mutmut_24': x_parse_checkpoint_event__mutmut_24, 
    'x_parse_checkpoint_event__mutmut_25': x_parse_checkpoint_event__mutmut_25, 
    'x_parse_checkpoint_event__mutmut_26': x_parse_checkpoint_event__mutmut_26, 
    'x_parse_checkpoint_event__mutmut_27': x_parse_checkpoint_event__mutmut_27, 
    'x_parse_checkpoint_event__mutmut_28': x_parse_checkpoint_event__mutmut_28, 
    'x_parse_checkpoint_event__mutmut_29': x_parse_checkpoint_event__mutmut_29, 
    'x_parse_checkpoint_event__mutmut_30': x_parse_checkpoint_event__mutmut_30, 
    'x_parse_checkpoint_event__mutmut_31': x_parse_checkpoint_event__mutmut_31, 
    'x_parse_checkpoint_event__mutmut_32': x_parse_checkpoint_event__mutmut_32, 
    'x_parse_checkpoint_event__mutmut_33': x_parse_checkpoint_event__mutmut_33, 
    'x_parse_checkpoint_event__mutmut_34': x_parse_checkpoint_event__mutmut_34, 
    'x_parse_checkpoint_event__mutmut_35': x_parse_checkpoint_event__mutmut_35, 
    'x_parse_checkpoint_event__mutmut_36': x_parse_checkpoint_event__mutmut_36, 
    'x_parse_checkpoint_event__mutmut_37': x_parse_checkpoint_event__mutmut_37, 
    'x_parse_checkpoint_event__mutmut_38': x_parse_checkpoint_event__mutmut_38, 
    'x_parse_checkpoint_event__mutmut_39': x_parse_checkpoint_event__mutmut_39, 
    'x_parse_checkpoint_event__mutmut_40': x_parse_checkpoint_event__mutmut_40, 
    'x_parse_checkpoint_event__mutmut_41': x_parse_checkpoint_event__mutmut_41, 
    'x_parse_checkpoint_event__mutmut_42': x_parse_checkpoint_event__mutmut_42, 
    'x_parse_checkpoint_event__mutmut_43': x_parse_checkpoint_event__mutmut_43, 
    'x_parse_checkpoint_event__mutmut_44': x_parse_checkpoint_event__mutmut_44, 
    'x_parse_checkpoint_event__mutmut_45': x_parse_checkpoint_event__mutmut_45, 
    'x_parse_checkpoint_event__mutmut_46': x_parse_checkpoint_event__mutmut_46, 
    'x_parse_checkpoint_event__mutmut_47': x_parse_checkpoint_event__mutmut_47, 
    'x_parse_checkpoint_event__mutmut_48': x_parse_checkpoint_event__mutmut_48, 
    'x_parse_checkpoint_event__mutmut_49': x_parse_checkpoint_event__mutmut_49, 
    'x_parse_checkpoint_event__mutmut_50': x_parse_checkpoint_event__mutmut_50, 
    'x_parse_checkpoint_event__mutmut_51': x_parse_checkpoint_event__mutmut_51, 
    'x_parse_checkpoint_event__mutmut_52': x_parse_checkpoint_event__mutmut_52, 
    'x_parse_checkpoint_event__mutmut_53': x_parse_checkpoint_event__mutmut_53
}
x_parse_checkpoint_event__mutmut_orig.__name__ = 'x_parse_checkpoint_event'


def checkpoint_to_dict(checkpoint: StepCheckpoint) -> dict[str, Any]:
    args = [checkpoint]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_checkpoint_to_dict__mutmut_orig, x_checkpoint_to_dict__mutmut_mutants, args, kwargs, None)


def x_checkpoint_to_dict__mutmut_orig(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_1(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "XXmission_idXX": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_2(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "MISSION_ID": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_3(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "XXrun_idXX": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_4(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "RUN_ID": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_5(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "XXstep_idXX": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_6(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "STEP_ID": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_7(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "XXstrictnessXX": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_8(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "STRICTNESS": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_9(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "XXscope_refsXX": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_10(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "SCOPE_REFS": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_11(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"XXscopeXX": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_12(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"SCOPE": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_13(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "XXversion_idXX": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_14(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "VERSION_ID": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_15(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "XXinput_hashXX": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_16(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "INPUT_HASH": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_17(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "XXcursorXX": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_18(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "CURSOR": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_19(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "XXretry_tokenXX": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_20(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "RETRY_TOKEN": checkpoint.retry_token,
        "timestamp": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_21(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "XXtimestampXX": checkpoint.timestamp.isoformat(),
    }


def x_checkpoint_to_dict__mutmut_22(checkpoint: StepCheckpoint) -> dict[str, Any]:
    """Serialize StepCheckpoint to dict for event emission.

    Args:
        checkpoint: Checkpoint to serialize

    Returns:
        JSON-serializable dictionary
    """
    return {
        "mission_id": checkpoint.mission_id,
        "run_id": checkpoint.run_id,
        "step_id": checkpoint.step_id,
        "strictness": checkpoint.strictness.value,
        "scope_refs": [
            {"scope": ref.scope.value, "version_id": ref.version_id}
            for ref in checkpoint.scope_refs
        ],
        "input_hash": checkpoint.input_hash,
        "cursor": checkpoint.cursor,
        "retry_token": checkpoint.retry_token,
        "TIMESTAMP": checkpoint.timestamp.isoformat(),
    }

x_checkpoint_to_dict__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_checkpoint_to_dict__mutmut_1': x_checkpoint_to_dict__mutmut_1, 
    'x_checkpoint_to_dict__mutmut_2': x_checkpoint_to_dict__mutmut_2, 
    'x_checkpoint_to_dict__mutmut_3': x_checkpoint_to_dict__mutmut_3, 
    'x_checkpoint_to_dict__mutmut_4': x_checkpoint_to_dict__mutmut_4, 
    'x_checkpoint_to_dict__mutmut_5': x_checkpoint_to_dict__mutmut_5, 
    'x_checkpoint_to_dict__mutmut_6': x_checkpoint_to_dict__mutmut_6, 
    'x_checkpoint_to_dict__mutmut_7': x_checkpoint_to_dict__mutmut_7, 
    'x_checkpoint_to_dict__mutmut_8': x_checkpoint_to_dict__mutmut_8, 
    'x_checkpoint_to_dict__mutmut_9': x_checkpoint_to_dict__mutmut_9, 
    'x_checkpoint_to_dict__mutmut_10': x_checkpoint_to_dict__mutmut_10, 
    'x_checkpoint_to_dict__mutmut_11': x_checkpoint_to_dict__mutmut_11, 
    'x_checkpoint_to_dict__mutmut_12': x_checkpoint_to_dict__mutmut_12, 
    'x_checkpoint_to_dict__mutmut_13': x_checkpoint_to_dict__mutmut_13, 
    'x_checkpoint_to_dict__mutmut_14': x_checkpoint_to_dict__mutmut_14, 
    'x_checkpoint_to_dict__mutmut_15': x_checkpoint_to_dict__mutmut_15, 
    'x_checkpoint_to_dict__mutmut_16': x_checkpoint_to_dict__mutmut_16, 
    'x_checkpoint_to_dict__mutmut_17': x_checkpoint_to_dict__mutmut_17, 
    'x_checkpoint_to_dict__mutmut_18': x_checkpoint_to_dict__mutmut_18, 
    'x_checkpoint_to_dict__mutmut_19': x_checkpoint_to_dict__mutmut_19, 
    'x_checkpoint_to_dict__mutmut_20': x_checkpoint_to_dict__mutmut_20, 
    'x_checkpoint_to_dict__mutmut_21': x_checkpoint_to_dict__mutmut_21, 
    'x_checkpoint_to_dict__mutmut_22': x_checkpoint_to_dict__mutmut_22
}
x_checkpoint_to_dict__mutmut_orig.__name__ = 'x_checkpoint_to_dict'


# ---------------------------------------------------------------------------
# T033: Input hash verification
# ---------------------------------------------------------------------------


def verify_input_hash(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
) -> tuple[bool, str, str]:
    args = [checkpoint, current_inputs]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_verify_input_hash__mutmut_orig, x_verify_input_hash__mutmut_mutants, args, kwargs, None)


# ---------------------------------------------------------------------------
# T033: Input hash verification
# ---------------------------------------------------------------------------


def x_verify_input_hash__mutmut_orig(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
) -> tuple[bool, str, str]:
    """Verify current inputs match checkpoint context.

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs

    Returns:
        Tuple of (matches, old_hash_display, new_hash_display):
        - matches: True if hashes match, False if context changed
        - old_hash_display: Original hash from checkpoint (first 16 chars)
        - new_hash_display: Current hash (first 16 chars)
    """
    current_hash = compute_input_hash(current_inputs)
    matches = current_hash == checkpoint.input_hash

    return (matches, checkpoint.input_hash[:16], current_hash[:16])


# ---------------------------------------------------------------------------
# T033: Input hash verification
# ---------------------------------------------------------------------------


def x_verify_input_hash__mutmut_1(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
) -> tuple[bool, str, str]:
    """Verify current inputs match checkpoint context.

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs

    Returns:
        Tuple of (matches, old_hash_display, new_hash_display):
        - matches: True if hashes match, False if context changed
        - old_hash_display: Original hash from checkpoint (first 16 chars)
        - new_hash_display: Current hash (first 16 chars)
    """
    current_hash = None
    matches = current_hash == checkpoint.input_hash

    return (matches, checkpoint.input_hash[:16], current_hash[:16])


# ---------------------------------------------------------------------------
# T033: Input hash verification
# ---------------------------------------------------------------------------


def x_verify_input_hash__mutmut_2(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
) -> tuple[bool, str, str]:
    """Verify current inputs match checkpoint context.

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs

    Returns:
        Tuple of (matches, old_hash_display, new_hash_display):
        - matches: True if hashes match, False if context changed
        - old_hash_display: Original hash from checkpoint (first 16 chars)
        - new_hash_display: Current hash (first 16 chars)
    """
    current_hash = compute_input_hash(None)
    matches = current_hash == checkpoint.input_hash

    return (matches, checkpoint.input_hash[:16], current_hash[:16])


# ---------------------------------------------------------------------------
# T033: Input hash verification
# ---------------------------------------------------------------------------


def x_verify_input_hash__mutmut_3(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
) -> tuple[bool, str, str]:
    """Verify current inputs match checkpoint context.

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs

    Returns:
        Tuple of (matches, old_hash_display, new_hash_display):
        - matches: True if hashes match, False if context changed
        - old_hash_display: Original hash from checkpoint (first 16 chars)
        - new_hash_display: Current hash (first 16 chars)
    """
    current_hash = compute_input_hash(current_inputs)
    matches = None

    return (matches, checkpoint.input_hash[:16], current_hash[:16])


# ---------------------------------------------------------------------------
# T033: Input hash verification
# ---------------------------------------------------------------------------


def x_verify_input_hash__mutmut_4(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
) -> tuple[bool, str, str]:
    """Verify current inputs match checkpoint context.

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs

    Returns:
        Tuple of (matches, old_hash_display, new_hash_display):
        - matches: True if hashes match, False if context changed
        - old_hash_display: Original hash from checkpoint (first 16 chars)
        - new_hash_display: Current hash (first 16 chars)
    """
    current_hash = compute_input_hash(current_inputs)
    matches = current_hash != checkpoint.input_hash

    return (matches, checkpoint.input_hash[:16], current_hash[:16])


# ---------------------------------------------------------------------------
# T033: Input hash verification
# ---------------------------------------------------------------------------


def x_verify_input_hash__mutmut_5(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
) -> tuple[bool, str, str]:
    """Verify current inputs match checkpoint context.

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs

    Returns:
        Tuple of (matches, old_hash_display, new_hash_display):
        - matches: True if hashes match, False if context changed
        - old_hash_display: Original hash from checkpoint (first 16 chars)
        - new_hash_display: Current hash (first 16 chars)
    """
    current_hash = compute_input_hash(current_inputs)
    matches = current_hash == checkpoint.input_hash

    return (matches, checkpoint.input_hash[:17], current_hash[:16])


# ---------------------------------------------------------------------------
# T033: Input hash verification
# ---------------------------------------------------------------------------


def x_verify_input_hash__mutmut_6(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
) -> tuple[bool, str, str]:
    """Verify current inputs match checkpoint context.

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs

    Returns:
        Tuple of (matches, old_hash_display, new_hash_display):
        - matches: True if hashes match, False if context changed
        - old_hash_display: Original hash from checkpoint (first 16 chars)
        - new_hash_display: Current hash (first 16 chars)
    """
    current_hash = compute_input_hash(current_inputs)
    matches = current_hash == checkpoint.input_hash

    return (matches, checkpoint.input_hash[:16], current_hash[:17])

x_verify_input_hash__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_verify_input_hash__mutmut_1': x_verify_input_hash__mutmut_1, 
    'x_verify_input_hash__mutmut_2': x_verify_input_hash__mutmut_2, 
    'x_verify_input_hash__mutmut_3': x_verify_input_hash__mutmut_3, 
    'x_verify_input_hash__mutmut_4': x_verify_input_hash__mutmut_4, 
    'x_verify_input_hash__mutmut_5': x_verify_input_hash__mutmut_5, 
    'x_verify_input_hash__mutmut_6': x_verify_input_hash__mutmut_6
}
x_verify_input_hash__mutmut_orig.__name__ = 'x_verify_input_hash'


def handle_context_change(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    args = [checkpoint, current_inputs, confirm_fn]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_handle_context_change__mutmut_orig, x_handle_context_change__mutmut_mutants, args, kwargs, None)


def x_handle_context_change__mutmut_orig(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(old_hash, new_hash)
        return result

    return prompt_context_change_confirmation(old_hash, new_hash)


def x_handle_context_change__mutmut_1(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = None

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(old_hash, new_hash)
        return result

    return prompt_context_change_confirmation(old_hash, new_hash)


def x_handle_context_change__mutmut_2(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(None, current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(old_hash, new_hash)
        return result

    return prompt_context_change_confirmation(old_hash, new_hash)


def x_handle_context_change__mutmut_3(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, None)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(old_hash, new_hash)
        return result

    return prompt_context_change_confirmation(old_hash, new_hash)


def x_handle_context_change__mutmut_4(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(old_hash, new_hash)
        return result

    return prompt_context_change_confirmation(old_hash, new_hash)


def x_handle_context_change__mutmut_5(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, )

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(old_hash, new_hash)
        return result

    return prompt_context_change_confirmation(old_hash, new_hash)


def x_handle_context_change__mutmut_6(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return False

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(old_hash, new_hash)
        return result

    return prompt_context_change_confirmation(old_hash, new_hash)


def x_handle_context_change__mutmut_7(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is None:
        result: bool = confirm_fn(old_hash, new_hash)
        return result

    return prompt_context_change_confirmation(old_hash, new_hash)


def x_handle_context_change__mutmut_8(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = None
        return result

    return prompt_context_change_confirmation(old_hash, new_hash)


def x_handle_context_change__mutmut_9(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(None, new_hash)
        return result

    return prompt_context_change_confirmation(old_hash, new_hash)


def x_handle_context_change__mutmut_10(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(old_hash, None)
        return result

    return prompt_context_change_confirmation(old_hash, new_hash)


def x_handle_context_change__mutmut_11(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(new_hash)
        return result

    return prompt_context_change_confirmation(old_hash, new_hash)


def x_handle_context_change__mutmut_12(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(old_hash, )
        return result

    return prompt_context_change_confirmation(old_hash, new_hash)


def x_handle_context_change__mutmut_13(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(old_hash, new_hash)
        return result

    return prompt_context_change_confirmation(None, new_hash)


def x_handle_context_change__mutmut_14(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(old_hash, new_hash)
        return result

    return prompt_context_change_confirmation(old_hash, None)


def x_handle_context_change__mutmut_15(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(old_hash, new_hash)
        return result

    return prompt_context_change_confirmation(new_hash)


def x_handle_context_change__mutmut_16(
    checkpoint: StepCheckpoint,
    current_inputs: dict[str, Any],
    confirm_fn: Any = None,
) -> bool:
    """Handle input context change between checkpoint and resume.

    Computes current input hash and prompts user for confirmation if
    context has changed materially (per spec.md FR-019).

    Args:
        checkpoint: Checkpoint with original input_hash
        current_inputs: Current step inputs
        confirm_fn: Optional confirmation function override (for testing).
                    Signature: (old_hash: str, new_hash: str) -> bool.
                    Defaults to prompt_context_change_confirmation.

    Returns:
        True if context unchanged or user confirms resumption,
        False if user declines (abort resume)
    """
    matches, old_hash, new_hash = verify_input_hash(checkpoint, current_inputs)

    if matches:
        # Context unchanged, safe to resume
        return True

    # Context changed - prompt user for confirmation
    if confirm_fn is not None:
        result: bool = confirm_fn(old_hash, new_hash)
        return result

    return prompt_context_change_confirmation(old_hash, )

x_handle_context_change__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_handle_context_change__mutmut_1': x_handle_context_change__mutmut_1, 
    'x_handle_context_change__mutmut_2': x_handle_context_change__mutmut_2, 
    'x_handle_context_change__mutmut_3': x_handle_context_change__mutmut_3, 
    'x_handle_context_change__mutmut_4': x_handle_context_change__mutmut_4, 
    'x_handle_context_change__mutmut_5': x_handle_context_change__mutmut_5, 
    'x_handle_context_change__mutmut_6': x_handle_context_change__mutmut_6, 
    'x_handle_context_change__mutmut_7': x_handle_context_change__mutmut_7, 
    'x_handle_context_change__mutmut_8': x_handle_context_change__mutmut_8, 
    'x_handle_context_change__mutmut_9': x_handle_context_change__mutmut_9, 
    'x_handle_context_change__mutmut_10': x_handle_context_change__mutmut_10, 
    'x_handle_context_change__mutmut_11': x_handle_context_change__mutmut_11, 
    'x_handle_context_change__mutmut_12': x_handle_context_change__mutmut_12, 
    'x_handle_context_change__mutmut_13': x_handle_context_change__mutmut_13, 
    'x_handle_context_change__mutmut_14': x_handle_context_change__mutmut_14, 
    'x_handle_context_change__mutmut_15': x_handle_context_change__mutmut_15, 
    'x_handle_context_change__mutmut_16': x_handle_context_change__mutmut_16
}
x_handle_context_change__mutmut_orig.__name__ = 'x_handle_context_change'


def prompt_context_change_confirmation(
    old_hash: str,
    new_hash: str,
) -> bool:
    args = [old_hash, new_hash]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_prompt_context_change_confirmation__mutmut_orig, x_prompt_context_change_confirmation__mutmut_mutants, args, kwargs, None)


def x_prompt_context_change_confirmation__mutmut_orig(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user for confirmation when context has changed.

    This is the default confirmation prompt. WP06 may provide a richer
    implementation via glossary/prompts.py; when available, pass it as
    confirm_fn to handle_context_change().

    Args:
        old_hash: Truncated hash from checkpoint (display only)
        new_hash: Truncated hash from current inputs (display only)

    Returns:
        True if user confirms resumption, False if user declines
    """
    import typer

    typer.echo(
        f"\nContext has changed since checkpoint was created.\n"
        f"  Checkpoint hash: {old_hash}...\n"
        f"  Current hash:    {new_hash}...\n"
    )
    result: bool = typer.confirm(
        "Resume despite context change?",
        default=False,
    )
    return result


def x_prompt_context_change_confirmation__mutmut_1(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user for confirmation when context has changed.

    This is the default confirmation prompt. WP06 may provide a richer
    implementation via glossary/prompts.py; when available, pass it as
    confirm_fn to handle_context_change().

    Args:
        old_hash: Truncated hash from checkpoint (display only)
        new_hash: Truncated hash from current inputs (display only)

    Returns:
        True if user confirms resumption, False if user declines
    """
    import typer

    typer.echo(
        None
    )
    result: bool = typer.confirm(
        "Resume despite context change?",
        default=False,
    )
    return result


def x_prompt_context_change_confirmation__mutmut_2(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user for confirmation when context has changed.

    This is the default confirmation prompt. WP06 may provide a richer
    implementation via glossary/prompts.py; when available, pass it as
    confirm_fn to handle_context_change().

    Args:
        old_hash: Truncated hash from checkpoint (display only)
        new_hash: Truncated hash from current inputs (display only)

    Returns:
        True if user confirms resumption, False if user declines
    """
    import typer

    typer.echo(
        f"\nContext has changed since checkpoint was created.\n"
        f"  Checkpoint hash: {old_hash}...\n"
        f"  Current hash:    {new_hash}...\n"
    )
    result: bool = None
    return result


def x_prompt_context_change_confirmation__mutmut_3(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user for confirmation when context has changed.

    This is the default confirmation prompt. WP06 may provide a richer
    implementation via glossary/prompts.py; when available, pass it as
    confirm_fn to handle_context_change().

    Args:
        old_hash: Truncated hash from checkpoint (display only)
        new_hash: Truncated hash from current inputs (display only)

    Returns:
        True if user confirms resumption, False if user declines
    """
    import typer

    typer.echo(
        f"\nContext has changed since checkpoint was created.\n"
        f"  Checkpoint hash: {old_hash}...\n"
        f"  Current hash:    {new_hash}...\n"
    )
    result: bool = typer.confirm(
        None,
        default=False,
    )
    return result


def x_prompt_context_change_confirmation__mutmut_4(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user for confirmation when context has changed.

    This is the default confirmation prompt. WP06 may provide a richer
    implementation via glossary/prompts.py; when available, pass it as
    confirm_fn to handle_context_change().

    Args:
        old_hash: Truncated hash from checkpoint (display only)
        new_hash: Truncated hash from current inputs (display only)

    Returns:
        True if user confirms resumption, False if user declines
    """
    import typer

    typer.echo(
        f"\nContext has changed since checkpoint was created.\n"
        f"  Checkpoint hash: {old_hash}...\n"
        f"  Current hash:    {new_hash}...\n"
    )
    result: bool = typer.confirm(
        "Resume despite context change?",
        default=None,
    )
    return result


def x_prompt_context_change_confirmation__mutmut_5(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user for confirmation when context has changed.

    This is the default confirmation prompt. WP06 may provide a richer
    implementation via glossary/prompts.py; when available, pass it as
    confirm_fn to handle_context_change().

    Args:
        old_hash: Truncated hash from checkpoint (display only)
        new_hash: Truncated hash from current inputs (display only)

    Returns:
        True if user confirms resumption, False if user declines
    """
    import typer

    typer.echo(
        f"\nContext has changed since checkpoint was created.\n"
        f"  Checkpoint hash: {old_hash}...\n"
        f"  Current hash:    {new_hash}...\n"
    )
    result: bool = typer.confirm(
        default=False,
    )
    return result


def x_prompt_context_change_confirmation__mutmut_6(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user for confirmation when context has changed.

    This is the default confirmation prompt. WP06 may provide a richer
    implementation via glossary/prompts.py; when available, pass it as
    confirm_fn to handle_context_change().

    Args:
        old_hash: Truncated hash from checkpoint (display only)
        new_hash: Truncated hash from current inputs (display only)

    Returns:
        True if user confirms resumption, False if user declines
    """
    import typer

    typer.echo(
        f"\nContext has changed since checkpoint was created.\n"
        f"  Checkpoint hash: {old_hash}...\n"
        f"  Current hash:    {new_hash}...\n"
    )
    result: bool = typer.confirm(
        "Resume despite context change?",
        )
    return result


def x_prompt_context_change_confirmation__mutmut_7(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user for confirmation when context has changed.

    This is the default confirmation prompt. WP06 may provide a richer
    implementation via glossary/prompts.py; when available, pass it as
    confirm_fn to handle_context_change().

    Args:
        old_hash: Truncated hash from checkpoint (display only)
        new_hash: Truncated hash from current inputs (display only)

    Returns:
        True if user confirms resumption, False if user declines
    """
    import typer

    typer.echo(
        f"\nContext has changed since checkpoint was created.\n"
        f"  Checkpoint hash: {old_hash}...\n"
        f"  Current hash:    {new_hash}...\n"
    )
    result: bool = typer.confirm(
        "XXResume despite context change?XX",
        default=False,
    )
    return result


def x_prompt_context_change_confirmation__mutmut_8(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user for confirmation when context has changed.

    This is the default confirmation prompt. WP06 may provide a richer
    implementation via glossary/prompts.py; when available, pass it as
    confirm_fn to handle_context_change().

    Args:
        old_hash: Truncated hash from checkpoint (display only)
        new_hash: Truncated hash from current inputs (display only)

    Returns:
        True if user confirms resumption, False if user declines
    """
    import typer

    typer.echo(
        f"\nContext has changed since checkpoint was created.\n"
        f"  Checkpoint hash: {old_hash}...\n"
        f"  Current hash:    {new_hash}...\n"
    )
    result: bool = typer.confirm(
        "resume despite context change?",
        default=False,
    )
    return result


def x_prompt_context_change_confirmation__mutmut_9(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user for confirmation when context has changed.

    This is the default confirmation prompt. WP06 may provide a richer
    implementation via glossary/prompts.py; when available, pass it as
    confirm_fn to handle_context_change().

    Args:
        old_hash: Truncated hash from checkpoint (display only)
        new_hash: Truncated hash from current inputs (display only)

    Returns:
        True if user confirms resumption, False if user declines
    """
    import typer

    typer.echo(
        f"\nContext has changed since checkpoint was created.\n"
        f"  Checkpoint hash: {old_hash}...\n"
        f"  Current hash:    {new_hash}...\n"
    )
    result: bool = typer.confirm(
        "RESUME DESPITE CONTEXT CHANGE?",
        default=False,
    )
    return result


def x_prompt_context_change_confirmation__mutmut_10(
    old_hash: str,
    new_hash: str,
) -> bool:
    """Prompt user for confirmation when context has changed.

    This is the default confirmation prompt. WP06 may provide a richer
    implementation via glossary/prompts.py; when available, pass it as
    confirm_fn to handle_context_change().

    Args:
        old_hash: Truncated hash from checkpoint (display only)
        new_hash: Truncated hash from current inputs (display only)

    Returns:
        True if user confirms resumption, False if user declines
    """
    import typer

    typer.echo(
        f"\nContext has changed since checkpoint was created.\n"
        f"  Checkpoint hash: {old_hash}...\n"
        f"  Current hash:    {new_hash}...\n"
    )
    result: bool = typer.confirm(
        "Resume despite context change?",
        default=True,
    )
    return result

x_prompt_context_change_confirmation__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_prompt_context_change_confirmation__mutmut_1': x_prompt_context_change_confirmation__mutmut_1, 
    'x_prompt_context_change_confirmation__mutmut_2': x_prompt_context_change_confirmation__mutmut_2, 
    'x_prompt_context_change_confirmation__mutmut_3': x_prompt_context_change_confirmation__mutmut_3, 
    'x_prompt_context_change_confirmation__mutmut_4': x_prompt_context_change_confirmation__mutmut_4, 
    'x_prompt_context_change_confirmation__mutmut_5': x_prompt_context_change_confirmation__mutmut_5, 
    'x_prompt_context_change_confirmation__mutmut_6': x_prompt_context_change_confirmation__mutmut_6, 
    'x_prompt_context_change_confirmation__mutmut_7': x_prompt_context_change_confirmation__mutmut_7, 
    'x_prompt_context_change_confirmation__mutmut_8': x_prompt_context_change_confirmation__mutmut_8, 
    'x_prompt_context_change_confirmation__mutmut_9': x_prompt_context_change_confirmation__mutmut_9, 
    'x_prompt_context_change_confirmation__mutmut_10': x_prompt_context_change_confirmation__mutmut_10
}
x_prompt_context_change_confirmation__mutmut_orig.__name__ = 'x_prompt_context_change_confirmation'


def compute_input_diff(
    old_inputs: dict[str, Any],
    new_inputs: dict[str, Any],
) -> dict[str, tuple[Any, Any]]:
    args = [old_inputs, new_inputs]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_compute_input_diff__mutmut_orig, x_compute_input_diff__mutmut_mutants, args, kwargs, None)


def x_compute_input_diff__mutmut_orig(
    old_inputs: dict[str, Any],
    new_inputs: dict[str, Any],
) -> dict[str, tuple[Any, Any]]:
    """Compute detailed diff between old and new inputs.

    Useful for debugging context changes -- shows which keys changed,
    were added, or were removed.

    Args:
        old_inputs: Original inputs from checkpoint
        new_inputs: Current inputs

    Returns:
        Dict mapping changed keys to (old_value, new_value) tuples.
        Removed keys have new_value=None; added keys have old_value=None.
    """
    diff: dict[str, tuple[Any, Any]] = {}

    # Find changed/removed keys
    for key in old_inputs:
        old_val = old_inputs[key]
        new_val = new_inputs.get(key)

        if new_val != old_val:
            diff[key] = (old_val, new_val)

    # Find added keys
    for key in new_inputs:
        if key not in old_inputs:
            diff[key] = (None, new_inputs[key])

    return diff


def x_compute_input_diff__mutmut_1(
    old_inputs: dict[str, Any],
    new_inputs: dict[str, Any],
) -> dict[str, tuple[Any, Any]]:
    """Compute detailed diff between old and new inputs.

    Useful for debugging context changes -- shows which keys changed,
    were added, or were removed.

    Args:
        old_inputs: Original inputs from checkpoint
        new_inputs: Current inputs

    Returns:
        Dict mapping changed keys to (old_value, new_value) tuples.
        Removed keys have new_value=None; added keys have old_value=None.
    """
    diff: dict[str, tuple[Any, Any]] = None

    # Find changed/removed keys
    for key in old_inputs:
        old_val = old_inputs[key]
        new_val = new_inputs.get(key)

        if new_val != old_val:
            diff[key] = (old_val, new_val)

    # Find added keys
    for key in new_inputs:
        if key not in old_inputs:
            diff[key] = (None, new_inputs[key])

    return diff


def x_compute_input_diff__mutmut_2(
    old_inputs: dict[str, Any],
    new_inputs: dict[str, Any],
) -> dict[str, tuple[Any, Any]]:
    """Compute detailed diff between old and new inputs.

    Useful for debugging context changes -- shows which keys changed,
    were added, or were removed.

    Args:
        old_inputs: Original inputs from checkpoint
        new_inputs: Current inputs

    Returns:
        Dict mapping changed keys to (old_value, new_value) tuples.
        Removed keys have new_value=None; added keys have old_value=None.
    """
    diff: dict[str, tuple[Any, Any]] = {}

    # Find changed/removed keys
    for key in old_inputs:
        old_val = None
        new_val = new_inputs.get(key)

        if new_val != old_val:
            diff[key] = (old_val, new_val)

    # Find added keys
    for key in new_inputs:
        if key not in old_inputs:
            diff[key] = (None, new_inputs[key])

    return diff


def x_compute_input_diff__mutmut_3(
    old_inputs: dict[str, Any],
    new_inputs: dict[str, Any],
) -> dict[str, tuple[Any, Any]]:
    """Compute detailed diff between old and new inputs.

    Useful for debugging context changes -- shows which keys changed,
    were added, or were removed.

    Args:
        old_inputs: Original inputs from checkpoint
        new_inputs: Current inputs

    Returns:
        Dict mapping changed keys to (old_value, new_value) tuples.
        Removed keys have new_value=None; added keys have old_value=None.
    """
    diff: dict[str, tuple[Any, Any]] = {}

    # Find changed/removed keys
    for key in old_inputs:
        old_val = old_inputs[key]
        new_val = None

        if new_val != old_val:
            diff[key] = (old_val, new_val)

    # Find added keys
    for key in new_inputs:
        if key not in old_inputs:
            diff[key] = (None, new_inputs[key])

    return diff


def x_compute_input_diff__mutmut_4(
    old_inputs: dict[str, Any],
    new_inputs: dict[str, Any],
) -> dict[str, tuple[Any, Any]]:
    """Compute detailed diff between old and new inputs.

    Useful for debugging context changes -- shows which keys changed,
    were added, or were removed.

    Args:
        old_inputs: Original inputs from checkpoint
        new_inputs: Current inputs

    Returns:
        Dict mapping changed keys to (old_value, new_value) tuples.
        Removed keys have new_value=None; added keys have old_value=None.
    """
    diff: dict[str, tuple[Any, Any]] = {}

    # Find changed/removed keys
    for key in old_inputs:
        old_val = old_inputs[key]
        new_val = new_inputs.get(None)

        if new_val != old_val:
            diff[key] = (old_val, new_val)

    # Find added keys
    for key in new_inputs:
        if key not in old_inputs:
            diff[key] = (None, new_inputs[key])

    return diff


def x_compute_input_diff__mutmut_5(
    old_inputs: dict[str, Any],
    new_inputs: dict[str, Any],
) -> dict[str, tuple[Any, Any]]:
    """Compute detailed diff between old and new inputs.

    Useful for debugging context changes -- shows which keys changed,
    were added, or were removed.

    Args:
        old_inputs: Original inputs from checkpoint
        new_inputs: Current inputs

    Returns:
        Dict mapping changed keys to (old_value, new_value) tuples.
        Removed keys have new_value=None; added keys have old_value=None.
    """
    diff: dict[str, tuple[Any, Any]] = {}

    # Find changed/removed keys
    for key in old_inputs:
        old_val = old_inputs[key]
        new_val = new_inputs.get(key)

        if new_val == old_val:
            diff[key] = (old_val, new_val)

    # Find added keys
    for key in new_inputs:
        if key not in old_inputs:
            diff[key] = (None, new_inputs[key])

    return diff


def x_compute_input_diff__mutmut_6(
    old_inputs: dict[str, Any],
    new_inputs: dict[str, Any],
) -> dict[str, tuple[Any, Any]]:
    """Compute detailed diff between old and new inputs.

    Useful for debugging context changes -- shows which keys changed,
    were added, or were removed.

    Args:
        old_inputs: Original inputs from checkpoint
        new_inputs: Current inputs

    Returns:
        Dict mapping changed keys to (old_value, new_value) tuples.
        Removed keys have new_value=None; added keys have old_value=None.
    """
    diff: dict[str, tuple[Any, Any]] = {}

    # Find changed/removed keys
    for key in old_inputs:
        old_val = old_inputs[key]
        new_val = new_inputs.get(key)

        if new_val != old_val:
            diff[key] = None

    # Find added keys
    for key in new_inputs:
        if key not in old_inputs:
            diff[key] = (None, new_inputs[key])

    return diff


def x_compute_input_diff__mutmut_7(
    old_inputs: dict[str, Any],
    new_inputs: dict[str, Any],
) -> dict[str, tuple[Any, Any]]:
    """Compute detailed diff between old and new inputs.

    Useful for debugging context changes -- shows which keys changed,
    were added, or were removed.

    Args:
        old_inputs: Original inputs from checkpoint
        new_inputs: Current inputs

    Returns:
        Dict mapping changed keys to (old_value, new_value) tuples.
        Removed keys have new_value=None; added keys have old_value=None.
    """
    diff: dict[str, tuple[Any, Any]] = {}

    # Find changed/removed keys
    for key in old_inputs:
        old_val = old_inputs[key]
        new_val = new_inputs.get(key)

        if new_val != old_val:
            diff[key] = (old_val, new_val)

    # Find added keys
    for key in new_inputs:
        if key in old_inputs:
            diff[key] = (None, new_inputs[key])

    return diff


def x_compute_input_diff__mutmut_8(
    old_inputs: dict[str, Any],
    new_inputs: dict[str, Any],
) -> dict[str, tuple[Any, Any]]:
    """Compute detailed diff between old and new inputs.

    Useful for debugging context changes -- shows which keys changed,
    were added, or were removed.

    Args:
        old_inputs: Original inputs from checkpoint
        new_inputs: Current inputs

    Returns:
        Dict mapping changed keys to (old_value, new_value) tuples.
        Removed keys have new_value=None; added keys have old_value=None.
    """
    diff: dict[str, tuple[Any, Any]] = {}

    # Find changed/removed keys
    for key in old_inputs:
        old_val = old_inputs[key]
        new_val = new_inputs.get(key)

        if new_val != old_val:
            diff[key] = (old_val, new_val)

    # Find added keys
    for key in new_inputs:
        if key not in old_inputs:
            diff[key] = None

    return diff

x_compute_input_diff__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_compute_input_diff__mutmut_1': x_compute_input_diff__mutmut_1, 
    'x_compute_input_diff__mutmut_2': x_compute_input_diff__mutmut_2, 
    'x_compute_input_diff__mutmut_3': x_compute_input_diff__mutmut_3, 
    'x_compute_input_diff__mutmut_4': x_compute_input_diff__mutmut_4, 
    'x_compute_input_diff__mutmut_5': x_compute_input_diff__mutmut_5, 
    'x_compute_input_diff__mutmut_6': x_compute_input_diff__mutmut_6, 
    'x_compute_input_diff__mutmut_7': x_compute_input_diff__mutmut_7, 
    'x_compute_input_diff__mutmut_8': x_compute_input_diff__mutmut_8
}
x_compute_input_diff__mutmut_orig.__name__ = 'x_compute_input_diff'
