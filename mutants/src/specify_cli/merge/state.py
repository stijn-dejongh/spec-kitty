"""Merge state persistence for resume capability.

Implements FR-021 through FR-024: persisting merge state to enable
resuming interrupted merge operations.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

__all__ = [
    "MergeState",
    "save_state",
    "load_state",
    "clear_state",
    "has_active_merge",
    "get_state_path",
    "detect_git_merge_state",
]

STATE_FILE = ".kittify/merge-state.json"
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
class MergeState:
    """Persisted state for resumable merge operations."""

    feature_slug: str
    target_branch: str
    wp_order: list[str]  # Ordered list of WP IDs to merge
    completed_wps: list[str] = field(default_factory=list)
    current_wp: str | None = None
    has_pending_conflicts: bool = False
    strategy: str = "merge"  # "merge", "squash", "rebase"
    started_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MergeState:
        """Create from dict (loaded JSON)."""
        return cls(**data)

    @property
    def remaining_wps(self) -> list[str]:
        """WPs not yet merged."""
        completed_set = set(self.completed_wps)
        return [wp for wp in self.wp_order if wp not in completed_set]

    @property
    def progress_percent(self) -> float:
        """Completion percentage."""
        if not self.wp_order:
            return 0.0
        return len(self.completed_wps) / len(self.wp_order) * 100

    def mark_wp_complete(self, wp_id: str) -> None:
        """Mark a WP as successfully merged."""
        if wp_id not in self.completed_wps:
            self.completed_wps.append(wp_id)
        self.current_wp = None
        self.has_pending_conflicts = False
        self.updated_at = datetime.now(UTC).isoformat()

    def set_current_wp(self, wp_id: str) -> None:
        """Set the currently-merging WP."""
        self.current_wp = wp_id
        self.updated_at = datetime.now(UTC).isoformat()

    def set_pending_conflicts(self, has_conflicts: bool = True) -> None:
        """Mark that there are pending conflicts to resolve."""
        self.has_pending_conflicts = has_conflicts
        self.updated_at = datetime.now(UTC).isoformat()


def get_state_path(repo_root: Path) -> Path:
    args = [repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_state_path__mutmut_orig, x_get_state_path__mutmut_mutants, args, kwargs, None)


def x_get_state_path__mutmut_orig(repo_root: Path) -> Path:
    """Get path to merge state file."""
    return repo_root / STATE_FILE


def x_get_state_path__mutmut_1(repo_root: Path) -> Path:
    """Get path to merge state file."""
    return repo_root * STATE_FILE

x_get_state_path__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_state_path__mutmut_1': x_get_state_path__mutmut_1
}
x_get_state_path__mutmut_orig.__name__ = 'x_get_state_path'


def save_state(state: MergeState, repo_root: Path) -> None:
    args = [state, repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_save_state__mutmut_orig, x_save_state__mutmut_mutants, args, kwargs, None)


def x_save_state__mutmut_orig(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_1(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = None
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_2(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(None)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_3(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=None, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_4(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=None)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_5(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_6(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, )

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_7(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=False, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_8(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=False)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_9(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = None

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_10(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(None).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_11(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(None, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_12(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, None, encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_13(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding=None) as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_14(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open("w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_15(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_16(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", ) as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_17(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "XXwXX", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_18(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "W", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_19(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="XXutf-8XX") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_20(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="UTF-8") as f:
        json.dump(state.to_dict(), f, indent=2)


def x_save_state__mutmut_21(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(None, f, indent=2)


def x_save_state__mutmut_22(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), None, indent=2)


def x_save_state__mutmut_23(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=None)


def x_save_state__mutmut_24(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(f, indent=2)


def x_save_state__mutmut_25(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), indent=2)


def x_save_state__mutmut_26(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, )


def x_save_state__mutmut_27(state: MergeState, repo_root: Path) -> None:
    """Save merge state to JSON file.

    Args:
        state: MergeState to persist
        repo_root: Repository root path
    """
    state_path = get_state_path(repo_root)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    state.updated_at = datetime.now(UTC).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=3)

x_save_state__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_save_state__mutmut_1': x_save_state__mutmut_1, 
    'x_save_state__mutmut_2': x_save_state__mutmut_2, 
    'x_save_state__mutmut_3': x_save_state__mutmut_3, 
    'x_save_state__mutmut_4': x_save_state__mutmut_4, 
    'x_save_state__mutmut_5': x_save_state__mutmut_5, 
    'x_save_state__mutmut_6': x_save_state__mutmut_6, 
    'x_save_state__mutmut_7': x_save_state__mutmut_7, 
    'x_save_state__mutmut_8': x_save_state__mutmut_8, 
    'x_save_state__mutmut_9': x_save_state__mutmut_9, 
    'x_save_state__mutmut_10': x_save_state__mutmut_10, 
    'x_save_state__mutmut_11': x_save_state__mutmut_11, 
    'x_save_state__mutmut_12': x_save_state__mutmut_12, 
    'x_save_state__mutmut_13': x_save_state__mutmut_13, 
    'x_save_state__mutmut_14': x_save_state__mutmut_14, 
    'x_save_state__mutmut_15': x_save_state__mutmut_15, 
    'x_save_state__mutmut_16': x_save_state__mutmut_16, 
    'x_save_state__mutmut_17': x_save_state__mutmut_17, 
    'x_save_state__mutmut_18': x_save_state__mutmut_18, 
    'x_save_state__mutmut_19': x_save_state__mutmut_19, 
    'x_save_state__mutmut_20': x_save_state__mutmut_20, 
    'x_save_state__mutmut_21': x_save_state__mutmut_21, 
    'x_save_state__mutmut_22': x_save_state__mutmut_22, 
    'x_save_state__mutmut_23': x_save_state__mutmut_23, 
    'x_save_state__mutmut_24': x_save_state__mutmut_24, 
    'x_save_state__mutmut_25': x_save_state__mutmut_25, 
    'x_save_state__mutmut_26': x_save_state__mutmut_26, 
    'x_save_state__mutmut_27': x_save_state__mutmut_27
}
x_save_state__mutmut_orig.__name__ = 'x_save_state'


def load_state(repo_root: Path) -> MergeState | None:
    args = [repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_load_state__mutmut_orig, x_load_state__mutmut_mutants, args, kwargs, None)


def x_load_state__mutmut_orig(repo_root: Path) -> MergeState | None:
    """Load merge state from JSON file.

    Args:
        repo_root: Repository root path

    Returns:
        MergeState if file exists and is valid, None otherwise
    """
    state_path = get_state_path(repo_root)

    if not state_path.exists():
        return None

    try:
        with open(state_path, encoding="utf-8") as f:
            data = json.load(f)
        return MergeState.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError):
        # Invalid state file - return None, caller should clear
        return None


def x_load_state__mutmut_1(repo_root: Path) -> MergeState | None:
    """Load merge state from JSON file.

    Args:
        repo_root: Repository root path

    Returns:
        MergeState if file exists and is valid, None otherwise
    """
    state_path = None

    if not state_path.exists():
        return None

    try:
        with open(state_path, encoding="utf-8") as f:
            data = json.load(f)
        return MergeState.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError):
        # Invalid state file - return None, caller should clear
        return None


def x_load_state__mutmut_2(repo_root: Path) -> MergeState | None:
    """Load merge state from JSON file.

    Args:
        repo_root: Repository root path

    Returns:
        MergeState if file exists and is valid, None otherwise
    """
    state_path = get_state_path(None)

    if not state_path.exists():
        return None

    try:
        with open(state_path, encoding="utf-8") as f:
            data = json.load(f)
        return MergeState.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError):
        # Invalid state file - return None, caller should clear
        return None


def x_load_state__mutmut_3(repo_root: Path) -> MergeState | None:
    """Load merge state from JSON file.

    Args:
        repo_root: Repository root path

    Returns:
        MergeState if file exists and is valid, None otherwise
    """
    state_path = get_state_path(repo_root)

    if state_path.exists():
        return None

    try:
        with open(state_path, encoding="utf-8") as f:
            data = json.load(f)
        return MergeState.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError):
        # Invalid state file - return None, caller should clear
        return None


def x_load_state__mutmut_4(repo_root: Path) -> MergeState | None:
    """Load merge state from JSON file.

    Args:
        repo_root: Repository root path

    Returns:
        MergeState if file exists and is valid, None otherwise
    """
    state_path = get_state_path(repo_root)

    if not state_path.exists():
        return None

    try:
        with open(None, encoding="utf-8") as f:
            data = json.load(f)
        return MergeState.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError):
        # Invalid state file - return None, caller should clear
        return None


def x_load_state__mutmut_5(repo_root: Path) -> MergeState | None:
    """Load merge state from JSON file.

    Args:
        repo_root: Repository root path

    Returns:
        MergeState if file exists and is valid, None otherwise
    """
    state_path = get_state_path(repo_root)

    if not state_path.exists():
        return None

    try:
        with open(state_path, encoding=None) as f:
            data = json.load(f)
        return MergeState.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError):
        # Invalid state file - return None, caller should clear
        return None


def x_load_state__mutmut_6(repo_root: Path) -> MergeState | None:
    """Load merge state from JSON file.

    Args:
        repo_root: Repository root path

    Returns:
        MergeState if file exists and is valid, None otherwise
    """
    state_path = get_state_path(repo_root)

    if not state_path.exists():
        return None

    try:
        with open(encoding="utf-8") as f:
            data = json.load(f)
        return MergeState.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError):
        # Invalid state file - return None, caller should clear
        return None


def x_load_state__mutmut_7(repo_root: Path) -> MergeState | None:
    """Load merge state from JSON file.

    Args:
        repo_root: Repository root path

    Returns:
        MergeState if file exists and is valid, None otherwise
    """
    state_path = get_state_path(repo_root)

    if not state_path.exists():
        return None

    try:
        with open(state_path, ) as f:
            data = json.load(f)
        return MergeState.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError):
        # Invalid state file - return None, caller should clear
        return None


def x_load_state__mutmut_8(repo_root: Path) -> MergeState | None:
    """Load merge state from JSON file.

    Args:
        repo_root: Repository root path

    Returns:
        MergeState if file exists and is valid, None otherwise
    """
    state_path = get_state_path(repo_root)

    if not state_path.exists():
        return None

    try:
        with open(state_path, encoding="XXutf-8XX") as f:
            data = json.load(f)
        return MergeState.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError):
        # Invalid state file - return None, caller should clear
        return None


def x_load_state__mutmut_9(repo_root: Path) -> MergeState | None:
    """Load merge state from JSON file.

    Args:
        repo_root: Repository root path

    Returns:
        MergeState if file exists and is valid, None otherwise
    """
    state_path = get_state_path(repo_root)

    if not state_path.exists():
        return None

    try:
        with open(state_path, encoding="UTF-8") as f:
            data = json.load(f)
        return MergeState.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError):
        # Invalid state file - return None, caller should clear
        return None


def x_load_state__mutmut_10(repo_root: Path) -> MergeState | None:
    """Load merge state from JSON file.

    Args:
        repo_root: Repository root path

    Returns:
        MergeState if file exists and is valid, None otherwise
    """
    state_path = get_state_path(repo_root)

    if not state_path.exists():
        return None

    try:
        with open(state_path, encoding="utf-8") as f:
            data = None
        return MergeState.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError):
        # Invalid state file - return None, caller should clear
        return None


def x_load_state__mutmut_11(repo_root: Path) -> MergeState | None:
    """Load merge state from JSON file.

    Args:
        repo_root: Repository root path

    Returns:
        MergeState if file exists and is valid, None otherwise
    """
    state_path = get_state_path(repo_root)

    if not state_path.exists():
        return None

    try:
        with open(state_path, encoding="utf-8") as f:
            data = json.load(None)
        return MergeState.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError):
        # Invalid state file - return None, caller should clear
        return None


def x_load_state__mutmut_12(repo_root: Path) -> MergeState | None:
    """Load merge state from JSON file.

    Args:
        repo_root: Repository root path

    Returns:
        MergeState if file exists and is valid, None otherwise
    """
    state_path = get_state_path(repo_root)

    if not state_path.exists():
        return None

    try:
        with open(state_path, encoding="utf-8") as f:
            data = json.load(f)
        return MergeState.from_dict(None)
    except (json.JSONDecodeError, TypeError, KeyError):
        # Invalid state file - return None, caller should clear
        return None

x_load_state__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_load_state__mutmut_1': x_load_state__mutmut_1, 
    'x_load_state__mutmut_2': x_load_state__mutmut_2, 
    'x_load_state__mutmut_3': x_load_state__mutmut_3, 
    'x_load_state__mutmut_4': x_load_state__mutmut_4, 
    'x_load_state__mutmut_5': x_load_state__mutmut_5, 
    'x_load_state__mutmut_6': x_load_state__mutmut_6, 
    'x_load_state__mutmut_7': x_load_state__mutmut_7, 
    'x_load_state__mutmut_8': x_load_state__mutmut_8, 
    'x_load_state__mutmut_9': x_load_state__mutmut_9, 
    'x_load_state__mutmut_10': x_load_state__mutmut_10, 
    'x_load_state__mutmut_11': x_load_state__mutmut_11, 
    'x_load_state__mutmut_12': x_load_state__mutmut_12
}
x_load_state__mutmut_orig.__name__ = 'x_load_state'


def clear_state(repo_root: Path) -> bool:
    args = [repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_clear_state__mutmut_orig, x_clear_state__mutmut_mutants, args, kwargs, None)


def x_clear_state__mutmut_orig(repo_root: Path) -> bool:
    """Remove merge state file.

    Args:
        repo_root: Repository root path

    Returns:
        True if file was removed, False if it didn't exist
    """
    state_path = get_state_path(repo_root)

    if state_path.exists():
        state_path.unlink()
        return True
    return False


def x_clear_state__mutmut_1(repo_root: Path) -> bool:
    """Remove merge state file.

    Args:
        repo_root: Repository root path

    Returns:
        True if file was removed, False if it didn't exist
    """
    state_path = None

    if state_path.exists():
        state_path.unlink()
        return True
    return False


def x_clear_state__mutmut_2(repo_root: Path) -> bool:
    """Remove merge state file.

    Args:
        repo_root: Repository root path

    Returns:
        True if file was removed, False if it didn't exist
    """
    state_path = get_state_path(None)

    if state_path.exists():
        state_path.unlink()
        return True
    return False


def x_clear_state__mutmut_3(repo_root: Path) -> bool:
    """Remove merge state file.

    Args:
        repo_root: Repository root path

    Returns:
        True if file was removed, False if it didn't exist
    """
    state_path = get_state_path(repo_root)

    if state_path.exists():
        state_path.unlink()
        return False
    return False


def x_clear_state__mutmut_4(repo_root: Path) -> bool:
    """Remove merge state file.

    Args:
        repo_root: Repository root path

    Returns:
        True if file was removed, False if it didn't exist
    """
    state_path = get_state_path(repo_root)

    if state_path.exists():
        state_path.unlink()
        return True
    return True

x_clear_state__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_clear_state__mutmut_1': x_clear_state__mutmut_1, 
    'x_clear_state__mutmut_2': x_clear_state__mutmut_2, 
    'x_clear_state__mutmut_3': x_clear_state__mutmut_3, 
    'x_clear_state__mutmut_4': x_clear_state__mutmut_4
}
x_clear_state__mutmut_orig.__name__ = 'x_clear_state'


def has_active_merge(repo_root: Path) -> bool:
    args = [repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_has_active_merge__mutmut_orig, x_has_active_merge__mutmut_mutants, args, kwargs, None)


def x_has_active_merge__mutmut_orig(repo_root: Path) -> bool:
    """Check if there's an active merge state.

    Returns True if state file exists and has remaining WPs.
    """
    state = load_state(repo_root)
    if state is None:
        return False
    return len(state.remaining_wps) > 0


def x_has_active_merge__mutmut_1(repo_root: Path) -> bool:
    """Check if there's an active merge state.

    Returns True if state file exists and has remaining WPs.
    """
    state = None
    if state is None:
        return False
    return len(state.remaining_wps) > 0


def x_has_active_merge__mutmut_2(repo_root: Path) -> bool:
    """Check if there's an active merge state.

    Returns True if state file exists and has remaining WPs.
    """
    state = load_state(None)
    if state is None:
        return False
    return len(state.remaining_wps) > 0


def x_has_active_merge__mutmut_3(repo_root: Path) -> bool:
    """Check if there's an active merge state.

    Returns True if state file exists and has remaining WPs.
    """
    state = load_state(repo_root)
    if state is not None:
        return False
    return len(state.remaining_wps) > 0


def x_has_active_merge__mutmut_4(repo_root: Path) -> bool:
    """Check if there's an active merge state.

    Returns True if state file exists and has remaining WPs.
    """
    state = load_state(repo_root)
    if state is None:
        return True
    return len(state.remaining_wps) > 0


def x_has_active_merge__mutmut_5(repo_root: Path) -> bool:
    """Check if there's an active merge state.

    Returns True if state file exists and has remaining WPs.
    """
    state = load_state(repo_root)
    if state is None:
        return False
    return len(state.remaining_wps) >= 0


def x_has_active_merge__mutmut_6(repo_root: Path) -> bool:
    """Check if there's an active merge state.

    Returns True if state file exists and has remaining WPs.
    """
    state = load_state(repo_root)
    if state is None:
        return False
    return len(state.remaining_wps) > 1

x_has_active_merge__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_has_active_merge__mutmut_1': x_has_active_merge__mutmut_1, 
    'x_has_active_merge__mutmut_2': x_has_active_merge__mutmut_2, 
    'x_has_active_merge__mutmut_3': x_has_active_merge__mutmut_3, 
    'x_has_active_merge__mutmut_4': x_has_active_merge__mutmut_4, 
    'x_has_active_merge__mutmut_5': x_has_active_merge__mutmut_5, 
    'x_has_active_merge__mutmut_6': x_has_active_merge__mutmut_6
}
x_has_active_merge__mutmut_orig.__name__ = 'x_has_active_merge'


def detect_git_merge_state(repo_root: Path) -> bool:
    args = [repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_detect_git_merge_state__mutmut_orig, x_detect_git_merge_state__mutmut_mutants, args, kwargs, None)


def x_detect_git_merge_state__mutmut_orig(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_1(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = None
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_2(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        None,
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_3(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        cwd=None,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_4(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=None,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_5(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        check=None,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_6(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_7(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_8(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_9(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_10(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["XXgitXX", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_11(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["GIT", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_12(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "XXrev-parseXX", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_13(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "REV-PARSE", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_14(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "XX-qXX", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_15(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-Q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_16(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "XX--verifyXX", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_17(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--VERIFY", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_18(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "XXMERGE_HEADXX"],
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_19(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "merge_head"],
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_20(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(None),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_21(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=False,
        check=False,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_22(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        check=True,
    )
    return result.returncode == 0


def x_detect_git_merge_state__mutmut_23(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode != 0


def x_detect_git_merge_state__mutmut_24(repo_root: Path) -> bool:
    """Check if git has an active merge in progress.

    Uses MERGE_HEAD presence to detect mid-merge state.
    """
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        check=False,
    )
    return result.returncode == 1

x_detect_git_merge_state__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_detect_git_merge_state__mutmut_1': x_detect_git_merge_state__mutmut_1, 
    'x_detect_git_merge_state__mutmut_2': x_detect_git_merge_state__mutmut_2, 
    'x_detect_git_merge_state__mutmut_3': x_detect_git_merge_state__mutmut_3, 
    'x_detect_git_merge_state__mutmut_4': x_detect_git_merge_state__mutmut_4, 
    'x_detect_git_merge_state__mutmut_5': x_detect_git_merge_state__mutmut_5, 
    'x_detect_git_merge_state__mutmut_6': x_detect_git_merge_state__mutmut_6, 
    'x_detect_git_merge_state__mutmut_7': x_detect_git_merge_state__mutmut_7, 
    'x_detect_git_merge_state__mutmut_8': x_detect_git_merge_state__mutmut_8, 
    'x_detect_git_merge_state__mutmut_9': x_detect_git_merge_state__mutmut_9, 
    'x_detect_git_merge_state__mutmut_10': x_detect_git_merge_state__mutmut_10, 
    'x_detect_git_merge_state__mutmut_11': x_detect_git_merge_state__mutmut_11, 
    'x_detect_git_merge_state__mutmut_12': x_detect_git_merge_state__mutmut_12, 
    'x_detect_git_merge_state__mutmut_13': x_detect_git_merge_state__mutmut_13, 
    'x_detect_git_merge_state__mutmut_14': x_detect_git_merge_state__mutmut_14, 
    'x_detect_git_merge_state__mutmut_15': x_detect_git_merge_state__mutmut_15, 
    'x_detect_git_merge_state__mutmut_16': x_detect_git_merge_state__mutmut_16, 
    'x_detect_git_merge_state__mutmut_17': x_detect_git_merge_state__mutmut_17, 
    'x_detect_git_merge_state__mutmut_18': x_detect_git_merge_state__mutmut_18, 
    'x_detect_git_merge_state__mutmut_19': x_detect_git_merge_state__mutmut_19, 
    'x_detect_git_merge_state__mutmut_20': x_detect_git_merge_state__mutmut_20, 
    'x_detect_git_merge_state__mutmut_21': x_detect_git_merge_state__mutmut_21, 
    'x_detect_git_merge_state__mutmut_22': x_detect_git_merge_state__mutmut_22, 
    'x_detect_git_merge_state__mutmut_23': x_detect_git_merge_state__mutmut_23, 
    'x_detect_git_merge_state__mutmut_24': x_detect_git_merge_state__mutmut_24
}
x_detect_git_merge_state__mutmut_orig.__name__ = 'x_detect_git_merge_state'


def abort_git_merge(repo_root: Path) -> bool:
    args = [repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_abort_git_merge__mutmut_orig, x_abort_git_merge__mutmut_mutants, args, kwargs, None)


def x_abort_git_merge__mutmut_orig(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["git", "merge", "--abort"],
        cwd=str(repo_root),
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_1(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["git", "merge", "--abort"],
        cwd=str(repo_root),
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_2(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(None):
        return False

    subprocess.run(
        ["git", "merge", "--abort"],
        cwd=str(repo_root),
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_3(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return True

    subprocess.run(
        ["git", "merge", "--abort"],
        cwd=str(repo_root),
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_4(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        None,
        cwd=str(repo_root),
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_5(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["git", "merge", "--abort"],
        cwd=None,
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_6(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["git", "merge", "--abort"],
        cwd=str(repo_root),
        check=None,
    )
    return True


def x_abort_git_merge__mutmut_7(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        cwd=str(repo_root),
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_8(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["git", "merge", "--abort"],
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_9(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["git", "merge", "--abort"],
        cwd=str(repo_root),
        )
    return True


def x_abort_git_merge__mutmut_10(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["XXgitXX", "merge", "--abort"],
        cwd=str(repo_root),
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_11(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["GIT", "merge", "--abort"],
        cwd=str(repo_root),
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_12(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["git", "XXmergeXX", "--abort"],
        cwd=str(repo_root),
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_13(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["git", "MERGE", "--abort"],
        cwd=str(repo_root),
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_14(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["git", "merge", "XX--abortXX"],
        cwd=str(repo_root),
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_15(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["git", "merge", "--ABORT"],
        cwd=str(repo_root),
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_16(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["git", "merge", "--abort"],
        cwd=str(None),
        check=False,
    )
    return True


def x_abort_git_merge__mutmut_17(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["git", "merge", "--abort"],
        cwd=str(repo_root),
        check=True,
    )
    return True


def x_abort_git_merge__mutmut_18(repo_root: Path) -> bool:
    """Abort an in-progress git merge.

    Returns:
        True if merge was aborted, False if no merge was in progress
    """
    if not detect_git_merge_state(repo_root):
        return False

    subprocess.run(
        ["git", "merge", "--abort"],
        cwd=str(repo_root),
        check=False,
    )
    return False

x_abort_git_merge__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_abort_git_merge__mutmut_1': x_abort_git_merge__mutmut_1, 
    'x_abort_git_merge__mutmut_2': x_abort_git_merge__mutmut_2, 
    'x_abort_git_merge__mutmut_3': x_abort_git_merge__mutmut_3, 
    'x_abort_git_merge__mutmut_4': x_abort_git_merge__mutmut_4, 
    'x_abort_git_merge__mutmut_5': x_abort_git_merge__mutmut_5, 
    'x_abort_git_merge__mutmut_6': x_abort_git_merge__mutmut_6, 
    'x_abort_git_merge__mutmut_7': x_abort_git_merge__mutmut_7, 
    'x_abort_git_merge__mutmut_8': x_abort_git_merge__mutmut_8, 
    'x_abort_git_merge__mutmut_9': x_abort_git_merge__mutmut_9, 
    'x_abort_git_merge__mutmut_10': x_abort_git_merge__mutmut_10, 
    'x_abort_git_merge__mutmut_11': x_abort_git_merge__mutmut_11, 
    'x_abort_git_merge__mutmut_12': x_abort_git_merge__mutmut_12, 
    'x_abort_git_merge__mutmut_13': x_abort_git_merge__mutmut_13, 
    'x_abort_git_merge__mutmut_14': x_abort_git_merge__mutmut_14, 
    'x_abort_git_merge__mutmut_15': x_abort_git_merge__mutmut_15, 
    'x_abort_git_merge__mutmut_16': x_abort_git_merge__mutmut_16, 
    'x_abort_git_merge__mutmut_17': x_abort_git_merge__mutmut_17, 
    'x_abort_git_merge__mutmut_18': x_abort_git_merge__mutmut_18
}
x_abort_git_merge__mutmut_orig.__name__ = 'x_abort_git_merge'
