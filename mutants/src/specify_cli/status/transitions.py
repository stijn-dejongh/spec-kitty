"""Transition matrix, guard conditions, alias resolution, and validation.

Implements the 7-lane state machine with 17 legal transition pairs,
guard condition functions, alias resolution, and force-override logic.
"""

from __future__ import annotations

from typing import Any

from .models import Lane

CANONICAL_LANES: tuple[str, ...] = (
    "planned",
    "claimed",
    "in_progress",
    "for_review",
    "done",
    "blocked",
    "canceled",
)

LANE_ALIASES: dict[str, str] = {"doing": "in_progress"}

TERMINAL_LANES: frozenset[str] = frozenset({"done", "canceled"})

ALLOWED_TRANSITIONS: frozenset[tuple[str, str]] = frozenset(
    {
        ("planned", "claimed"),
        ("claimed", "in_progress"),
        ("in_progress", "for_review"),
        ("for_review", "done"),
        ("for_review", "in_progress"),
        ("for_review", "planned"),
        ("in_progress", "planned"),
        ("planned", "blocked"),
        ("claimed", "blocked"),
        ("in_progress", "blocked"),
        ("for_review", "blocked"),
        ("blocked", "in_progress"),
        ("planned", "canceled"),
        ("claimed", "canceled"),
        ("in_progress", "canceled"),
        ("for_review", "canceled"),
        ("blocked", "canceled"),
    }
)

# Map of (from_lane, to_lane) -> guard function name
_GUARDED_TRANSITIONS: dict[tuple[str, str], str] = {
    ("planned", "claimed"): "actor_required",
    ("claimed", "in_progress"): "workspace_context",
    ("in_progress", "for_review"): "subtasks_complete_or_force",
    ("for_review", "done"): "reviewer_approval",
    ("for_review", "in_progress"): "review_ref_required",
    ("for_review", "planned"): "review_ref_required",
    ("in_progress", "planned"): "reason_required",
}
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


def resolve_lane_alias(lane: str) -> str:
    args = [lane]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_resolve_lane_alias__mutmut_orig, x_resolve_lane_alias__mutmut_mutants, args, kwargs, None)


def x_resolve_lane_alias__mutmut_orig(lane: str) -> str:
    """Resolve alias to canonical lane name. Returns input if not an alias."""
    normalized = lane.strip().lower()
    return LANE_ALIASES.get(normalized, normalized)


def x_resolve_lane_alias__mutmut_1(lane: str) -> str:
    """Resolve alias to canonical lane name. Returns input if not an alias."""
    normalized = None
    return LANE_ALIASES.get(normalized, normalized)


def x_resolve_lane_alias__mutmut_2(lane: str) -> str:
    """Resolve alias to canonical lane name. Returns input if not an alias."""
    normalized = lane.strip().upper()
    return LANE_ALIASES.get(normalized, normalized)


def x_resolve_lane_alias__mutmut_3(lane: str) -> str:
    """Resolve alias to canonical lane name. Returns input if not an alias."""
    normalized = lane.strip().lower()
    return LANE_ALIASES.get(None, normalized)


def x_resolve_lane_alias__mutmut_4(lane: str) -> str:
    """Resolve alias to canonical lane name. Returns input if not an alias."""
    normalized = lane.strip().lower()
    return LANE_ALIASES.get(normalized, None)


def x_resolve_lane_alias__mutmut_5(lane: str) -> str:
    """Resolve alias to canonical lane name. Returns input if not an alias."""
    normalized = lane.strip().lower()
    return LANE_ALIASES.get(normalized)


def x_resolve_lane_alias__mutmut_6(lane: str) -> str:
    """Resolve alias to canonical lane name. Returns input if not an alias."""
    normalized = lane.strip().lower()
    return LANE_ALIASES.get(normalized, )

x_resolve_lane_alias__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_resolve_lane_alias__mutmut_1': x_resolve_lane_alias__mutmut_1, 
    'x_resolve_lane_alias__mutmut_2': x_resolve_lane_alias__mutmut_2, 
    'x_resolve_lane_alias__mutmut_3': x_resolve_lane_alias__mutmut_3, 
    'x_resolve_lane_alias__mutmut_4': x_resolve_lane_alias__mutmut_4, 
    'x_resolve_lane_alias__mutmut_5': x_resolve_lane_alias__mutmut_5, 
    'x_resolve_lane_alias__mutmut_6': x_resolve_lane_alias__mutmut_6
}
x_resolve_lane_alias__mutmut_orig.__name__ = 'x_resolve_lane_alias'


def is_terminal(lane: str) -> bool:
    args = [lane]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_is_terminal__mutmut_orig, x_is_terminal__mutmut_mutants, args, kwargs, None)


def x_is_terminal__mutmut_orig(lane: str) -> bool:
    """Check if a lane is terminal (done or canceled)."""
    return resolve_lane_alias(lane) in TERMINAL_LANES


def x_is_terminal__mutmut_1(lane: str) -> bool:
    """Check if a lane is terminal (done or canceled)."""
    return resolve_lane_alias(None) in TERMINAL_LANES


def x_is_terminal__mutmut_2(lane: str) -> bool:
    """Check if a lane is terminal (done or canceled)."""
    return resolve_lane_alias(lane) not in TERMINAL_LANES

x_is_terminal__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_is_terminal__mutmut_1': x_is_terminal__mutmut_1, 
    'x_is_terminal__mutmut_2': x_is_terminal__mutmut_2
}
x_is_terminal__mutmut_orig.__name__ = 'x_is_terminal'


def _guard_actor_required(actor: str | None) -> tuple[bool, str | None]:
    args = [actor]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__guard_actor_required__mutmut_orig, x__guard_actor_required__mutmut_mutants, args, kwargs, None)


def x__guard_actor_required__mutmut_orig(actor: str | None) -> tuple[bool, str | None]:
    """Guard: planned -> claimed requires actor identity."""
    if not actor or not actor.strip():
        return False, "Transition planned -> claimed requires actor identity"
    return True, None


def x__guard_actor_required__mutmut_1(actor: str | None) -> tuple[bool, str | None]:
    """Guard: planned -> claimed requires actor identity."""
    if not actor and not actor.strip():
        return False, "Transition planned -> claimed requires actor identity"
    return True, None


