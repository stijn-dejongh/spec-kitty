"""Dependency resolution and merge strategy recommendation.

This module provides logic to detect when multi-parent dependencies should be
merged to main before implementing a dependent WP, avoiding auto-merge conflicts.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from specify_cli.frontmatter import read_frontmatter
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
class DependencyStatus:
    """Status of a WP's dependencies.

    Attributes:
        wp_id: Work package ID (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])
        all_done: True if all dependencies in "done" lane
        lanes: Dict mapping dependency WP ID to lane status
        is_multi_parent: True if more than one dependency
    """

    wp_id: str
    dependencies: list[str]
    all_done: bool
    lanes: dict[str, str]
    is_multi_parent: bool

    @property
    def should_suggest_merge_first(self) -> bool:
        """Return True if we should suggest merging dependencies before implement.

        Logic:
        - Multi-parent (2+ dependencies) AND
        - All dependencies in "done" lane
        → Suggest merging to main first
        """
        return self.is_multi_parent and self.all_done

    def get_recommendation(self) -> str:
        """Get recommended workflow for implementing this WP.

        Returns:
            Recommendation string (user/agent guidance)
        """
        if not self.dependencies:
            return "No dependencies - implement directly from main"

        if not self.all_done:
            not_done = [dep for dep, lane in self.lanes.items() if lane != "done"]
            return f"Cannot implement - dependencies not complete: {', '.join(not_done)}"

        if len(self.dependencies) == 1:
            dep = self.dependencies[0]
            return f"Single dependency ({dep}) - use --base {dep}"

        # Multi-parent, all done
        deps_str = ", ".join(self.dependencies)
        return (
            f"Multi-parent dependencies ({deps_str}) all done.\n"
            f"\n"
            f"RECOMMENDED: Merge dependencies to main first (avoids conflicts)\n"
            f"  1. spec-kitty merge --feature <feature-slug>\n"
            f"  2. spec-kitty implement {self.wp_id}\n"
            f"\n"
            f"ALTERNATIVE: Attempt auto-merge (may conflict)\n"
            f"  spec-kitty implement {self.wp_id} --force\n"
            f"\n"
            f"Auto-merge works if WPs don't conflict on shared files\n"
            f"(.gitignore, package.json, etc.)"
        )


def check_dependency_status(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    args = [feature_dir, wp_id, dependencies]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_dependency_status__mutmut_orig, x_check_dependency_status__mutmut_mutants, args, kwargs, None)


def x_check_dependency_status__mutmut_orig(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_1(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = None
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_2(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir * "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_3(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "XXtasksXX"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_4(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "TASKS"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_5(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = None

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_6(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = None
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_7(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(None)
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_8(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(None))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_9(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_10(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = None
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_11(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "XXunknownXX"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_12(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "UNKNOWN"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_13(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            break

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_14(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = None
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_15(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[1]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_16(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = None
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_17(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(None)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_18(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = None
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_19(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get(None, "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_20(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", None)
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_21(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_22(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", )
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_23(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("XXlaneXX", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_24(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("LANE", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_25(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "XXunknownXX")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_26(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "UNKNOWN")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_27(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = None

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_28(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "XXunknownXX"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_29(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "UNKNOWN"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_30(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = None

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_31(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(None)

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_32(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane != "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_33(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "XXdoneXX" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_34(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "DONE" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_35(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=None,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_36(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=None,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_37(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=None,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_38(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=None,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_39(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=None,
    )


def x_check_dependency_status__mutmut_40(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_41(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_42(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_43(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        is_multi_parent=len(dependencies) > 1,
    )


def x_check_dependency_status__mutmut_44(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        )


def x_check_dependency_status__mutmut_45(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) >= 1,
    )


def x_check_dependency_status__mutmut_46(
    feature_dir: Path, wp_id: str, dependencies: list[str]
) -> DependencyStatus:
    """Check status of a WP's dependencies.

    Args:
        feature_dir: Path to feature directory (kitty-specs/###-feature/)
        wp_id: Work package ID to check (e.g., "WP04")
        dependencies: List of dependency WP IDs (e.g., ["WP01", "WP02", "WP03"])

    Returns:
        DependencyStatus with analysis and recommendation
    """
    tasks_dir = feature_dir / "tasks"
    lanes = {}

    # Read lane status for each dependency
    for dep_id in dependencies:
        # Find WP file (may have slug suffix)
        wp_files = list(tasks_dir.glob(f"{dep_id}-*.md"))
        if not wp_files:
            # Dependency file not found - cannot determine status
            lanes[dep_id] = "unknown"
            continue

        wp_file = wp_files[0]
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            lanes[dep_id] = frontmatter.get("lane", "unknown")
        except Exception:
            lanes[dep_id] = "unknown"

    # Determine if all done
    all_done = all(lane == "done" for lane in lanes.values())

    return DependencyStatus(
        wp_id=wp_id,
        dependencies=dependencies,
        all_done=all_done,
        lanes=lanes,
        is_multi_parent=len(dependencies) > 2,
    )

x_check_dependency_status__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_dependency_status__mutmut_1': x_check_dependency_status__mutmut_1, 
    'x_check_dependency_status__mutmut_2': x_check_dependency_status__mutmut_2, 
    'x_check_dependency_status__mutmut_3': x_check_dependency_status__mutmut_3, 
    'x_check_dependency_status__mutmut_4': x_check_dependency_status__mutmut_4, 
    'x_check_dependency_status__mutmut_5': x_check_dependency_status__mutmut_5, 
    'x_check_dependency_status__mutmut_6': x_check_dependency_status__mutmut_6, 
    'x_check_dependency_status__mutmut_7': x_check_dependency_status__mutmut_7, 
    'x_check_dependency_status__mutmut_8': x_check_dependency_status__mutmut_8, 
    'x_check_dependency_status__mutmut_9': x_check_dependency_status__mutmut_9, 
    'x_check_dependency_status__mutmut_10': x_check_dependency_status__mutmut_10, 
    'x_check_dependency_status__mutmut_11': x_check_dependency_status__mutmut_11, 
    'x_check_dependency_status__mutmut_12': x_check_dependency_status__mutmut_12, 
    'x_check_dependency_status__mutmut_13': x_check_dependency_status__mutmut_13, 
    'x_check_dependency_status__mutmut_14': x_check_dependency_status__mutmut_14, 
    'x_check_dependency_status__mutmut_15': x_check_dependency_status__mutmut_15, 
    'x_check_dependency_status__mutmut_16': x_check_dependency_status__mutmut_16, 
    'x_check_dependency_status__mutmut_17': x_check_dependency_status__mutmut_17, 
    'x_check_dependency_status__mutmut_18': x_check_dependency_status__mutmut_18, 
    'x_check_dependency_status__mutmut_19': x_check_dependency_status__mutmut_19, 
    'x_check_dependency_status__mutmut_20': x_check_dependency_status__mutmut_20, 
    'x_check_dependency_status__mutmut_21': x_check_dependency_status__mutmut_21, 
    'x_check_dependency_status__mutmut_22': x_check_dependency_status__mutmut_22, 
    'x_check_dependency_status__mutmut_23': x_check_dependency_status__mutmut_23, 
    'x_check_dependency_status__mutmut_24': x_check_dependency_status__mutmut_24, 
    'x_check_dependency_status__mutmut_25': x_check_dependency_status__mutmut_25, 
    'x_check_dependency_status__mutmut_26': x_check_dependency_status__mutmut_26, 
    'x_check_dependency_status__mutmut_27': x_check_dependency_status__mutmut_27, 
    'x_check_dependency_status__mutmut_28': x_check_dependency_status__mutmut_28, 
    'x_check_dependency_status__mutmut_29': x_check_dependency_status__mutmut_29, 
    'x_check_dependency_status__mutmut_30': x_check_dependency_status__mutmut_30, 
    'x_check_dependency_status__mutmut_31': x_check_dependency_status__mutmut_31, 
    'x_check_dependency_status__mutmut_32': x_check_dependency_status__mutmut_32, 
    'x_check_dependency_status__mutmut_33': x_check_dependency_status__mutmut_33, 
    'x_check_dependency_status__mutmut_34': x_check_dependency_status__mutmut_34, 
    'x_check_dependency_status__mutmut_35': x_check_dependency_status__mutmut_35, 
    'x_check_dependency_status__mutmut_36': x_check_dependency_status__mutmut_36, 
    'x_check_dependency_status__mutmut_37': x_check_dependency_status__mutmut_37, 
    'x_check_dependency_status__mutmut_38': x_check_dependency_status__mutmut_38, 
    'x_check_dependency_status__mutmut_39': x_check_dependency_status__mutmut_39, 
    'x_check_dependency_status__mutmut_40': x_check_dependency_status__mutmut_40, 
    'x_check_dependency_status__mutmut_41': x_check_dependency_status__mutmut_41, 
    'x_check_dependency_status__mutmut_42': x_check_dependency_status__mutmut_42, 
    'x_check_dependency_status__mutmut_43': x_check_dependency_status__mutmut_43, 
    'x_check_dependency_status__mutmut_44': x_check_dependency_status__mutmut_44, 
    'x_check_dependency_status__mutmut_45': x_check_dependency_status__mutmut_45, 
    'x_check_dependency_status__mutmut_46': x_check_dependency_status__mutmut_46
}
x_check_dependency_status__mutmut_orig.__name__ = 'x_check_dependency_status'


def predict_merge_conflicts(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    args = [repo_root, branches, target]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_predict_merge_conflicts__mutmut_orig, x_predict_merge_conflicts__mutmut_mutants, args, kwargs, None)


def x_predict_merge_conflicts__mutmut_orig(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_1(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is not None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_2(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = None

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_3(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(None)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_4(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = None

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_5(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = None

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_6(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                None,
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_7(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=None,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_8(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=None,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_9(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=None,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_10(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding=None,
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_11(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors=None,
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_12(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=None,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_13(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_14(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_15(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_16(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_17(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_18(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_19(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_20(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["XXgitXX", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_21(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["GIT", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_22(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "XXmerge-treeXX", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_23(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "MERGE-TREE", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_24(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=False,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_25(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=False,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_26(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="XXutf-8XX",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_27(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="UTF-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_28(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="XXreplaceXX",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_29(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="REPLACE",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_30(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=True,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_31(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 and "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_32(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode == 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_33(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 1 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_34(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "XX<<<<<<<XX" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_35(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" not in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_36(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split(None):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_37(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("XX\nXX"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_38(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith(None):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_39(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("XXCONFLICTXX"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_40(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("conflict"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_41(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if "XX in XX" in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_42(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " IN " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_43(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " not in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_44(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = None
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_45(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(None)[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_46(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split("XX in XX")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_47(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" IN ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_48(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[+1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_49(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-2].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_50(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_51(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = None
                            conflicts[file_path].append(branch)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts


def x_predict_merge_conflicts__mutmut_52(
    repo_root: Path, branches: list[str], target: str | None = None
) -> dict[str, list[str]]:
    """Predict which files will conflict when merging branches.

    Uses git merge-tree to simulate merge without touching working directory.

    Args:
        repo_root: Repository root path
        branches: List of branches to merge (e.g., ["WP01", "WP02", "WP03"])
        target: Target branch to merge into (default: "main")

    Returns:
        Dict mapping file paths to list of conflicting branches
        Example: {".gitignore": ["WP01", "WP02", "WP03"]}
    """
    import subprocess

    if target is None:
        from specify_cli.core.git_ops import resolve_primary_branch
        target = resolve_primary_branch(repo_root)

    conflicts = {}

    # Check each branch against target
    for branch in branches:
        try:
            # git merge-tree: simulate merge without touching working tree
            result = subprocess.run(
                ["git", "merge-tree", target, branch],
                cwd=repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            # Parse output for conflict markers
            if result.returncode != 0 or "<<<<<<<" in result.stdout:
                # Has conflicts - parse which files
                for line in result.stdout.split("\n"):
                    if line.startswith("CONFLICT"):
                        # Example: "CONFLICT (add/add): Merge conflict in .gitignore"
                        if " in " in line:
                            file_path = line.split(" in ")[-1].strip()
                            if file_path not in conflicts:
                                conflicts[file_path] = []
                            conflicts[file_path].append(None)

        except Exception:
            # merge-tree failed or not available - skip prediction
            pass

    return conflicts

x_predict_merge_conflicts__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_predict_merge_conflicts__mutmut_1': x_predict_merge_conflicts__mutmut_1, 
    'x_predict_merge_conflicts__mutmut_2': x_predict_merge_conflicts__mutmut_2, 
    'x_predict_merge_conflicts__mutmut_3': x_predict_merge_conflicts__mutmut_3, 
    'x_predict_merge_conflicts__mutmut_4': x_predict_merge_conflicts__mutmut_4, 
    'x_predict_merge_conflicts__mutmut_5': x_predict_merge_conflicts__mutmut_5, 
    'x_predict_merge_conflicts__mutmut_6': x_predict_merge_conflicts__mutmut_6, 
    'x_predict_merge_conflicts__mutmut_7': x_predict_merge_conflicts__mutmut_7, 
    'x_predict_merge_conflicts__mutmut_8': x_predict_merge_conflicts__mutmut_8, 
    'x_predict_merge_conflicts__mutmut_9': x_predict_merge_conflicts__mutmut_9, 
    'x_predict_merge_conflicts__mutmut_10': x_predict_merge_conflicts__mutmut_10, 
    'x_predict_merge_conflicts__mutmut_11': x_predict_merge_conflicts__mutmut_11, 
    'x_predict_merge_conflicts__mutmut_12': x_predict_merge_conflicts__mutmut_12, 
    'x_predict_merge_conflicts__mutmut_13': x_predict_merge_conflicts__mutmut_13, 
    'x_predict_merge_conflicts__mutmut_14': x_predict_merge_conflicts__mutmut_14, 
    'x_predict_merge_conflicts__mutmut_15': x_predict_merge_conflicts__mutmut_15, 
    'x_predict_merge_conflicts__mutmut_16': x_predict_merge_conflicts__mutmut_16, 
    'x_predict_merge_conflicts__mutmut_17': x_predict_merge_conflicts__mutmut_17, 
    'x_predict_merge_conflicts__mutmut_18': x_predict_merge_conflicts__mutmut_18, 
    'x_predict_merge_conflicts__mutmut_19': x_predict_merge_conflicts__mutmut_19, 
    'x_predict_merge_conflicts__mutmut_20': x_predict_merge_conflicts__mutmut_20, 
    'x_predict_merge_conflicts__mutmut_21': x_predict_merge_conflicts__mutmut_21, 
    'x_predict_merge_conflicts__mutmut_22': x_predict_merge_conflicts__mutmut_22, 
    'x_predict_merge_conflicts__mutmut_23': x_predict_merge_conflicts__mutmut_23, 
    'x_predict_merge_conflicts__mutmut_24': x_predict_merge_conflicts__mutmut_24, 
    'x_predict_merge_conflicts__mutmut_25': x_predict_merge_conflicts__mutmut_25, 
    'x_predict_merge_conflicts__mutmut_26': x_predict_merge_conflicts__mutmut_26, 
    'x_predict_merge_conflicts__mutmut_27': x_predict_merge_conflicts__mutmut_27, 
    'x_predict_merge_conflicts__mutmut_28': x_predict_merge_conflicts__mutmut_28, 
    'x_predict_merge_conflicts__mutmut_29': x_predict_merge_conflicts__mutmut_29, 
    'x_predict_merge_conflicts__mutmut_30': x_predict_merge_conflicts__mutmut_30, 
    'x_predict_merge_conflicts__mutmut_31': x_predict_merge_conflicts__mutmut_31, 
    'x_predict_merge_conflicts__mutmut_32': x_predict_merge_conflicts__mutmut_32, 
    'x_predict_merge_conflicts__mutmut_33': x_predict_merge_conflicts__mutmut_33, 
    'x_predict_merge_conflicts__mutmut_34': x_predict_merge_conflicts__mutmut_34, 
    'x_predict_merge_conflicts__mutmut_35': x_predict_merge_conflicts__mutmut_35, 
    'x_predict_merge_conflicts__mutmut_36': x_predict_merge_conflicts__mutmut_36, 
    'x_predict_merge_conflicts__mutmut_37': x_predict_merge_conflicts__mutmut_37, 
    'x_predict_merge_conflicts__mutmut_38': x_predict_merge_conflicts__mutmut_38, 
    'x_predict_merge_conflicts__mutmut_39': x_predict_merge_conflicts__mutmut_39, 
    'x_predict_merge_conflicts__mutmut_40': x_predict_merge_conflicts__mutmut_40, 
    'x_predict_merge_conflicts__mutmut_41': x_predict_merge_conflicts__mutmut_41, 
    'x_predict_merge_conflicts__mutmut_42': x_predict_merge_conflicts__mutmut_42, 
    'x_predict_merge_conflicts__mutmut_43': x_predict_merge_conflicts__mutmut_43, 
    'x_predict_merge_conflicts__mutmut_44': x_predict_merge_conflicts__mutmut_44, 
    'x_predict_merge_conflicts__mutmut_45': x_predict_merge_conflicts__mutmut_45, 
    'x_predict_merge_conflicts__mutmut_46': x_predict_merge_conflicts__mutmut_46, 
    'x_predict_merge_conflicts__mutmut_47': x_predict_merge_conflicts__mutmut_47, 
    'x_predict_merge_conflicts__mutmut_48': x_predict_merge_conflicts__mutmut_48, 
    'x_predict_merge_conflicts__mutmut_49': x_predict_merge_conflicts__mutmut_49, 
    'x_predict_merge_conflicts__mutmut_50': x_predict_merge_conflicts__mutmut_50, 
    'x_predict_merge_conflicts__mutmut_51': x_predict_merge_conflicts__mutmut_51, 
    'x_predict_merge_conflicts__mutmut_52': x_predict_merge_conflicts__mutmut_52
}
x_predict_merge_conflicts__mutmut_orig.__name__ = 'x_predict_merge_conflicts'


def get_merge_strategy_recommendation(status: DependencyStatus) -> dict:
    args = [status]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_merge_strategy_recommendation__mutmut_orig, x_get_merge_strategy_recommendation__mutmut_mutants, args, kwargs, None)


def x_get_merge_strategy_recommendation__mutmut_orig(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_1(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_2(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "XXstrategyXX": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_3(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "STRATEGY": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_4(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "XXno_dependenciesXX",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_5(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "NO_DEPENDENCIES",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_6(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "XXreasonXX": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_7(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "REASON": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_8(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "XXNo dependencies to resolveXX",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_9(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "no dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_10(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "NO DEPENDENCIES TO RESOLVE",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_11(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "XXcommandXX": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_12(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "COMMAND": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_13(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "XXwarningsXX": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_14(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "WARNINGS": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_15(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_16(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = None
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_17(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane == "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_18(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "XXdoneXX"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_19(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "DONE"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_20(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "XXstrategyXX": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_21(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "STRATEGY": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_22(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "XXwaitXX",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_23(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "WAIT",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_24(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "XXreasonXX": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_25(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "REASON": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_26(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(None)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_27(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {'XX, XX'.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_28(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "XXcommandXX": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_29(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "COMMAND": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_30(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "XXwarningsXX": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_31(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "WARNINGS": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_32(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(None)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_33(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {'XX, XX'.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_34(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) != 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_35(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 2:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_36(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = None
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_37(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[1]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_38(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "XXstrategyXX": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_39(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "STRATEGY": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_40(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "XXuse_baseXX",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_41(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "USE_BASE",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_42(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "XXreasonXX": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_43(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "REASON": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_44(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "XXcommandXX": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_45(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "COMMAND": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_46(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "XXwarningsXX": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_47(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "WARNINGS": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_48(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "XXstrategyXX": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_49(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "STRATEGY": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_50(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "XXmerge_firstXX",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_51(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "MERGE_FIRST",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_52(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "XXreasonXX": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_53(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "REASON": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_54(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(None)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_55(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({'XX, XX'.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_56(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "XXcommandXX": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_57(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "COMMAND": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_58(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "XXspec-kitty merge --feature <feature-slug>XX",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_59(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "SPEC-KITTY MERGE --FEATURE <FEATURE-SLUG>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_60(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "XXwarningsXX": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_61(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "WARNINGS": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_62(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "XXAuto-merge may conflict on shared files (.gitignore, package.json)XX",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_63(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "auto-merge may conflict on shared files (.gitignore, package.json)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_64(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "AUTO-MERGE MAY CONFLICT ON SHARED FILES (.GITIGNORE, PACKAGE.JSON)",
            "Merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_65(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "XXMerging dependencies to main first is saferXX",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_66(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "merging dependencies to main first is safer",
        ],
    }


def x_get_merge_strategy_recommendation__mutmut_67(status: DependencyStatus) -> dict:
    """Get recommended merge strategy for dependencies.

    Args:
        status: DependencyStatus from check_dependency_status()

    Returns:
        Dict with recommendation details:
        {
            "strategy": "merge_first" | "auto_merge" | "use_base" | "wait",
            "reason": "...",
            "command": "...",
            "warnings": [...]
        }
    """
    if not status.dependencies:
        return {
            "strategy": "no_dependencies",
            "reason": "No dependencies to resolve",
            "command": f"spec-kitty implement {status.wp_id}",
            "warnings": [],
        }

    if not status.all_done:
        not_done = [dep for dep, lane in status.lanes.items() if lane != "done"]
        return {
            "strategy": "wait",
            "reason": f"Dependencies not complete: {', '.join(not_done)}",
            "command": None,
            "warnings": [f"Complete {', '.join(not_done)} before implementing {status.wp_id}"],
        }

    if len(status.dependencies) == 1:
        dep = status.dependencies[0]
        return {
            "strategy": "use_base",
            "reason": f"Single dependency ({dep}) - use --base flag",
            "command": f"spec-kitty implement {status.wp_id} --base {dep}",
            "warnings": [],
        }

    # Multi-parent, all done
    return {
        "strategy": "merge_first",
        "reason": f"Multi-parent dependencies ({', '.join(status.dependencies)}) all done",
        "command": "spec-kitty merge --feature <feature-slug>",
        "warnings": [
            "Auto-merge may conflict on shared files (.gitignore, package.json)",
            "MERGING DEPENDENCIES TO MAIN FIRST IS SAFER",
        ],
    }

x_get_merge_strategy_recommendation__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_merge_strategy_recommendation__mutmut_1': x_get_merge_strategy_recommendation__mutmut_1, 
    'x_get_merge_strategy_recommendation__mutmut_2': x_get_merge_strategy_recommendation__mutmut_2, 
    'x_get_merge_strategy_recommendation__mutmut_3': x_get_merge_strategy_recommendation__mutmut_3, 
    'x_get_merge_strategy_recommendation__mutmut_4': x_get_merge_strategy_recommendation__mutmut_4, 
    'x_get_merge_strategy_recommendation__mutmut_5': x_get_merge_strategy_recommendation__mutmut_5, 
    'x_get_merge_strategy_recommendation__mutmut_6': x_get_merge_strategy_recommendation__mutmut_6, 
    'x_get_merge_strategy_recommendation__mutmut_7': x_get_merge_strategy_recommendation__mutmut_7, 
    'x_get_merge_strategy_recommendation__mutmut_8': x_get_merge_strategy_recommendation__mutmut_8, 
    'x_get_merge_strategy_recommendation__mutmut_9': x_get_merge_strategy_recommendation__mutmut_9, 
    'x_get_merge_strategy_recommendation__mutmut_10': x_get_merge_strategy_recommendation__mutmut_10, 
    'x_get_merge_strategy_recommendation__mutmut_11': x_get_merge_strategy_recommendation__mutmut_11, 
    'x_get_merge_strategy_recommendation__mutmut_12': x_get_merge_strategy_recommendation__mutmut_12, 
    'x_get_merge_strategy_recommendation__mutmut_13': x_get_merge_strategy_recommendation__mutmut_13, 
    'x_get_merge_strategy_recommendation__mutmut_14': x_get_merge_strategy_recommendation__mutmut_14, 
    'x_get_merge_strategy_recommendation__mutmut_15': x_get_merge_strategy_recommendation__mutmut_15, 
    'x_get_merge_strategy_recommendation__mutmut_16': x_get_merge_strategy_recommendation__mutmut_16, 
    'x_get_merge_strategy_recommendation__mutmut_17': x_get_merge_strategy_recommendation__mutmut_17, 
    'x_get_merge_strategy_recommendation__mutmut_18': x_get_merge_strategy_recommendation__mutmut_18, 
    'x_get_merge_strategy_recommendation__mutmut_19': x_get_merge_strategy_recommendation__mutmut_19, 
    'x_get_merge_strategy_recommendation__mutmut_20': x_get_merge_strategy_recommendation__mutmut_20, 
    'x_get_merge_strategy_recommendation__mutmut_21': x_get_merge_strategy_recommendation__mutmut_21, 
    'x_get_merge_strategy_recommendation__mutmut_22': x_get_merge_strategy_recommendation__mutmut_22, 
    'x_get_merge_strategy_recommendation__mutmut_23': x_get_merge_strategy_recommendation__mutmut_23, 
    'x_get_merge_strategy_recommendation__mutmut_24': x_get_merge_strategy_recommendation__mutmut_24, 
    'x_get_merge_strategy_recommendation__mutmut_25': x_get_merge_strategy_recommendation__mutmut_25, 
    'x_get_merge_strategy_recommendation__mutmut_26': x_get_merge_strategy_recommendation__mutmut_26, 
    'x_get_merge_strategy_recommendation__mutmut_27': x_get_merge_strategy_recommendation__mutmut_27, 
    'x_get_merge_strategy_recommendation__mutmut_28': x_get_merge_strategy_recommendation__mutmut_28, 
    'x_get_merge_strategy_recommendation__mutmut_29': x_get_merge_strategy_recommendation__mutmut_29, 
    'x_get_merge_strategy_recommendation__mutmut_30': x_get_merge_strategy_recommendation__mutmut_30, 
    'x_get_merge_strategy_recommendation__mutmut_31': x_get_merge_strategy_recommendation__mutmut_31, 
    'x_get_merge_strategy_recommendation__mutmut_32': x_get_merge_strategy_recommendation__mutmut_32, 
    'x_get_merge_strategy_recommendation__mutmut_33': x_get_merge_strategy_recommendation__mutmut_33, 
    'x_get_merge_strategy_recommendation__mutmut_34': x_get_merge_strategy_recommendation__mutmut_34, 
    'x_get_merge_strategy_recommendation__mutmut_35': x_get_merge_strategy_recommendation__mutmut_35, 
    'x_get_merge_strategy_recommendation__mutmut_36': x_get_merge_strategy_recommendation__mutmut_36, 
    'x_get_merge_strategy_recommendation__mutmut_37': x_get_merge_strategy_recommendation__mutmut_37, 
    'x_get_merge_strategy_recommendation__mutmut_38': x_get_merge_strategy_recommendation__mutmut_38, 
    'x_get_merge_strategy_recommendation__mutmut_39': x_get_merge_strategy_recommendation__mutmut_39, 
    'x_get_merge_strategy_recommendation__mutmut_40': x_get_merge_strategy_recommendation__mutmut_40, 
    'x_get_merge_strategy_recommendation__mutmut_41': x_get_merge_strategy_recommendation__mutmut_41, 
    'x_get_merge_strategy_recommendation__mutmut_42': x_get_merge_strategy_recommendation__mutmut_42, 
    'x_get_merge_strategy_recommendation__mutmut_43': x_get_merge_strategy_recommendation__mutmut_43, 
    'x_get_merge_strategy_recommendation__mutmut_44': x_get_merge_strategy_recommendation__mutmut_44, 
    'x_get_merge_strategy_recommendation__mutmut_45': x_get_merge_strategy_recommendation__mutmut_45, 
    'x_get_merge_strategy_recommendation__mutmut_46': x_get_merge_strategy_recommendation__mutmut_46, 
    'x_get_merge_strategy_recommendation__mutmut_47': x_get_merge_strategy_recommendation__mutmut_47, 
    'x_get_merge_strategy_recommendation__mutmut_48': x_get_merge_strategy_recommendation__mutmut_48, 
    'x_get_merge_strategy_recommendation__mutmut_49': x_get_merge_strategy_recommendation__mutmut_49, 
    'x_get_merge_strategy_recommendation__mutmut_50': x_get_merge_strategy_recommendation__mutmut_50, 
    'x_get_merge_strategy_recommendation__mutmut_51': x_get_merge_strategy_recommendation__mutmut_51, 
    'x_get_merge_strategy_recommendation__mutmut_52': x_get_merge_strategy_recommendation__mutmut_52, 
    'x_get_merge_strategy_recommendation__mutmut_53': x_get_merge_strategy_recommendation__mutmut_53, 
    'x_get_merge_strategy_recommendation__mutmut_54': x_get_merge_strategy_recommendation__mutmut_54, 
    'x_get_merge_strategy_recommendation__mutmut_55': x_get_merge_strategy_recommendation__mutmut_55, 
    'x_get_merge_strategy_recommendation__mutmut_56': x_get_merge_strategy_recommendation__mutmut_56, 
    'x_get_merge_strategy_recommendation__mutmut_57': x_get_merge_strategy_recommendation__mutmut_57, 
    'x_get_merge_strategy_recommendation__mutmut_58': x_get_merge_strategy_recommendation__mutmut_58, 
    'x_get_merge_strategy_recommendation__mutmut_59': x_get_merge_strategy_recommendation__mutmut_59, 
    'x_get_merge_strategy_recommendation__mutmut_60': x_get_merge_strategy_recommendation__mutmut_60, 
    'x_get_merge_strategy_recommendation__mutmut_61': x_get_merge_strategy_recommendation__mutmut_61, 
    'x_get_merge_strategy_recommendation__mutmut_62': x_get_merge_strategy_recommendation__mutmut_62, 
    'x_get_merge_strategy_recommendation__mutmut_63': x_get_merge_strategy_recommendation__mutmut_63, 
    'x_get_merge_strategy_recommendation__mutmut_64': x_get_merge_strategy_recommendation__mutmut_64, 
    'x_get_merge_strategy_recommendation__mutmut_65': x_get_merge_strategy_recommendation__mutmut_65, 
    'x_get_merge_strategy_recommendation__mutmut_66': x_get_merge_strategy_recommendation__mutmut_66, 
    'x_get_merge_strategy_recommendation__mutmut_67': x_get_merge_strategy_recommendation__mutmut_67
}
x_get_merge_strategy_recommendation__mutmut_orig.__name__ = 'x_get_merge_strategy_recommendation'
