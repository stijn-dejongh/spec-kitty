"""Legacy bridge -- backward compatibility views from canonical StatusSnapshot.

Generates human-readable views (WP frontmatter `lane` fields and tasks.md
status sections) from the canonical `status.json` snapshot. These views are
never authoritative; they are compatibility caches that existing tools
(agents, dashboards, slash commands) read.

Phase behavior:
  - Phase 0: No-op (no event log yet, frontmatter is still the authority)
  - Phase 1: Update views on every emit (dual-write mode)
  - Phase 2: Views are generated after materialize only, never read as authority
"""

from __future__ import annotations

import logging
from pathlib import Path

from specify_cli.frontmatter import FrontmatterManager
from specify_cli.status.models import StatusSnapshot
from specify_cli.status.phase import resolve_phase

logger = logging.getLogger(__name__)

STATUS_BLOCK_START = "<!-- status-model:start -->"
STATUS_BLOCK_END = "<!-- status-model:end -->"
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


def update_frontmatter_views(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    args = [feature_dir, snapshot]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_update_frontmatter_views__mutmut_orig, x_update_frontmatter_views__mutmut_mutants, args, kwargs, None)


def x_update_frontmatter_views__mutmut_orig(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_1(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = None
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_2(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir * "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_3(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "XXtasksXX"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_4(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "TASKS"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_5(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_6(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning(None, tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_7(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", None)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_8(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning(tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_9(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", )
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_10(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("XXTasks directory not found: %sXX", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_11(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_12(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("TASKS DIRECTORY NOT FOUND: %S", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_13(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = None

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_14(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = None
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_15(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get(None)
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_16(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("XXlaneXX")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_17(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("LANE")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_18(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is not None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_19(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            break

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_20(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = None
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_21(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(None)
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_22(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(None))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_23(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_24(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                None, wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_25(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", None, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_26(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, None
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_27(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_28(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_29(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_30(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "XXNo task file found for %s in %sXX", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_31(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "no task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_32(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "NO TASK FILE FOUND FOR %S IN %S", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_33(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            break
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_34(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) >= 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_35(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 2:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_36(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                None,
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_37(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                None, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_38(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, None,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_39(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_40(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_41(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_42(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "XXMultiple task files for %s: %s (using first)XX",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_43(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_44(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "MULTIPLE TASK FILES FOR %S: %S (USING FIRST)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_45(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = None

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_46(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[1]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_47(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = None
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_48(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(None)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_49(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = None

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_50(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get(None)

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_51(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("XXlaneXX")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_52(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("LANE")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_53(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane != lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_54(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            break

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_55(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = None
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_56(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["XXlaneXX"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_57(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["LANE"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_58(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(None, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_59(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, None, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_60(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, None)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_61(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_62(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_63(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, )
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_64(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            None,
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_65(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            None, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_66(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, None, lane_value,
        )


def x_update_frontmatter_views__mutmut_67(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, None,
        )


def x_update_frontmatter_views__mutmut_68(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_69(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_70(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, lane_value,
        )


def x_update_frontmatter_views__mutmut_71(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "Updated %s lane: %s -> %s",
            wp_id, current_lane, )


def x_update_frontmatter_views__mutmut_72(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "XXUpdated %s lane: %s -> %sXX",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_73(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "updated %s lane: %s -> %s",
            wp_id, current_lane, lane_value,
        )


def x_update_frontmatter_views__mutmut_74(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update WP frontmatter lane fields from StatusSnapshot.

    For each WP in the snapshot, finds the corresponding
    tasks/WP##-*.md file and updates its 'lane' field.

    Skips writes when the lane already matches to avoid unnecessary diffs.
    Logs warnings for missing WP files but does not error.
    Propagates write errors without catching them.
    """
    tasks_dir = feature_dir / "tasks"
    if not tasks_dir.exists():
        logger.warning("Tasks directory not found: %s", tasks_dir)
        return

    fm = FrontmatterManager()

    for wp_id, wp_state in snapshot.work_packages.items():
        lane_value = wp_state.get("lane")
        if lane_value is None:
            continue

        # Find the WP file by glob pattern
        wp_files = list(tasks_dir.glob(f"{wp_id}-*.md"))
        if not wp_files:
            logger.warning(
                "No task file found for %s in %s", wp_id, tasks_dir
            )
            continue
        if len(wp_files) > 1:
            logger.warning(
                "Multiple task files for %s: %s (using first)",
                wp_id, wp_files,
            )

        wp_file = wp_files[0]

        frontmatter, body = fm.read(wp_file)
        current_lane = frontmatter.get("lane")

        if current_lane == lane_value:
            # Already in sync, skip write
            continue

        frontmatter["lane"] = lane_value
        fm.write(wp_file, frontmatter, body)
        logger.debug(
            "UPDATED %S LANE: %S -> %S",
            wp_id, current_lane, lane_value,
        )

x_update_frontmatter_views__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_update_frontmatter_views__mutmut_1': x_update_frontmatter_views__mutmut_1, 
    'x_update_frontmatter_views__mutmut_2': x_update_frontmatter_views__mutmut_2, 
    'x_update_frontmatter_views__mutmut_3': x_update_frontmatter_views__mutmut_3, 
    'x_update_frontmatter_views__mutmut_4': x_update_frontmatter_views__mutmut_4, 
    'x_update_frontmatter_views__mutmut_5': x_update_frontmatter_views__mutmut_5, 
    'x_update_frontmatter_views__mutmut_6': x_update_frontmatter_views__mutmut_6, 
    'x_update_frontmatter_views__mutmut_7': x_update_frontmatter_views__mutmut_7, 
    'x_update_frontmatter_views__mutmut_8': x_update_frontmatter_views__mutmut_8, 
    'x_update_frontmatter_views__mutmut_9': x_update_frontmatter_views__mutmut_9, 
    'x_update_frontmatter_views__mutmut_10': x_update_frontmatter_views__mutmut_10, 
    'x_update_frontmatter_views__mutmut_11': x_update_frontmatter_views__mutmut_11, 
    'x_update_frontmatter_views__mutmut_12': x_update_frontmatter_views__mutmut_12, 
    'x_update_frontmatter_views__mutmut_13': x_update_frontmatter_views__mutmut_13, 
    'x_update_frontmatter_views__mutmut_14': x_update_frontmatter_views__mutmut_14, 
    'x_update_frontmatter_views__mutmut_15': x_update_frontmatter_views__mutmut_15, 
    'x_update_frontmatter_views__mutmut_16': x_update_frontmatter_views__mutmut_16, 
    'x_update_frontmatter_views__mutmut_17': x_update_frontmatter_views__mutmut_17, 
    'x_update_frontmatter_views__mutmut_18': x_update_frontmatter_views__mutmut_18, 
    'x_update_frontmatter_views__mutmut_19': x_update_frontmatter_views__mutmut_19, 
    'x_update_frontmatter_views__mutmut_20': x_update_frontmatter_views__mutmut_20, 
    'x_update_frontmatter_views__mutmut_21': x_update_frontmatter_views__mutmut_21, 
    'x_update_frontmatter_views__mutmut_22': x_update_frontmatter_views__mutmut_22, 
    'x_update_frontmatter_views__mutmut_23': x_update_frontmatter_views__mutmut_23, 
    'x_update_frontmatter_views__mutmut_24': x_update_frontmatter_views__mutmut_24, 
    'x_update_frontmatter_views__mutmut_25': x_update_frontmatter_views__mutmut_25, 
    'x_update_frontmatter_views__mutmut_26': x_update_frontmatter_views__mutmut_26, 
    'x_update_frontmatter_views__mutmut_27': x_update_frontmatter_views__mutmut_27, 
    'x_update_frontmatter_views__mutmut_28': x_update_frontmatter_views__mutmut_28, 
    'x_update_frontmatter_views__mutmut_29': x_update_frontmatter_views__mutmut_29, 
    'x_update_frontmatter_views__mutmut_30': x_update_frontmatter_views__mutmut_30, 
    'x_update_frontmatter_views__mutmut_31': x_update_frontmatter_views__mutmut_31, 
    'x_update_frontmatter_views__mutmut_32': x_update_frontmatter_views__mutmut_32, 
    'x_update_frontmatter_views__mutmut_33': x_update_frontmatter_views__mutmut_33, 
    'x_update_frontmatter_views__mutmut_34': x_update_frontmatter_views__mutmut_34, 
    'x_update_frontmatter_views__mutmut_35': x_update_frontmatter_views__mutmut_35, 
    'x_update_frontmatter_views__mutmut_36': x_update_frontmatter_views__mutmut_36, 
    'x_update_frontmatter_views__mutmut_37': x_update_frontmatter_views__mutmut_37, 
    'x_update_frontmatter_views__mutmut_38': x_update_frontmatter_views__mutmut_38, 
    'x_update_frontmatter_views__mutmut_39': x_update_frontmatter_views__mutmut_39, 
    'x_update_frontmatter_views__mutmut_40': x_update_frontmatter_views__mutmut_40, 
    'x_update_frontmatter_views__mutmut_41': x_update_frontmatter_views__mutmut_41, 
    'x_update_frontmatter_views__mutmut_42': x_update_frontmatter_views__mutmut_42, 
    'x_update_frontmatter_views__mutmut_43': x_update_frontmatter_views__mutmut_43, 
    'x_update_frontmatter_views__mutmut_44': x_update_frontmatter_views__mutmut_44, 
    'x_update_frontmatter_views__mutmut_45': x_update_frontmatter_views__mutmut_45, 
    'x_update_frontmatter_views__mutmut_46': x_update_frontmatter_views__mutmut_46, 
    'x_update_frontmatter_views__mutmut_47': x_update_frontmatter_views__mutmut_47, 
    'x_update_frontmatter_views__mutmut_48': x_update_frontmatter_views__mutmut_48, 
    'x_update_frontmatter_views__mutmut_49': x_update_frontmatter_views__mutmut_49, 
    'x_update_frontmatter_views__mutmut_50': x_update_frontmatter_views__mutmut_50, 
    'x_update_frontmatter_views__mutmut_51': x_update_frontmatter_views__mutmut_51, 
    'x_update_frontmatter_views__mutmut_52': x_update_frontmatter_views__mutmut_52, 
    'x_update_frontmatter_views__mutmut_53': x_update_frontmatter_views__mutmut_53, 
    'x_update_frontmatter_views__mutmut_54': x_update_frontmatter_views__mutmut_54, 
    'x_update_frontmatter_views__mutmut_55': x_update_frontmatter_views__mutmut_55, 
    'x_update_frontmatter_views__mutmut_56': x_update_frontmatter_views__mutmut_56, 
    'x_update_frontmatter_views__mutmut_57': x_update_frontmatter_views__mutmut_57, 
    'x_update_frontmatter_views__mutmut_58': x_update_frontmatter_views__mutmut_58, 
    'x_update_frontmatter_views__mutmut_59': x_update_frontmatter_views__mutmut_59, 
    'x_update_frontmatter_views__mutmut_60': x_update_frontmatter_views__mutmut_60, 
    'x_update_frontmatter_views__mutmut_61': x_update_frontmatter_views__mutmut_61, 
    'x_update_frontmatter_views__mutmut_62': x_update_frontmatter_views__mutmut_62, 
    'x_update_frontmatter_views__mutmut_63': x_update_frontmatter_views__mutmut_63, 
    'x_update_frontmatter_views__mutmut_64': x_update_frontmatter_views__mutmut_64, 
    'x_update_frontmatter_views__mutmut_65': x_update_frontmatter_views__mutmut_65, 
    'x_update_frontmatter_views__mutmut_66': x_update_frontmatter_views__mutmut_66, 
    'x_update_frontmatter_views__mutmut_67': x_update_frontmatter_views__mutmut_67, 
    'x_update_frontmatter_views__mutmut_68': x_update_frontmatter_views__mutmut_68, 
    'x_update_frontmatter_views__mutmut_69': x_update_frontmatter_views__mutmut_69, 
    'x_update_frontmatter_views__mutmut_70': x_update_frontmatter_views__mutmut_70, 
    'x_update_frontmatter_views__mutmut_71': x_update_frontmatter_views__mutmut_71, 
    'x_update_frontmatter_views__mutmut_72': x_update_frontmatter_views__mutmut_72, 
    'x_update_frontmatter_views__mutmut_73': x_update_frontmatter_views__mutmut_73, 
    'x_update_frontmatter_views__mutmut_74': x_update_frontmatter_views__mutmut_74
}
x_update_frontmatter_views__mutmut_orig.__name__ = 'x_update_frontmatter_views'


def update_tasks_md_views(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    args = [feature_dir, snapshot]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_update_tasks_md_views__mutmut_orig, x_update_tasks_md_views__mutmut_mutants, args, kwargs, None)


def x_update_tasks_md_views__mutmut_orig(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_1(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = None
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_2(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir * "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_3(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "XXtasks.mdXX"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_4(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "TASKS.MD"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_5(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_6(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug(None, tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_7(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", None)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_8(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug(tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_9(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", )
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_10(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("XXtasks.md not found: %sXX", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_11(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("TASKS.MD NOT FOUND: %S", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_12(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = None
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_13(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding=None)
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_14(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="XXutf-8XX")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_15(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="UTF-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_16(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = None

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_17(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(None, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_18(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, None)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_19(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_20(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, )

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_21(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated == content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_22(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(None, encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_23(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding=None)
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_24(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(encoding="utf-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_25(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, )
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_26(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="XXutf-8XX")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_27(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="UTF-8")
        logger.debug("Updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_28(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug(None)


def x_update_tasks_md_views__mutmut_29(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("XXUpdated tasks.md status sectionsXX")


def x_update_tasks_md_views__mutmut_30(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("updated tasks.md status sections")


def x_update_tasks_md_views__mutmut_31(
    feature_dir: Path,
    snapshot: StatusSnapshot,
) -> None:
    """Update tasks.md status sections from StatusSnapshot.

    Updates WP section headers or status metadata to reflect
    canonical lane values. Does NOT modify subtask checkboxes
    (those are for subtask tracking, separate from lane status).

    Current implementation is a lightweight pass-through because
    tasks.md does not contain lane status fields that need updating.
    The WP sections in tasks.md have subtask checkboxes and descriptive
    text, not frontmatter-style lane fields. The authoritative lane
    display is in the individual WP files' frontmatter.
    """
    tasks_md = feature_dir / "tasks.md"
    if not tasks_md.exists():
        logger.debug("tasks.md not found: %s", tasks_md)
        return

    content = tasks_md.read_text(encoding="utf-8")
    updated = _update_wp_status_in_tasks_md(content, snapshot)

    if updated != content:
        tasks_md.write_text(updated, encoding="utf-8")
        logger.debug("UPDATED TASKS.MD STATUS SECTIONS")

x_update_tasks_md_views__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_update_tasks_md_views__mutmut_1': x_update_tasks_md_views__mutmut_1, 
    'x_update_tasks_md_views__mutmut_2': x_update_tasks_md_views__mutmut_2, 
    'x_update_tasks_md_views__mutmut_3': x_update_tasks_md_views__mutmut_3, 
    'x_update_tasks_md_views__mutmut_4': x_update_tasks_md_views__mutmut_4, 
    'x_update_tasks_md_views__mutmut_5': x_update_tasks_md_views__mutmut_5, 
    'x_update_tasks_md_views__mutmut_6': x_update_tasks_md_views__mutmut_6, 
    'x_update_tasks_md_views__mutmut_7': x_update_tasks_md_views__mutmut_7, 
    'x_update_tasks_md_views__mutmut_8': x_update_tasks_md_views__mutmut_8, 
    'x_update_tasks_md_views__mutmut_9': x_update_tasks_md_views__mutmut_9, 
    'x_update_tasks_md_views__mutmut_10': x_update_tasks_md_views__mutmut_10, 
    'x_update_tasks_md_views__mutmut_11': x_update_tasks_md_views__mutmut_11, 
    'x_update_tasks_md_views__mutmut_12': x_update_tasks_md_views__mutmut_12, 
    'x_update_tasks_md_views__mutmut_13': x_update_tasks_md_views__mutmut_13, 
    'x_update_tasks_md_views__mutmut_14': x_update_tasks_md_views__mutmut_14, 
    'x_update_tasks_md_views__mutmut_15': x_update_tasks_md_views__mutmut_15, 
    'x_update_tasks_md_views__mutmut_16': x_update_tasks_md_views__mutmut_16, 
    'x_update_tasks_md_views__mutmut_17': x_update_tasks_md_views__mutmut_17, 
    'x_update_tasks_md_views__mutmut_18': x_update_tasks_md_views__mutmut_18, 
    'x_update_tasks_md_views__mutmut_19': x_update_tasks_md_views__mutmut_19, 
    'x_update_tasks_md_views__mutmut_20': x_update_tasks_md_views__mutmut_20, 
    'x_update_tasks_md_views__mutmut_21': x_update_tasks_md_views__mutmut_21, 
    'x_update_tasks_md_views__mutmut_22': x_update_tasks_md_views__mutmut_22, 
    'x_update_tasks_md_views__mutmut_23': x_update_tasks_md_views__mutmut_23, 
    'x_update_tasks_md_views__mutmut_24': x_update_tasks_md_views__mutmut_24, 
    'x_update_tasks_md_views__mutmut_25': x_update_tasks_md_views__mutmut_25, 
    'x_update_tasks_md_views__mutmut_26': x_update_tasks_md_views__mutmut_26, 
    'x_update_tasks_md_views__mutmut_27': x_update_tasks_md_views__mutmut_27, 
    'x_update_tasks_md_views__mutmut_28': x_update_tasks_md_views__mutmut_28, 
    'x_update_tasks_md_views__mutmut_29': x_update_tasks_md_views__mutmut_29, 
    'x_update_tasks_md_views__mutmut_30': x_update_tasks_md_views__mutmut_30, 
    'x_update_tasks_md_views__mutmut_31': x_update_tasks_md_views__mutmut_31
}
x_update_tasks_md_views__mutmut_orig.__name__ = 'x_update_tasks_md_views'


def _update_wp_status_in_tasks_md(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    args = [content, snapshot]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__update_wp_status_in_tasks_md__mutmut_orig, x__update_wp_status_in_tasks_md__mutmut_mutants, args, kwargs, None)


def x__update_wp_status_in_tasks_md__mutmut_orig(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_1(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = None
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_2(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(None)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_3(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = None
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_4(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(None)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_5(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.rfind(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_6(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = None

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_7(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(None, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_8(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, None)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_9(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_10(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, )

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_11(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.rfind(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_12(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx == -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_13(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != +1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_14(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -2 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_15(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 1)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_16(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 or end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_17(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx == -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_18(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != +1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_19(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -2 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_20(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx == -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_21(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != +1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_22(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -2:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_23(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = None
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_24(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx - len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_25(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = None
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_26(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].lstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_27(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = None
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_28(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip(None)
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_29(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].rstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_30(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("XX\nXX")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_31(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = None
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_32(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt = "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_33(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt -= "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_34(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "XX\n\nXX"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_35(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt = status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_36(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt -= status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_37(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt = "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_38(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt -= "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_39(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" - after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_40(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "XX\n\nXX" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_41(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_42(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith(None):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_43(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("XX\nXX"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_44(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt = "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_45(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt -= "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_46(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "XX\nXX"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_47(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_48(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block - "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_49(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "XX\nXX"

    rebuilt = content.rstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_50(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = None
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_51(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block - "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_52(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" - status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_53(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() - "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_54(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.lstrip() + "\n\n" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_55(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "XX\n\nXX" + status_block + "\n"
    return rebuilt


def x__update_wp_status_in_tasks_md__mutmut_56(
    content: str,
    snapshot: StatusSnapshot,
) -> str:
    """Update WP status references in tasks.md content.

    Strategy: Find WP section headers and update any inline
    status indicators. Preserves all other content unchanged.

    Does NOT modify:
    - Subtask checkboxes ([ ] or [x])
    - Non-WP sections
    - Content within WP sections (only headers/metadata)

    Adds/updates a generated canonical status block delimited by stable
    markers so validation can detect drift reliably.
    """
    status_block = _render_tasks_status_block(snapshot)
    start_idx = content.find(STATUS_BLOCK_START)
    end_idx = content.find(STATUS_BLOCK_END, start_idx if start_idx != -1 else 0)

    if start_idx != -1 and end_idx != -1:
        end_exclusive = end_idx + len(STATUS_BLOCK_END)
        before = content[:start_idx].rstrip()
        after = content[end_exclusive:].lstrip("\n")
        rebuilt = before
        if rebuilt:
            rebuilt += "\n\n"
        rebuilt += status_block
        if after:
            rebuilt += "\n\n" + after
        if not rebuilt.endswith("\n"):
            rebuilt += "\n"
        return rebuilt

    if not content.strip():
        return status_block + "\n"

    rebuilt = content.rstrip() + "\n\n" + status_block + "XX\nXX"
    return rebuilt

x__update_wp_status_in_tasks_md__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__update_wp_status_in_tasks_md__mutmut_1': x__update_wp_status_in_tasks_md__mutmut_1, 
    'x__update_wp_status_in_tasks_md__mutmut_2': x__update_wp_status_in_tasks_md__mutmut_2, 
    'x__update_wp_status_in_tasks_md__mutmut_3': x__update_wp_status_in_tasks_md__mutmut_3, 
    'x__update_wp_status_in_tasks_md__mutmut_4': x__update_wp_status_in_tasks_md__mutmut_4, 
    'x__update_wp_status_in_tasks_md__mutmut_5': x__update_wp_status_in_tasks_md__mutmut_5, 
    'x__update_wp_status_in_tasks_md__mutmut_6': x__update_wp_status_in_tasks_md__mutmut_6, 
    'x__update_wp_status_in_tasks_md__mutmut_7': x__update_wp_status_in_tasks_md__mutmut_7, 
    'x__update_wp_status_in_tasks_md__mutmut_8': x__update_wp_status_in_tasks_md__mutmut_8, 
    'x__update_wp_status_in_tasks_md__mutmut_9': x__update_wp_status_in_tasks_md__mutmut_9, 
    'x__update_wp_status_in_tasks_md__mutmut_10': x__update_wp_status_in_tasks_md__mutmut_10, 
    'x__update_wp_status_in_tasks_md__mutmut_11': x__update_wp_status_in_tasks_md__mutmut_11, 
    'x__update_wp_status_in_tasks_md__mutmut_12': x__update_wp_status_in_tasks_md__mutmut_12, 
    'x__update_wp_status_in_tasks_md__mutmut_13': x__update_wp_status_in_tasks_md__mutmut_13, 
    'x__update_wp_status_in_tasks_md__mutmut_14': x__update_wp_status_in_tasks_md__mutmut_14, 
    'x__update_wp_status_in_tasks_md__mutmut_15': x__update_wp_status_in_tasks_md__mutmut_15, 
    'x__update_wp_status_in_tasks_md__mutmut_16': x__update_wp_status_in_tasks_md__mutmut_16, 
    'x__update_wp_status_in_tasks_md__mutmut_17': x__update_wp_status_in_tasks_md__mutmut_17, 
    'x__update_wp_status_in_tasks_md__mutmut_18': x__update_wp_status_in_tasks_md__mutmut_18, 
    'x__update_wp_status_in_tasks_md__mutmut_19': x__update_wp_status_in_tasks_md__mutmut_19, 
    'x__update_wp_status_in_tasks_md__mutmut_20': x__update_wp_status_in_tasks_md__mutmut_20, 
    'x__update_wp_status_in_tasks_md__mutmut_21': x__update_wp_status_in_tasks_md__mutmut_21, 
    'x__update_wp_status_in_tasks_md__mutmut_22': x__update_wp_status_in_tasks_md__mutmut_22, 
    'x__update_wp_status_in_tasks_md__mutmut_23': x__update_wp_status_in_tasks_md__mutmut_23, 
    'x__update_wp_status_in_tasks_md__mutmut_24': x__update_wp_status_in_tasks_md__mutmut_24, 
    'x__update_wp_status_in_tasks_md__mutmut_25': x__update_wp_status_in_tasks_md__mutmut_25, 
    'x__update_wp_status_in_tasks_md__mutmut_26': x__update_wp_status_in_tasks_md__mutmut_26, 
    'x__update_wp_status_in_tasks_md__mutmut_27': x__update_wp_status_in_tasks_md__mutmut_27, 
    'x__update_wp_status_in_tasks_md__mutmut_28': x__update_wp_status_in_tasks_md__mutmut_28, 
    'x__update_wp_status_in_tasks_md__mutmut_29': x__update_wp_status_in_tasks_md__mutmut_29, 
    'x__update_wp_status_in_tasks_md__mutmut_30': x__update_wp_status_in_tasks_md__mutmut_30, 
    'x__update_wp_status_in_tasks_md__mutmut_31': x__update_wp_status_in_tasks_md__mutmut_31, 
    'x__update_wp_status_in_tasks_md__mutmut_32': x__update_wp_status_in_tasks_md__mutmut_32, 
    'x__update_wp_status_in_tasks_md__mutmut_33': x__update_wp_status_in_tasks_md__mutmut_33, 
    'x__update_wp_status_in_tasks_md__mutmut_34': x__update_wp_status_in_tasks_md__mutmut_34, 
    'x__update_wp_status_in_tasks_md__mutmut_35': x__update_wp_status_in_tasks_md__mutmut_35, 
    'x__update_wp_status_in_tasks_md__mutmut_36': x__update_wp_status_in_tasks_md__mutmut_36, 
    'x__update_wp_status_in_tasks_md__mutmut_37': x__update_wp_status_in_tasks_md__mutmut_37, 
    'x__update_wp_status_in_tasks_md__mutmut_38': x__update_wp_status_in_tasks_md__mutmut_38, 
    'x__update_wp_status_in_tasks_md__mutmut_39': x__update_wp_status_in_tasks_md__mutmut_39, 
    'x__update_wp_status_in_tasks_md__mutmut_40': x__update_wp_status_in_tasks_md__mutmut_40, 
    'x__update_wp_status_in_tasks_md__mutmut_41': x__update_wp_status_in_tasks_md__mutmut_41, 
    'x__update_wp_status_in_tasks_md__mutmut_42': x__update_wp_status_in_tasks_md__mutmut_42, 
    'x__update_wp_status_in_tasks_md__mutmut_43': x__update_wp_status_in_tasks_md__mutmut_43, 
    'x__update_wp_status_in_tasks_md__mutmut_44': x__update_wp_status_in_tasks_md__mutmut_44, 
    'x__update_wp_status_in_tasks_md__mutmut_45': x__update_wp_status_in_tasks_md__mutmut_45, 
    'x__update_wp_status_in_tasks_md__mutmut_46': x__update_wp_status_in_tasks_md__mutmut_46, 
    'x__update_wp_status_in_tasks_md__mutmut_47': x__update_wp_status_in_tasks_md__mutmut_47, 
    'x__update_wp_status_in_tasks_md__mutmut_48': x__update_wp_status_in_tasks_md__mutmut_48, 
    'x__update_wp_status_in_tasks_md__mutmut_49': x__update_wp_status_in_tasks_md__mutmut_49, 
    'x__update_wp_status_in_tasks_md__mutmut_50': x__update_wp_status_in_tasks_md__mutmut_50, 
    'x__update_wp_status_in_tasks_md__mutmut_51': x__update_wp_status_in_tasks_md__mutmut_51, 
    'x__update_wp_status_in_tasks_md__mutmut_52': x__update_wp_status_in_tasks_md__mutmut_52, 
    'x__update_wp_status_in_tasks_md__mutmut_53': x__update_wp_status_in_tasks_md__mutmut_53, 
    'x__update_wp_status_in_tasks_md__mutmut_54': x__update_wp_status_in_tasks_md__mutmut_54, 
    'x__update_wp_status_in_tasks_md__mutmut_55': x__update_wp_status_in_tasks_md__mutmut_55, 
    'x__update_wp_status_in_tasks_md__mutmut_56': x__update_wp_status_in_tasks_md__mutmut_56
}
x__update_wp_status_in_tasks_md__mutmut_orig.__name__ = 'x__update_wp_status_in_tasks_md'


def _render_tasks_status_block(snapshot: StatusSnapshot) -> str:
    args = [snapshot]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__render_tasks_status_block__mutmut_orig, x__render_tasks_status_block__mutmut_mutants, args, kwargs, None)


def x__render_tasks_status_block__mutmut_orig(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("lane", "")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_1(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = None
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("lane", "")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_2(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "XX## Canonical Status (Generated)XX",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("lane", "")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_3(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## canonical status (generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("lane", "")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_4(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## CANONICAL STATUS (GENERATED)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("lane", "")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_5(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(None):
        lane = snapshot.work_packages[wp_id].get("lane", "")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_6(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = None
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_7(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get(None, "")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_8(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("lane", None)
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_9(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_10(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("lane", )
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_11(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("XXlaneXX", "")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_12(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("LANE", "")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_13(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("lane", "XXXX")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_14(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("lane", "")
        lines.append(None)
    lines.append(STATUS_BLOCK_END)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_15(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("lane", "")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(None)
    return "\n".join(lines)


def x__render_tasks_status_block__mutmut_16(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("lane", "")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "\n".join(None)


def x__render_tasks_status_block__mutmut_17(snapshot: StatusSnapshot) -> str:
    """Render deterministic generated status lines for tasks.md."""
    lines = [
        STATUS_BLOCK_START,
        "## Canonical Status (Generated)",
    ]
    for wp_id in sorted(snapshot.work_packages):
        lane = snapshot.work_packages[wp_id].get("lane", "")
        lines.append(f"- {wp_id}: {lane}")
    lines.append(STATUS_BLOCK_END)
    return "XX\nXX".join(lines)

x__render_tasks_status_block__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__render_tasks_status_block__mutmut_1': x__render_tasks_status_block__mutmut_1, 
    'x__render_tasks_status_block__mutmut_2': x__render_tasks_status_block__mutmut_2, 
    'x__render_tasks_status_block__mutmut_3': x__render_tasks_status_block__mutmut_3, 
    'x__render_tasks_status_block__mutmut_4': x__render_tasks_status_block__mutmut_4, 
    'x__render_tasks_status_block__mutmut_5': x__render_tasks_status_block__mutmut_5, 
    'x__render_tasks_status_block__mutmut_6': x__render_tasks_status_block__mutmut_6, 
    'x__render_tasks_status_block__mutmut_7': x__render_tasks_status_block__mutmut_7, 
    'x__render_tasks_status_block__mutmut_8': x__render_tasks_status_block__mutmut_8, 
    'x__render_tasks_status_block__mutmut_9': x__render_tasks_status_block__mutmut_9, 
    'x__render_tasks_status_block__mutmut_10': x__render_tasks_status_block__mutmut_10, 
    'x__render_tasks_status_block__mutmut_11': x__render_tasks_status_block__mutmut_11, 
    'x__render_tasks_status_block__mutmut_12': x__render_tasks_status_block__mutmut_12, 
    'x__render_tasks_status_block__mutmut_13': x__render_tasks_status_block__mutmut_13, 
    'x__render_tasks_status_block__mutmut_14': x__render_tasks_status_block__mutmut_14, 
    'x__render_tasks_status_block__mutmut_15': x__render_tasks_status_block__mutmut_15, 
    'x__render_tasks_status_block__mutmut_16': x__render_tasks_status_block__mutmut_16, 
    'x__render_tasks_status_block__mutmut_17': x__render_tasks_status_block__mutmut_17
}
x__render_tasks_status_block__mutmut_orig.__name__ = 'x__render_tasks_status_block'


def update_all_views(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    args = [feature_dir, snapshot]# type: ignore
    kwargs = {'repo_root': repo_root}# type: ignore
    return _mutmut_trampoline(x_update_all_views__mutmut_orig, x_update_all_views__mutmut_mutants, args, kwargs, None)


def x_update_all_views__mutmut_orig(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_1(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is not None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_2(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = None

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_3(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = None

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_4(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(None, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_5(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, None)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_6(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_7(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, )

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_8(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase != 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_9(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 1:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_10(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            None, source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_11(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", None
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_12(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_13(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_14(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "XXPhase 0 (%s): legacy bridge is no-opXX", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_15(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_16(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "PHASE 0 (%S): LEGACY BRIDGE IS NO-OP", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_17(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(None, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_18(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, None)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_19(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_20(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, )
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_21(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(None, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_22(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, None)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_23(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_24(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, )

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_25(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        None,
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_26(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        None, phase, source,
    )


def x_update_all_views__mutmut_27(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, None, source,
    )


def x_update_all_views__mutmut_28(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, None,
    )


def x_update_all_views__mutmut_29(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_30(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        phase, source,
    )


def x_update_all_views__mutmut_31(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, source,
    )


def x_update_all_views__mutmut_32(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "Legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, )


def x_update_all_views__mutmut_33(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "XXLegacy views updated for %s (phase %d: %s)XX",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_34(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "legacy views updated for %s (phase %d: %s)",
        snapshot.feature_slug, phase, source,
    )


def x_update_all_views__mutmut_35(
    feature_dir: Path,
    snapshot: StatusSnapshot,
    *,
    repo_root: Path | None = None,
) -> None:
    """Update all compatibility views from the canonical snapshot.

    Checks the current phase and adjusts behavior:
    - Phase 0: No-op (no event log, frontmatter is still authority)
    - Phase 1: Update views (dual-write mode)
    - Phase 2: Update views (views are generated-only)

    Args:
        feature_dir: Path to the feature directory (kitty-specs/<feature>/)
        snapshot: The StatusSnapshot to generate views from
        repo_root: Repository root for phase resolution. If None, derived
                   from feature_dir (assumes kitty-specs/<slug>/ structure).
    """
    if repo_root is None:
        # Derive repo_root: feature_dir is typically kitty-specs/<slug>/
        repo_root = feature_dir.parent.parent

    phase, source = resolve_phase(repo_root, snapshot.feature_slug)

    if phase == 0:
        logger.debug(
            "Phase 0 (%s): legacy bridge is no-op", source
        )
        return

    # Phase 1 and Phase 2: update views
    update_frontmatter_views(feature_dir, snapshot)
    update_tasks_md_views(feature_dir, snapshot)

    logger.debug(
        "LEGACY VIEWS UPDATED FOR %S (PHASE %D: %S)",
        snapshot.feature_slug, phase, source,
    )

x_update_all_views__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_update_all_views__mutmut_1': x_update_all_views__mutmut_1, 
    'x_update_all_views__mutmut_2': x_update_all_views__mutmut_2, 
    'x_update_all_views__mutmut_3': x_update_all_views__mutmut_3, 
    'x_update_all_views__mutmut_4': x_update_all_views__mutmut_4, 
    'x_update_all_views__mutmut_5': x_update_all_views__mutmut_5, 
    'x_update_all_views__mutmut_6': x_update_all_views__mutmut_6, 
    'x_update_all_views__mutmut_7': x_update_all_views__mutmut_7, 
    'x_update_all_views__mutmut_8': x_update_all_views__mutmut_8, 
    'x_update_all_views__mutmut_9': x_update_all_views__mutmut_9, 
    'x_update_all_views__mutmut_10': x_update_all_views__mutmut_10, 
    'x_update_all_views__mutmut_11': x_update_all_views__mutmut_11, 
    'x_update_all_views__mutmut_12': x_update_all_views__mutmut_12, 
    'x_update_all_views__mutmut_13': x_update_all_views__mutmut_13, 
    'x_update_all_views__mutmut_14': x_update_all_views__mutmut_14, 
    'x_update_all_views__mutmut_15': x_update_all_views__mutmut_15, 
    'x_update_all_views__mutmut_16': x_update_all_views__mutmut_16, 
    'x_update_all_views__mutmut_17': x_update_all_views__mutmut_17, 
    'x_update_all_views__mutmut_18': x_update_all_views__mutmut_18, 
    'x_update_all_views__mutmut_19': x_update_all_views__mutmut_19, 
    'x_update_all_views__mutmut_20': x_update_all_views__mutmut_20, 
    'x_update_all_views__mutmut_21': x_update_all_views__mutmut_21, 
    'x_update_all_views__mutmut_22': x_update_all_views__mutmut_22, 
    'x_update_all_views__mutmut_23': x_update_all_views__mutmut_23, 
    'x_update_all_views__mutmut_24': x_update_all_views__mutmut_24, 
    'x_update_all_views__mutmut_25': x_update_all_views__mutmut_25, 
    'x_update_all_views__mutmut_26': x_update_all_views__mutmut_26, 
    'x_update_all_views__mutmut_27': x_update_all_views__mutmut_27, 
    'x_update_all_views__mutmut_28': x_update_all_views__mutmut_28, 
    'x_update_all_views__mutmut_29': x_update_all_views__mutmut_29, 
    'x_update_all_views__mutmut_30': x_update_all_views__mutmut_30, 
    'x_update_all_views__mutmut_31': x_update_all_views__mutmut_31, 
    'x_update_all_views__mutmut_32': x_update_all_views__mutmut_32, 
    'x_update_all_views__mutmut_33': x_update_all_views__mutmut_33, 
    'x_update_all_views__mutmut_34': x_update_all_views__mutmut_34, 
    'x_update_all_views__mutmut_35': x_update_all_views__mutmut_35
}
x_update_all_views__mutmut_orig.__name__ = 'x_update_all_views'