def x__guard_actor_required__mutmut_2(actor: str | None) -> tuple[bool, str | None]:
    """Guard: planned -> claimed requires actor identity."""
    if actor or not actor.strip():
        return False, "Transition planned -> claimed requires actor identity"
    return True, None


def x__guard_actor_required__mutmut_3(actor: str | None) -> tuple[bool, str | None]:
    """Guard: planned -> claimed requires actor identity."""
    if not actor or actor.strip():
        return False, "Transition planned -> claimed requires actor identity"
    return True, None


def x__guard_actor_required__mutmut_4(actor: str | None) -> tuple[bool, str | None]:
    """Guard: planned -> claimed requires actor identity."""
    if not actor or not actor.strip():
        return True, "Transition planned -> claimed requires actor identity"
    return True, None


def x__guard_actor_required__mutmut_5(actor: str | None) -> tuple[bool, str | None]:
    """Guard: planned -> claimed requires actor identity."""
    if not actor or not actor.strip():
        return False, "XXTransition planned -> claimed requires actor identityXX"
    return True, None


def x__guard_actor_required__mutmut_6(actor: str | None) -> tuple[bool, str | None]:
    """Guard: planned -> claimed requires actor identity."""
    if not actor or not actor.strip():
        return False, "transition planned -> claimed requires actor identity"
    return True, None


def x__guard_actor_required__mutmut_7(actor: str | None) -> tuple[bool, str | None]:
    """Guard: planned -> claimed requires actor identity."""
    if not actor or not actor.strip():
        return False, "TRANSITION PLANNED -> CLAIMED REQUIRES ACTOR IDENTITY"
    return True, None


def x__guard_actor_required__mutmut_8(actor: str | None) -> tuple[bool, str | None]:
    """Guard: planned -> claimed requires actor identity."""
    if not actor or not actor.strip():
        return False, "Transition planned -> claimed requires actor identity"
    return False, None

x__guard_actor_required__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__guard_actor_required__mutmut_1': x__guard_actor_required__mutmut_1, 
    'x__guard_actor_required__mutmut_2': x__guard_actor_required__mutmut_2, 
    'x__guard_actor_required__mutmut_3': x__guard_actor_required__mutmut_3, 
    'x__guard_actor_required__mutmut_4': x__guard_actor_required__mutmut_4, 
    'x__guard_actor_required__mutmut_5': x__guard_actor_required__mutmut_5, 
    'x__guard_actor_required__mutmut_6': x__guard_actor_required__mutmut_6, 
    'x__guard_actor_required__mutmut_7': x__guard_actor_required__mutmut_7, 
    'x__guard_actor_required__mutmut_8': x__guard_actor_required__mutmut_8
}
x__guard_actor_required__mutmut_orig.__name__ = 'x__guard_actor_required'


def _guard_workspace_context(
    workspace_context: str | None,
) -> tuple[bool, str | None]:
    args = [workspace_context]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__guard_workspace_context__mutmut_orig, x__guard_workspace_context__mutmut_mutants, args, kwargs, None)


def x__guard_workspace_context__mutmut_orig(
    workspace_context: str | None,
) -> tuple[bool, str | None]:
    """Guard: claimed -> in_progress requires active workspace context."""
    if not workspace_context or not workspace_context.strip():
        return (
            False,
            "Transition claimed -> in_progress requires workspace context",
        )
    return True, None


def x__guard_workspace_context__mutmut_1(
    workspace_context: str | None,
) -> tuple[bool, str | None]:
    """Guard: claimed -> in_progress requires active workspace context."""
    if not workspace_context and not workspace_context.strip():
        return (
            False,
            "Transition claimed -> in_progress requires workspace context",
        )
    return True, None


def x__guard_workspace_context__mutmut_2(
    workspace_context: str | None,
) -> tuple[bool, str | None]:
    """Guard: claimed -> in_progress requires active workspace context."""
    if workspace_context or not workspace_context.strip():
        return (
            False,
            "Transition claimed -> in_progress requires workspace context",
        )
    return True, None


def x__guard_workspace_context__mutmut_3(
    workspace_context: str | None,
) -> tuple[bool, str | None]:
    """Guard: claimed -> in_progress requires active workspace context."""
    if not workspace_context or workspace_context.strip():
        return (
            False,
            "Transition claimed -> in_progress requires workspace context",
        )
    return True, None


def x__guard_workspace_context__mutmut_4(
    workspace_context: str | None,
) -> tuple[bool, str | None]:
    """Guard: claimed -> in_progress requires active workspace context."""
    if not workspace_context or not workspace_context.strip():
        return (
            True,
            "Transition claimed -> in_progress requires workspace context",
        )
    return True, None


def x__guard_workspace_context__mutmut_5(
    workspace_context: str | None,
) -> tuple[bool, str | None]:
    """Guard: claimed -> in_progress requires active workspace context."""
    if not workspace_context or not workspace_context.strip():
        return (
            False,
            "XXTransition claimed -> in_progress requires workspace contextXX",
        )
    return True, None


def x__guard_workspace_context__mutmut_6(
    workspace_context: str | None,
) -> tuple[bool, str | None]:
    """Guard: claimed -> in_progress requires active workspace context."""
    if not workspace_context or not workspace_context.strip():
        return (
            False,
            "transition claimed -> in_progress requires workspace context",
        )
    return True, None


def x__guard_workspace_context__mutmut_7(
    workspace_context: str | None,
) -> tuple[bool, str | None]:
    """Guard: claimed -> in_progress requires active workspace context."""
    if not workspace_context or not workspace_context.strip():
        return (
            False,
            "TRANSITION CLAIMED -> IN_PROGRESS REQUIRES WORKSPACE CONTEXT",
        )
    return True, None


def x__guard_workspace_context__mutmut_8(
    workspace_context: str | None,
) -> tuple[bool, str | None]:
    """Guard: claimed -> in_progress requires active workspace context."""
    if not workspace_context or not workspace_context.strip():
        return (
            False,
            "Transition claimed -> in_progress requires workspace context",
        )
    return False, None

x__guard_workspace_context__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__guard_workspace_context__mutmut_1': x__guard_workspace_context__mutmut_1, 
    'x__guard_workspace_context__mutmut_2': x__guard_workspace_context__mutmut_2, 
    'x__guard_workspace_context__mutmut_3': x__guard_workspace_context__mutmut_3, 
    'x__guard_workspace_context__mutmut_4': x__guard_workspace_context__mutmut_4, 
    'x__guard_workspace_context__mutmut_5': x__guard_workspace_context__mutmut_5, 
    'x__guard_workspace_context__mutmut_6': x__guard_workspace_context__mutmut_6, 
    'x__guard_workspace_context__mutmut_7': x__guard_workspace_context__mutmut_7, 
    'x__guard_workspace_context__mutmut_8': x__guard_workspace_context__mutmut_8
}
x__guard_workspace_context__mutmut_orig.__name__ = 'x__guard_workspace_context'


def _guard_subtasks_complete_or_force(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    args = [subtasks_complete, implementation_evidence_present, force]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__guard_subtasks_complete_or_force__mutmut_orig, x__guard_subtasks_complete_or_force__mutmut_mutants, args, kwargs, None)


def x__guard_subtasks_complete_or_force__mutmut_orig(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_1(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return False, None
    if subtasks_complete is not True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_2(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_3(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not False:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_4(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            True,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_5(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "XXTransition in_progress -> for_review requires completed subtasks XX"
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_6(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_7(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "TRANSITION IN_PROGRESS -> FOR_REVIEW REQUIRES COMPLETED SUBTASKS "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_8(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "XXor force with reasonXX",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_9(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "OR FORCE WITH REASON",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_10(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_11(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not False:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_12(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            True,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_13(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "XXTransition in_progress -> for_review requires implementation evidence XX"
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_14(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_15(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "TRANSITION IN_PROGRESS -> FOR_REVIEW REQUIRES IMPLEMENTATION EVIDENCE "
            "or force with reason",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_16(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "XXor force with reasonXX",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_17(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "OR FORCE WITH REASON",
        )
    return True, None


def x__guard_subtasks_complete_or_force__mutmut_18(
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    force: bool,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> for_review requires subtask completion and evidence."""
    if force:
        return True, None
    if subtasks_complete is not True:
        return (
            False,
            "Transition in_progress -> for_review requires completed subtasks "
            "or force with reason",
        )
    if implementation_evidence_present is not True:
        return (
            False,
            "Transition in_progress -> for_review requires implementation evidence "
            "or force with reason",
        )
    return False, None

x__guard_subtasks_complete_or_force__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__guard_subtasks_complete_or_force__mutmut_1': x__guard_subtasks_complete_or_force__mutmut_1, 
    'x__guard_subtasks_complete_or_force__mutmut_2': x__guard_subtasks_complete_or_force__mutmut_2, 
    'x__guard_subtasks_complete_or_force__mutmut_3': x__guard_subtasks_complete_or_force__mutmut_3, 
    'x__guard_subtasks_complete_or_force__mutmut_4': x__guard_subtasks_complete_or_force__mutmut_4, 
    'x__guard_subtasks_complete_or_force__mutmut_5': x__guard_subtasks_complete_or_force__mutmut_5, 
    'x__guard_subtasks_complete_or_force__mutmut_6': x__guard_subtasks_complete_or_force__mutmut_6, 
    'x__guard_subtasks_complete_or_force__mutmut_7': x__guard_subtasks_complete_or_force__mutmut_7, 
    'x__guard_subtasks_complete_or_force__mutmut_8': x__guard_subtasks_complete_or_force__mutmut_8, 
    'x__guard_subtasks_complete_or_force__mutmut_9': x__guard_subtasks_complete_or_force__mutmut_9, 
    'x__guard_subtasks_complete_or_force__mutmut_10': x__guard_subtasks_complete_or_force__mutmut_10, 
    'x__guard_subtasks_complete_or_force__mutmut_11': x__guard_subtasks_complete_or_force__mutmut_11, 
    'x__guard_subtasks_complete_or_force__mutmut_12': x__guard_subtasks_complete_or_force__mutmut_12, 
    'x__guard_subtasks_complete_or_force__mutmut_13': x__guard_subtasks_complete_or_force__mutmut_13, 
    'x__guard_subtasks_complete_or_force__mutmut_14': x__guard_subtasks_complete_or_force__mutmut_14, 
    'x__guard_subtasks_complete_or_force__mutmut_15': x__guard_subtasks_complete_or_force__mutmut_15, 
    'x__guard_subtasks_complete_or_force__mutmut_16': x__guard_subtasks_complete_or_force__mutmut_16, 
    'x__guard_subtasks_complete_or_force__mutmut_17': x__guard_subtasks_complete_or_force__mutmut_17, 
    'x__guard_subtasks_complete_or_force__mutmut_18': x__guard_subtasks_complete_or_force__mutmut_18
}
x__guard_subtasks_complete_or_force__mutmut_orig.__name__ = 'x__guard_subtasks_complete_or_force'


def _guard_reviewer_approval(
    evidence: Any,
) -> tuple[bool, str | None]:
    args = [evidence]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__guard_reviewer_approval__mutmut_orig, x__guard_reviewer_approval__mutmut_mutants, args, kwargs, None)


def x__guard_reviewer_approval__mutmut_orig(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_1(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is not None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_2(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            True,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_3(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "XXTransition for_review -> done requires evidence XX"
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_4(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_5(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "TRANSITION FOR_REVIEW -> DONE REQUIRES EVIDENCE "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_6(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "XX(reviewer identity and approval reference)XX",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_7(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(REVIEWER IDENTITY AND APPROVAL REFERENCE)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_8(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = None
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_9(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(None, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_10(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, None, None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_11(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr("review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_12(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_13(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", )
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_14(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "XXreviewXX", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_15(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "REVIEW", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_16(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_17(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(None, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_18(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, None, None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_19(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr("reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_20(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_21(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", ) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_22(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "XXreviewerXX", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_23(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "REVIEWER", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_24(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_25(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_26(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(None, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_27(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, None, None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_28(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr("reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_29(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_30(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", ) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_31(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "XXreferenceXX", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_32(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "REFERENCE", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_33(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_34(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer and not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_35(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_36(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_37(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(None).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_38(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            True,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_39(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "XXTransition for_review -> done requires evidence XX"
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_40(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_41(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "TRANSITION FOR_REVIEW -> DONE REQUIRES EVIDENCE "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_42(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "XX(reviewer identity and approval reference)XX",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_43(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(REVIEWER IDENTITY AND APPROVAL REFERENCE)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_44(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference and not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_45(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_46(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_47(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(None).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_48(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            True,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_49(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "XXTransition for_review -> done requires evidence XX"
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_50(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_51(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "TRANSITION FOR_REVIEW -> DONE REQUIRES EVIDENCE "
            "(reviewer identity and approval reference)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_52(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "XX(reviewer identity and approval reference)XX",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_53(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(REVIEWER IDENTITY AND APPROVAL REFERENCE)",
        )
    return True, None


def x__guard_reviewer_approval__mutmut_54(
    evidence: Any,
) -> tuple[bool, str | None]:
    """Guard: for_review -> done requires reviewer approval evidence."""
    if evidence is None:
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    review = getattr(evidence, "review", None)
    reviewer = getattr(review, "reviewer", None) if review is not None else None
    reference = getattr(review, "reference", None) if review is not None else None
    if not reviewer or not str(reviewer).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    if not reference or not str(reference).strip():
        return (
            False,
            "Transition for_review -> done requires evidence "
            "(reviewer identity and approval reference)",
        )
    return False, None

x__guard_reviewer_approval__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__guard_reviewer_approval__mutmut_1': x__guard_reviewer_approval__mutmut_1, 
    'x__guard_reviewer_approval__mutmut_2': x__guard_reviewer_approval__mutmut_2, 
    'x__guard_reviewer_approval__mutmut_3': x__guard_reviewer_approval__mutmut_3, 
    'x__guard_reviewer_approval__mutmut_4': x__guard_reviewer_approval__mutmut_4, 
    'x__guard_reviewer_approval__mutmut_5': x__guard_reviewer_approval__mutmut_5, 
    'x__guard_reviewer_approval__mutmut_6': x__guard_reviewer_approval__mutmut_6, 
    'x__guard_reviewer_approval__mutmut_7': x__guard_reviewer_approval__mutmut_7, 
    'x__guard_reviewer_approval__mutmut_8': x__guard_reviewer_approval__mutmut_8, 
    'x__guard_reviewer_approval__mutmut_9': x__guard_reviewer_approval__mutmut_9, 
    'x__guard_reviewer_approval__mutmut_10': x__guard_reviewer_approval__mutmut_10, 
    'x__guard_reviewer_approval__mutmut_11': x__guard_reviewer_approval__mutmut_11, 
    'x__guard_reviewer_approval__mutmut_12': x__guard_reviewer_approval__mutmut_12, 
    'x__guard_reviewer_approval__mutmut_13': x__guard_reviewer_approval__mutmut_13, 
    'x__guard_reviewer_approval__mutmut_14': x__guard_reviewer_approval__mutmut_14, 
    'x__guard_reviewer_approval__mutmut_15': x__guard_reviewer_approval__mutmut_15, 
    'x__guard_reviewer_approval__mutmut_16': x__guard_reviewer_approval__mutmut_16, 
    'x__guard_reviewer_approval__mutmut_17': x__guard_reviewer_approval__mutmut_17, 
    'x__guard_reviewer_approval__mutmut_18': x__guard_reviewer_approval__mutmut_18, 
    'x__guard_reviewer_approval__mutmut_19': x__guard_reviewer_approval__mutmut_19, 
    'x__guard_reviewer_approval__mutmut_20': x__guard_reviewer_approval__mutmut_20, 
    'x__guard_reviewer_approval__mutmut_21': x__guard_reviewer_approval__mutmut_21, 
    'x__guard_reviewer_approval__mutmut_22': x__guard_reviewer_approval__mutmut_22, 
    'x__guard_reviewer_approval__mutmut_23': x__guard_reviewer_approval__mutmut_23, 
    'x__guard_reviewer_approval__mutmut_24': x__guard_reviewer_approval__mutmut_24, 
    'x__guard_reviewer_approval__mutmut_25': x__guard_reviewer_approval__mutmut_25, 
    'x__guard_reviewer_approval__mutmut_26': x__guard_reviewer_approval__mutmut_26, 
    'x__guard_reviewer_approval__mutmut_27': x__guard_reviewer_approval__mutmut_27, 
    'x__guard_reviewer_approval__mutmut_28': x__guard_reviewer_approval__mutmut_28, 
    'x__guard_reviewer_approval__mutmut_29': x__guard_reviewer_approval__mutmut_29, 
    'x__guard_reviewer_approval__mutmut_30': x__guard_reviewer_approval__mutmut_30, 
    'x__guard_reviewer_approval__mutmut_31': x__guard_reviewer_approval__mutmut_31, 
    'x__guard_reviewer_approval__mutmut_32': x__guard_reviewer_approval__mutmut_32, 
    'x__guard_reviewer_approval__mutmut_33': x__guard_reviewer_approval__mutmut_33, 
    'x__guard_reviewer_approval__mutmut_34': x__guard_reviewer_approval__mutmut_34, 
    'x__guard_reviewer_approval__mutmut_35': x__guard_reviewer_approval__mutmut_35, 
    'x__guard_reviewer_approval__mutmut_36': x__guard_reviewer_approval__mutmut_36, 
    'x__guard_reviewer_approval__mutmut_37': x__guard_reviewer_approval__mutmut_37, 
    'x__guard_reviewer_approval__mutmut_38': x__guard_reviewer_approval__mutmut_38, 
    'x__guard_reviewer_approval__mutmut_39': x__guard_reviewer_approval__mutmut_39, 
    'x__guard_reviewer_approval__mutmut_40': x__guard_reviewer_approval__mutmut_40, 
    'x__guard_reviewer_approval__mutmut_41': x__guard_reviewer_approval__mutmut_41, 
    'x__guard_reviewer_approval__mutmut_42': x__guard_reviewer_approval__mutmut_42, 
    'x__guard_reviewer_approval__mutmut_43': x__guard_reviewer_approval__mutmut_43, 
    'x__guard_reviewer_approval__mutmut_44': x__guard_reviewer_approval__mutmut_44, 
    'x__guard_reviewer_approval__mutmut_45': x__guard_reviewer_approval__mutmut_45, 
    'x__guard_reviewer_approval__mutmut_46': x__guard_reviewer_approval__mutmut_46, 
    'x__guard_reviewer_approval__mutmut_47': x__guard_reviewer_approval__mutmut_47, 
    'x__guard_reviewer_approval__mutmut_48': x__guard_reviewer_approval__mutmut_48, 
    'x__guard_reviewer_approval__mutmut_49': x__guard_reviewer_approval__mutmut_49, 
    'x__guard_reviewer_approval__mutmut_50': x__guard_reviewer_approval__mutmut_50, 
    'x__guard_reviewer_approval__mutmut_51': x__guard_reviewer_approval__mutmut_51, 
    'x__guard_reviewer_approval__mutmut_52': x__guard_reviewer_approval__mutmut_52, 
    'x__guard_reviewer_approval__mutmut_53': x__guard_reviewer_approval__mutmut_53, 
    'x__guard_reviewer_approval__mutmut_54': x__guard_reviewer_approval__mutmut_54
}
x__guard_reviewer_approval__mutmut_orig.__name__ = 'x__guard_reviewer_approval'


def _guard_review_ref_required(
    review_ref: str | None,
) -> tuple[bool, str | None]:
    args = [review_ref]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__guard_review_ref_required__mutmut_orig, x__guard_review_ref_required__mutmut_mutants, args, kwargs, None)


def x__guard_review_ref_required__mutmut_orig(
    review_ref: str | None,
) -> tuple[bool, str | None]:
    """Guard: for_review -> in_progress/planned requires review feedback reference."""
    if not review_ref or not review_ref.strip():
        return (
            False,
            "Transition from for_review requires review_ref "
            "(review feedback reference)",
        )
    return True, None


def x__guard_review_ref_required__mutmut_1(
    review_ref: str | None,
) -> tuple[bool, str | None]:
    """Guard: for_review -> in_progress/planned requires review feedback reference."""
    if not review_ref and not review_ref.strip():
        return (
            False,
            "Transition from for_review requires review_ref "
            "(review feedback reference)",
        )
    return True, None


def x__guard_review_ref_required__mutmut_2(
    review_ref: str | None,
) -> tuple[bool, str | None]:
    """Guard: for_review -> in_progress/planned requires review feedback reference."""
    if review_ref or not review_ref.strip():
        return (
            False,
            "Transition from for_review requires review_ref "
            "(review feedback reference)",
        )
    return True, None


def x__guard_review_ref_required__mutmut_3(
    review_ref: str | None,
) -> tuple[bool, str | None]:
    """Guard: for_review -> in_progress/planned requires review feedback reference."""
    if not review_ref or review_ref.strip():
        return (
            False,
            "Transition from for_review requires review_ref "
            "(review feedback reference)",
        )
    return True, None


def x__guard_review_ref_required__mutmut_4(
    review_ref: str | None,
) -> tuple[bool, str | None]:
    """Guard: for_review -> in_progress/planned requires review feedback reference."""
    if not review_ref or not review_ref.strip():
        return (
            True,
            "Transition from for_review requires review_ref "
            "(review feedback reference)",
        )
    return True, None


def x__guard_review_ref_required__mutmut_5(
    review_ref: str | None,
) -> tuple[bool, str | None]:
    """Guard: for_review -> in_progress/planned requires review feedback reference."""
    if not review_ref or not review_ref.strip():
        return (
            False,
            "XXTransition from for_review requires review_ref XX"
            "(review feedback reference)",
        )
    return True, None


def x__guard_review_ref_required__mutmut_6(
    review_ref: str | None,
) -> tuple[bool, str | None]:
    """Guard: for_review -> in_progress/planned requires review feedback reference."""
    if not review_ref or not review_ref.strip():
        return (
            False,
            "transition from for_review requires review_ref "
            "(review feedback reference)",
        )
    return True, None


def x__guard_review_ref_required__mutmut_7(
    review_ref: str | None,
) -> tuple[bool, str | None]:
    """Guard: for_review -> in_progress/planned requires review feedback reference."""
    if not review_ref or not review_ref.strip():
        return (
            False,
            "TRANSITION FROM FOR_REVIEW REQUIRES REVIEW_REF "
            "(review feedback reference)",
        )
    return True, None


def x__guard_review_ref_required__mutmut_8(
    review_ref: str | None,
) -> tuple[bool, str | None]:
    """Guard: for_review -> in_progress/planned requires review feedback reference."""
    if not review_ref or not review_ref.strip():
        return (
            False,
            "Transition from for_review requires review_ref "
            "XX(review feedback reference)XX",
        )
    return True, None


def x__guard_review_ref_required__mutmut_9(
    review_ref: str | None,
) -> tuple[bool, str | None]:
    """Guard: for_review -> in_progress/planned requires review feedback reference."""
    if not review_ref or not review_ref.strip():
        return (
            False,
            "Transition from for_review requires review_ref "
            "(REVIEW FEEDBACK REFERENCE)",
        )
    return True, None


def x__guard_review_ref_required__mutmut_10(
    review_ref: str | None,
) -> tuple[bool, str | None]:
    """Guard: for_review -> in_progress/planned requires review feedback reference."""
    if not review_ref or not review_ref.strip():
        return (
            False,
            "Transition from for_review requires review_ref "
            "(review feedback reference)",
        )
    return False, None

x__guard_review_ref_required__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__guard_review_ref_required__mutmut_1': x__guard_review_ref_required__mutmut_1, 
    'x__guard_review_ref_required__mutmut_2': x__guard_review_ref_required__mutmut_2, 
    'x__guard_review_ref_required__mutmut_3': x__guard_review_ref_required__mutmut_3, 
    'x__guard_review_ref_required__mutmut_4': x__guard_review_ref_required__mutmut_4, 
    'x__guard_review_ref_required__mutmut_5': x__guard_review_ref_required__mutmut_5, 
    'x__guard_review_ref_required__mutmut_6': x__guard_review_ref_required__mutmut_6, 
    'x__guard_review_ref_required__mutmut_7': x__guard_review_ref_required__mutmut_7, 
    'x__guard_review_ref_required__mutmut_8': x__guard_review_ref_required__mutmut_8, 
    'x__guard_review_ref_required__mutmut_9': x__guard_review_ref_required__mutmut_9, 
    'x__guard_review_ref_required__mutmut_10': x__guard_review_ref_required__mutmut_10
}
x__guard_review_ref_required__mutmut_orig.__name__ = 'x__guard_review_ref_required'


def _guard_reason_required(
    reason: str | None,
) -> tuple[bool, str | None]:
    args = [reason]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__guard_reason_required__mutmut_orig, x__guard_reason_required__mutmut_mutants, args, kwargs, None)


def x__guard_reason_required__mutmut_orig(
    reason: str | None,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> planned requires a reason."""
    if not reason or not reason.strip():
        return (
            False,
            "Transition in_progress -> planned requires reason",
        )
    return True, None


def x__guard_reason_required__mutmut_1(
    reason: str | None,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> planned requires a reason."""
    if not reason and not reason.strip():
        return (
            False,
            "Transition in_progress -> planned requires reason",
        )
    return True, None


def x__guard_reason_required__mutmut_2(
    reason: str | None,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> planned requires a reason."""
    if reason or not reason.strip():
        return (
            False,
            "Transition in_progress -> planned requires reason",
        )
    return True, None


def x__guard_reason_required__mutmut_3(
    reason: str | None,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> planned requires a reason."""
    if not reason or reason.strip():
        return (
            False,
            "Transition in_progress -> planned requires reason",
        )
    return True, None


def x__guard_reason_required__mutmut_4(
    reason: str | None,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> planned requires a reason."""
    if not reason or not reason.strip():
        return (
            True,
            "Transition in_progress -> planned requires reason",
        )
    return True, None


def x__guard_reason_required__mutmut_5(
    reason: str | None,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> planned requires a reason."""
    if not reason or not reason.strip():
        return (
            False,
            "XXTransition in_progress -> planned requires reasonXX",
        )
    return True, None


def x__guard_reason_required__mutmut_6(
    reason: str | None,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> planned requires a reason."""
    if not reason or not reason.strip():
        return (
            False,
            "transition in_progress -> planned requires reason",
        )
    return True, None


def x__guard_reason_required__mutmut_7(
    reason: str | None,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> planned requires a reason."""
    if not reason or not reason.strip():
        return (
            False,
            "TRANSITION IN_PROGRESS -> PLANNED REQUIRES REASON",
        )
    return True, None


def x__guard_reason_required__mutmut_8(
    reason: str | None,
) -> tuple[bool, str | None]:
    """Guard: in_progress -> planned requires a reason."""
    if not reason or not reason.strip():
        return (
            False,
            "Transition in_progress -> planned requires reason",
        )
    return False, None

x__guard_reason_required__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__guard_reason_required__mutmut_1': x__guard_reason_required__mutmut_1, 
    'x__guard_reason_required__mutmut_2': x__guard_reason_required__mutmut_2, 
    'x__guard_reason_required__mutmut_3': x__guard_reason_required__mutmut_3, 
    'x__guard_reason_required__mutmut_4': x__guard_reason_required__mutmut_4, 
    'x__guard_reason_required__mutmut_5': x__guard_reason_required__mutmut_5, 
    'x__guard_reason_required__mutmut_6': x__guard_reason_required__mutmut_6, 
    'x__guard_reason_required__mutmut_7': x__guard_reason_required__mutmut_7, 
    'x__guard_reason_required__mutmut_8': x__guard_reason_required__mutmut_8
}
x__guard_reason_required__mutmut_orig.__name__ = 'x__guard_reason_required'


def _run_guard(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    args = [from_lane, to_lane]# type: ignore
    kwargs = {'actor': actor, 'workspace_context': workspace_context, 'subtasks_complete': subtasks_complete, 'implementation_evidence_present': implementation_evidence_present, 'reason': reason, 'review_ref': review_ref, 'evidence': evidence, 'force': force}# type: ignore
    return _mutmut_trampoline(x__run_guard__mutmut_orig, x__run_guard__mutmut_mutants, args, kwargs, None)


def x__run_guard__mutmut_orig(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_1(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = None
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_2(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get(None)
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_3(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is not None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_4(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return False, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_5(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name != "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_6(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "XXactor_requiredXX":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_7(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "ACTOR_REQUIRED":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_8(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(None)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_9(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name != "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_10(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "XXworkspace_contextXX":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_11(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "WORKSPACE_CONTEXT":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_12(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(None)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_13(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name != "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_14(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "XXsubtasks_complete_or_forceXX":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_15(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "SUBTASKS_COMPLETE_OR_FORCE":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_16(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            None,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_17(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            None,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_18(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            None,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_19(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_20(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_21(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_22(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name != "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_23(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "XXreviewer_approvalXX":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_24(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "REVIEWER_APPROVAL":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_25(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(None)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_26(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name != "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_27(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "XXreview_ref_requiredXX":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_28(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "REVIEW_REF_REQUIRED":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_29(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(None)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_30(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name != "reason_required":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_31(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "XXreason_requiredXX":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_32(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "REASON_REQUIRED":
        return _guard_reason_required(reason)

    return True, None


def x__run_guard__mutmut_33(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(None)

    return True, None


def x__run_guard__mutmut_34(
    from_lane: str,
    to_lane: str,
    *,
    actor: str | None,
    workspace_context: str | None,
    subtasks_complete: bool | None,
    implementation_evidence_present: bool | None,
    reason: str | None,
    review_ref: str | None,
    evidence: Any,
    force: bool,
) -> tuple[bool, str | None]:
    """Run the guard condition for a specific transition, if any."""
    guard_name = _GUARDED_TRANSITIONS.get((from_lane, to_lane))
    if guard_name is None:
        return True, None

    if guard_name == "actor_required":
        return _guard_actor_required(actor)
    elif guard_name == "workspace_context":
        return _guard_workspace_context(workspace_context)
    elif guard_name == "subtasks_complete_or_force":
        return _guard_subtasks_complete_or_force(
            subtasks_complete,
            implementation_evidence_present,
            force,
        )
    elif guard_name == "reviewer_approval":
        return _guard_reviewer_approval(evidence)
    elif guard_name == "review_ref_required":
        return _guard_review_ref_required(review_ref)
    elif guard_name == "reason_required":
        return _guard_reason_required(reason)

    return False, None

x__run_guard__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__run_guard__mutmut_1': x__run_guard__mutmut_1, 
    'x__run_guard__mutmut_2': x__run_guard__mutmut_2, 
    'x__run_guard__mutmut_3': x__run_guard__mutmut_3, 
    'x__run_guard__mutmut_4': x__run_guard__mutmut_4, 
    'x__run_guard__mutmut_5': x__run_guard__mutmut_5, 
    'x__run_guard__mutmut_6': x__run_guard__mutmut_6, 
    'x__run_guard__mutmut_7': x__run_guard__mutmut_7, 
    'x__run_guard__mutmut_8': x__run_guard__mutmut_8, 
    'x__run_guard__mutmut_9': x__run_guard__mutmut_9, 
    'x__run_guard__mutmut_10': x__run_guard__mutmut_10, 
    'x__run_guard__mutmut_11': x__run_guard__mutmut_11, 
    'x__run_guard__mutmut_12': x__run_guard__mutmut_12, 
    'x__run_guard__mutmut_13': x__run_guard__mutmut_13, 
    'x__run_guard__mutmut_14': x__run_guard__mutmut_14, 
    'x__run_guard__mutmut_15': x__run_guard__mutmut_15, 
    'x__run_guard__mutmut_16': x__run_guard__mutmut_16, 
    'x__run_guard__mutmut_17': x__run_guard__mutmut_17, 
    'x__run_guard__mutmut_18': x__run_guard__mutmut_18, 
    'x__run_guard__mutmut_19': x__run_guard__mutmut_19, 
    'x__run_guard__mutmut_20': x__run_guard__mutmut_20, 
    'x__run_guard__mutmut_21': x__run_guard__mutmut_21, 
    'x__run_guard__mutmut_22': x__run_guard__mutmut_22, 
    'x__run_guard__mutmut_23': x__run_guard__mutmut_23, 
    'x__run_guard__mutmut_24': x__run_guard__mutmut_24, 
    'x__run_guard__mutmut_25': x__run_guard__mutmut_25, 
    'x__run_guard__mutmut_26': x__run_guard__mutmut_26, 
    'x__run_guard__mutmut_27': x__run_guard__mutmut_27, 
    'x__run_guard__mutmut_28': x__run_guard__mutmut_28, 
    'x__run_guard__mutmut_29': x__run_guard__mutmut_29, 
    'x__run_guard__mutmut_30': x__run_guard__mutmut_30, 
    'x__run_guard__mutmut_31': x__run_guard__mutmut_31, 
    'x__run_guard__mutmut_32': x__run_guard__mutmut_32, 
    'x__run_guard__mutmut_33': x__run_guard__mutmut_33, 
    'x__run_guard__mutmut_34': x__run_guard__mutmut_34
}
x__run_guard__mutmut_orig.__name__ = 'x__run_guard'


def validate_transition(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    args = [from_lane, to_lane]# type: ignore
    kwargs = {'force': force, 'actor': actor, 'workspace_context': workspace_context, 'subtasks_complete': subtasks_complete, 'implementation_evidence_present': implementation_evidence_present, 'reason': reason, 'review_ref': review_ref, 'evidence': evidence}# type: ignore
    return _mutmut_trampoline(x_validate_transition__mutmut_orig, x_validate_transition__mutmut_mutants, args, kwargs, None)


def x_validate_transition__mutmut_orig(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_1(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = True,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_2(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = None
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_3(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(None)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_4(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = None

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_5(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(None)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_6(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(None)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_7(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return True, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_8(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(None)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_9(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return True, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_10(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = None

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_11(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_12(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor and not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_13(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_14(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_15(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    True,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_16(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "XXForce transitions require actor and reasonXX",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_17(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_18(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "FORCE TRANSITIONS REQUIRE ACTOR AND REASON",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_19(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason and not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_20(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_21(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_22(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    True,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_23(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "XXForce transitions require actor and reasonXX",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_24(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_25(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "FORCE TRANSITIONS REQUIRE ACTOR AND REASON",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_26(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return False, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_27(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            True,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_28(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor and not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_29(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_30(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_31(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return True, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_32(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "XXForce transitions require actor and reasonXX"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_33(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_34(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "FORCE TRANSITIONS REQUIRE ACTOR AND REASON"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_35(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason and not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_36(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_37(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_38(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return True, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_39(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "XXForce transitions require actor and reasonXX"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_40(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_41(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "FORCE TRANSITIONS REQUIRE ACTOR AND REASON"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_42(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return False, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_43(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        None,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_44(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        None,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_45(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=None,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_46(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=None,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_47(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=None,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_48(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=None,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_49(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=None,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_50(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=None,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_51(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=None,
        force=force,
    )


def x_validate_transition__mutmut_52(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=None,
    )


def x_validate_transition__mutmut_53(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_54(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_55(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_56(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_57(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_58(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_59(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        review_ref=review_ref,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_60(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        evidence=evidence,
        force=force,
    )


def x_validate_transition__mutmut_61(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        force=force,
    )


def x_validate_transition__mutmut_62(
    from_lane: str,
    to_lane: str,
    *,
    force: bool = False,
    actor: str | None = None,
    workspace_context: str | None = None,
    subtasks_complete: bool | None = None,
    implementation_evidence_present: bool | None = None,
    reason: str | None = None,
    review_ref: str | None = None,
    evidence: Any = None,
) -> tuple[bool, str | None]:
    """Validate a lane transition. Returns (ok, error_message).

    Resolves aliases, checks the transition matrix, runs guard conditions,
    and validates force-override requirements.
    """
    resolved_from = resolve_lane_alias(from_lane)
    resolved_to = resolve_lane_alias(to_lane)

    # Validate that resolved lanes are canonical
    try:
        Lane(resolved_from)
    except ValueError:
        return False, f"Unknown lane: {from_lane}"
    try:
        Lane(resolved_to)
    except ValueError:
        return False, f"Unknown lane: {to_lane}"

    pair = (resolved_from, resolved_to)

    if pair not in ALLOWED_TRANSITIONS:
        if force:
            # Force can override any transition, but requires actor + reason
            if not actor or not actor.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            if not reason or not reason.strip():
                return (
                    False,
                    "Force transitions require actor and reason",
                )
            return True, None
        return (
            False,
            f"Illegal transition: {resolved_from} -> {resolved_to}",
        )

    # For allowed transitions, run guard conditions
    # Force bypasses guards (but force still requires actor + reason for audit)
    if force:
        if not actor or not actor.strip():
            return False, "Force transitions require actor and reason"
        if not reason or not reason.strip():
            return False, "Force transitions require actor and reason"
        return True, None

    return _run_guard(
        resolved_from,
        resolved_to,
        actor=actor,
        workspace_context=workspace_context,
        subtasks_complete=subtasks_complete,
        implementation_evidence_present=implementation_evidence_present,
        reason=reason,
        review_ref=review_ref,
        evidence=evidence,
        )

x_validate_transition__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_validate_transition__mutmut_1': x_validate_transition__mutmut_1, 
    'x_validate_transition__mutmut_2': x_validate_transition__mutmut_2, 
    'x_validate_transition__mutmut_3': x_validate_transition__mutmut_3, 
    'x_validate_transition__mutmut_4': x_validate_transition__mutmut_4, 
    'x_validate_transition__mutmut_5': x_validate_transition__mutmut_5, 
    'x_validate_transition__mutmut_6': x_validate_transition__mutmut_6, 
    'x_validate_transition__mutmut_7': x_validate_transition__mutmut_7, 
    'x_validate_transition__mutmut_8': x_validate_transition__mutmut_8, 
    'x_validate_transition__mutmut_9': x_validate_transition__mutmut_9, 
    'x_validate_transition__mutmut_10': x_validate_transition__mutmut_10, 
    'x_validate_transition__mutmut_11': x_validate_transition__mutmut_11, 
    'x_validate_transition__mutmut_12': x_validate_transition__mutmut_12, 
    'x_validate_transition__mutmut_13': x_validate_transition__mutmut_13, 
    'x_validate_transition__mutmut_14': x_validate_transition__mutmut_14, 
    'x_validate_transition__mutmut_15': x_validate_transition__mutmut_15, 
    'x_validate_transition__mutmut_16': x_validate_transition__mutmut_16, 
    'x_validate_transition__mutmut_17': x_validate_transition__mutmut_17, 
    'x_validate_transition__mutmut_18': x_validate_transition__mutmut_18, 
    'x_validate_transition__mutmut_19': x_validate_transition__mutmut_19, 
    'x_validate_transition__mutmut_20': x_validate_transition__mutmut_20, 
    'x_validate_transition__mutmut_21': x_validate_transition__mutmut_21, 
    'x_validate_transition__mutmut_22': x_validate_transition__mutmut_22, 
    'x_validate_transition__mutmut_23': x_validate_transition__mutmut_23, 
    'x_validate_transition__mutmut_24': x_validate_transition__mutmut_24, 
    'x_validate_transition__mutmut_25': x_validate_transition__mutmut_25, 
    'x_validate_transition__mutmut_26': x_validate_transition__mutmut_26, 
    'x_validate_transition__mutmut_27': x_validate_transition__mutmut_27, 
    'x_validate_transition__mutmut_28': x_validate_transition__mutmut_28, 
    'x_validate_transition__mutmut_29': x_validate_transition__mutmut_29, 
    'x_validate_transition__mutmut_30': x_validate_transition__mutmut_30, 
    'x_validate_transition__mutmut_31': x_validate_transition__mutmut_31, 
    'x_validate_transition__mutmut_32': x_validate_transition__mutmut_32, 
    'x_validate_transition__mutmut_33': x_validate_transition__mutmut_33, 
    'x_validate_transition__mutmut_34': x_validate_transition__mutmut_34, 
    'x_validate_transition__mutmut_35': x_validate_transition__mutmut_35, 
    'x_validate_transition__mutmut_36': x_validate_transition__mutmut_36, 
    'x_validate_transition__mutmut_37': x_validate_transition__mutmut_37, 
    'x_validate_transition__mutmut_38': x_validate_transition__mutmut_38, 
    'x_validate_transition__mutmut_39': x_validate_transition__mutmut_39, 
    'x_validate_transition__mutmut_40': x_validate_transition__mutmut_40, 
    'x_validate_transition__mutmut_41': x_validate_transition__mutmut_41, 
    'x_validate_transition__mutmut_42': x_validate_transition__mutmut_42, 
    'x_validate_transition__mutmut_43': x_validate_transition__mutmut_43, 
    'x_validate_transition__mutmut_44': x_validate_transition__mutmut_44, 
    'x_validate_transition__mutmut_45': x_validate_transition__mutmut_45, 
    'x_validate_transition__mutmut_46': x_validate_transition__mutmut_46, 
    'x_validate_transition__mutmut_47': x_validate_transition__mutmut_47, 
    'x_validate_transition__mutmut_48': x_validate_transition__mutmut_48, 
    'x_validate_transition__mutmut_49': x_validate_transition__mutmut_49, 
    'x_validate_transition__mutmut_50': x_validate_transition__mutmut_50, 
    'x_validate_transition__mutmut_51': x_validate_transition__mutmut_51, 
    'x_validate_transition__mutmut_52': x_validate_transition__mutmut_52, 
    'x_validate_transition__mutmut_53': x_validate_transition__mutmut_53, 
    'x_validate_transition__mutmut_54': x_validate_transition__mutmut_54, 
    'x_validate_transition__mutmut_55': x_validate_transition__mutmut_55, 
    'x_validate_transition__mutmut_56': x_validate_transition__mutmut_56, 
    'x_validate_transition__mutmut_57': x_validate_transition__mutmut_57, 
    'x_validate_transition__mutmut_58': x_validate_transition__mutmut_58, 
    'x_validate_transition__mutmut_59': x_validate_transition__mutmut_59, 
    'x_validate_transition__mutmut_60': x_validate_transition__mutmut_60, 
    'x_validate_transition__mutmut_61': x_validate_transition__mutmut_61, 
    'x_validate_transition__mutmut_62': x_validate_transition__mutmut_62
}
x_validate_transition__mutmut_orig.__name__ = 'x_validate_transition'
