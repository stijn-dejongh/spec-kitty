"""Merge ordering based on WP dependencies.

Implements FR-008 through FR-011: determining merge order via topological
sort of the dependency graph.
"""

from __future__ import annotations

import logging
from pathlib import Path

from specify_cli.core.dependency_graph import (
    build_dependency_graph,
    detect_cycles,
    topological_sort,
)

__all__ = ["get_merge_order", "MergeOrderError", "has_dependency_info", "display_merge_order"]

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


class MergeOrderError(Exception):
    """Error determining merge order."""

    pass


def has_dependency_info(graph: dict[str, list[str]]) -> bool:
    args = [graph]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_has_dependency_info__mutmut_orig, x_has_dependency_info__mutmut_mutants, args, kwargs, None)


def x_has_dependency_info__mutmut_orig(graph: dict[str, list[str]]) -> bool:
    """Check if any WP has declared dependencies.

    Args:
        graph: Dependency graph mapping WP ID to list of dependencies

    Returns:
        True if at least one WP has non-empty dependencies
    """
    return any(deps for deps in graph.values())


def x_has_dependency_info__mutmut_1(graph: dict[str, list[str]]) -> bool:
    """Check if any WP has declared dependencies.

    Args:
        graph: Dependency graph mapping WP ID to list of dependencies

    Returns:
        True if at least one WP has non-empty dependencies
    """
    return any(None)

x_has_dependency_info__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_has_dependency_info__mutmut_1': x_has_dependency_info__mutmut_1
}
x_has_dependency_info__mutmut_orig.__name__ = 'x_has_dependency_info'


def get_merge_order(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    args = [wp_workspaces, feature_dir]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_merge_order__mutmut_orig, x_get_merge_order__mutmut_mutants, args, kwargs, None)


def x_get_merge_order__mutmut_orig(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_1(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_2(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = None

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_3(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = None

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_4(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(None)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_5(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_6(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = None  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_7(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_8(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(None):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_9(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            None
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_10(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "XXNo dependency information found in WP frontmatter. XX"
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_11(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "no dependency information found in wp frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_12(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "NO DEPENDENCY INFORMATION FOUND IN WP FRONTMATTER. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_13(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "XXFalling back to numerical order (WP01, WP02, ...).XX"
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_14(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "falling back to numerical order (wp01, wp02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_15(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "FALLING BACK TO NUMERICAL ORDER (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_16(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(None, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_17(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=None)  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_18(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_19(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, )  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_20(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: None)  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_21(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[2])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_22(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = None
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_23(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(None)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_24(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = None
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_25(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[1]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_26(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = None
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_27(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(None)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_28(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = "XX → XX".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_29(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            None
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_30(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "XXFix the dependencies in the WP frontmatter to remove this cycle.XX"
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_31(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "fix the dependencies in the wp frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_32(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "FIX THE DEPENDENCIES IN THE WP FRONTMATTER TO REMOVE THIS CYCLE."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_33(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = None
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_34(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(None)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_35(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(None) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_36(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(None)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_37(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = None
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_38(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id not in wp_map:
            result.append(wp_map[wp_id])

    return result


def x_get_merge_order__mutmut_39(
    wp_workspaces: list[tuple[Path, str, str]],
    feature_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return WPs in dependency order (topological sort).

    Determines the optimal merge order based on WP dependencies declared
    in frontmatter. WPs with dependencies will be merged after their
    dependencies.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        feature_dir: Path to feature directory containing tasks/

    Returns:
        Same tuples reordered by dependency (dependencies first)

    Raises:
        MergeOrderError: If circular dependency detected
    """
    if not wp_workspaces:
        return []

    # Build WP ID → workspace mapping
    wp_map = {wp_id: (path, wp_id, branch) for path, wp_id, branch in wp_workspaces}

    # Build dependency graph from task frontmatter
    graph = build_dependency_graph(feature_dir)

    # Check for missing WPs in graph (may have no frontmatter)
    for wp_id in wp_map:
        if wp_id not in graph:
            graph[wp_id] = []  # No dependencies

    # Check if we have any dependency info
    if not has_dependency_info(graph):
        # No dependency info - fall back to numerical order with warning
        logger.warning(
            "No dependency information found in WP frontmatter. "
            "Falling back to numerical order (WP01, WP02, ...)."
        )
        return sorted(wp_workspaces, key=lambda x: x[1])  # Sort by wp_id

    # Detect cycles - show full cycle path in error
    cycles = detect_cycles(graph)
    if cycles:
        # Format the cycle path clearly: WP01 → WP02 → WP03 → WP01
        cycle = cycles[0]
        cycle_str = " → ".join(cycle)
        raise MergeOrderError(
            f"Circular dependency detected: {cycle_str}\n"
            "Fix the dependencies in the WP frontmatter to remove this cycle."
        )

    # Topological sort
    try:
        ordered_ids = topological_sort(graph)
    except ValueError as e:
        raise MergeOrderError(str(e)) from e

    # Filter to only WPs we have workspaces for, maintaining order
    result = []
    for wp_id in ordered_ids:
        if wp_id in wp_map:
            result.append(None)

    return result

x_get_merge_order__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_merge_order__mutmut_1': x_get_merge_order__mutmut_1, 
    'x_get_merge_order__mutmut_2': x_get_merge_order__mutmut_2, 
    'x_get_merge_order__mutmut_3': x_get_merge_order__mutmut_3, 
    'x_get_merge_order__mutmut_4': x_get_merge_order__mutmut_4, 
    'x_get_merge_order__mutmut_5': x_get_merge_order__mutmut_5, 
    'x_get_merge_order__mutmut_6': x_get_merge_order__mutmut_6, 
    'x_get_merge_order__mutmut_7': x_get_merge_order__mutmut_7, 
    'x_get_merge_order__mutmut_8': x_get_merge_order__mutmut_8, 
    'x_get_merge_order__mutmut_9': x_get_merge_order__mutmut_9, 
    'x_get_merge_order__mutmut_10': x_get_merge_order__mutmut_10, 
    'x_get_merge_order__mutmut_11': x_get_merge_order__mutmut_11, 
    'x_get_merge_order__mutmut_12': x_get_merge_order__mutmut_12, 
    'x_get_merge_order__mutmut_13': x_get_merge_order__mutmut_13, 
    'x_get_merge_order__mutmut_14': x_get_merge_order__mutmut_14, 
    'x_get_merge_order__mutmut_15': x_get_merge_order__mutmut_15, 
    'x_get_merge_order__mutmut_16': x_get_merge_order__mutmut_16, 
    'x_get_merge_order__mutmut_17': x_get_merge_order__mutmut_17, 
    'x_get_merge_order__mutmut_18': x_get_merge_order__mutmut_18, 
    'x_get_merge_order__mutmut_19': x_get_merge_order__mutmut_19, 
    'x_get_merge_order__mutmut_20': x_get_merge_order__mutmut_20, 
    'x_get_merge_order__mutmut_21': x_get_merge_order__mutmut_21, 
    'x_get_merge_order__mutmut_22': x_get_merge_order__mutmut_22, 
    'x_get_merge_order__mutmut_23': x_get_merge_order__mutmut_23, 
    'x_get_merge_order__mutmut_24': x_get_merge_order__mutmut_24, 
    'x_get_merge_order__mutmut_25': x_get_merge_order__mutmut_25, 
    'x_get_merge_order__mutmut_26': x_get_merge_order__mutmut_26, 
    'x_get_merge_order__mutmut_27': x_get_merge_order__mutmut_27, 
    'x_get_merge_order__mutmut_28': x_get_merge_order__mutmut_28, 
    'x_get_merge_order__mutmut_29': x_get_merge_order__mutmut_29, 
    'x_get_merge_order__mutmut_30': x_get_merge_order__mutmut_30, 
    'x_get_merge_order__mutmut_31': x_get_merge_order__mutmut_31, 
    'x_get_merge_order__mutmut_32': x_get_merge_order__mutmut_32, 
    'x_get_merge_order__mutmut_33': x_get_merge_order__mutmut_33, 
    'x_get_merge_order__mutmut_34': x_get_merge_order__mutmut_34, 
    'x_get_merge_order__mutmut_35': x_get_merge_order__mutmut_35, 
    'x_get_merge_order__mutmut_36': x_get_merge_order__mutmut_36, 
    'x_get_merge_order__mutmut_37': x_get_merge_order__mutmut_37, 
    'x_get_merge_order__mutmut_38': x_get_merge_order__mutmut_38, 
    'x_get_merge_order__mutmut_39': x_get_merge_order__mutmut_39
}
x_get_merge_order__mutmut_orig.__name__ = 'x_get_merge_order'


def display_merge_order(
    ordered_workspaces: list[tuple[Path, str, str]],
    console,
) -> None:
    args = [ordered_workspaces, console]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_display_merge_order__mutmut_orig, x_display_merge_order__mutmut_mutants, args, kwargs, None)


def x_display_merge_order__mutmut_orig(
    ordered_workspaces: list[tuple[Path, str, str]],
    console,
) -> None:
    """Display the merge order to the user.

    Args:
        ordered_workspaces: Ordered list of (path, wp_id, branch) tuples
        console: Rich Console for output
    """
    if not ordered_workspaces:
        return

    console.print("\n[bold]Merge Order[/bold] (dependency-based):\n")
    for i, (_, wp_id, branch) in enumerate(ordered_workspaces, 1):
        console.print(f"  {i}. {wp_id} ({branch})")
    console.print()


def x_display_merge_order__mutmut_1(
    ordered_workspaces: list[tuple[Path, str, str]],
    console,
) -> None:
    """Display the merge order to the user.

    Args:
        ordered_workspaces: Ordered list of (path, wp_id, branch) tuples
        console: Rich Console for output
    """
    if ordered_workspaces:
        return

    console.print("\n[bold]Merge Order[/bold] (dependency-based):\n")
    for i, (_, wp_id, branch) in enumerate(ordered_workspaces, 1):
        console.print(f"  {i}. {wp_id} ({branch})")
    console.print()


def x_display_merge_order__mutmut_2(
    ordered_workspaces: list[tuple[Path, str, str]],
    console,
) -> None:
    """Display the merge order to the user.

    Args:
        ordered_workspaces: Ordered list of (path, wp_id, branch) tuples
        console: Rich Console for output
    """
    if not ordered_workspaces:
        return

    console.print(None)
    for i, (_, wp_id, branch) in enumerate(ordered_workspaces, 1):
        console.print(f"  {i}. {wp_id} ({branch})")
    console.print()


def x_display_merge_order__mutmut_3(
    ordered_workspaces: list[tuple[Path, str, str]],
    console,
) -> None:
    """Display the merge order to the user.

    Args:
        ordered_workspaces: Ordered list of (path, wp_id, branch) tuples
        console: Rich Console for output
    """
    if not ordered_workspaces:
        return

    console.print("XX\n[bold]Merge Order[/bold] (dependency-based):\nXX")
    for i, (_, wp_id, branch) in enumerate(ordered_workspaces, 1):
        console.print(f"  {i}. {wp_id} ({branch})")
    console.print()


def x_display_merge_order__mutmut_4(
    ordered_workspaces: list[tuple[Path, str, str]],
    console,
) -> None:
    """Display the merge order to the user.

    Args:
        ordered_workspaces: Ordered list of (path, wp_id, branch) tuples
        console: Rich Console for output
    """
    if not ordered_workspaces:
        return

    console.print("\n[bold]merge order[/bold] (dependency-based):\n")
    for i, (_, wp_id, branch) in enumerate(ordered_workspaces, 1):
        console.print(f"  {i}. {wp_id} ({branch})")
    console.print()


def x_display_merge_order__mutmut_5(
    ordered_workspaces: list[tuple[Path, str, str]],
    console,
) -> None:
    """Display the merge order to the user.

    Args:
        ordered_workspaces: Ordered list of (path, wp_id, branch) tuples
        console: Rich Console for output
    """
    if not ordered_workspaces:
        return

    console.print("\n[BOLD]MERGE ORDER[/BOLD] (DEPENDENCY-BASED):\n")
    for i, (_, wp_id, branch) in enumerate(ordered_workspaces, 1):
        console.print(f"  {i}. {wp_id} ({branch})")
    console.print()


def x_display_merge_order__mutmut_6(
    ordered_workspaces: list[tuple[Path, str, str]],
    console,
) -> None:
    """Display the merge order to the user.

    Args:
        ordered_workspaces: Ordered list of (path, wp_id, branch) tuples
        console: Rich Console for output
    """
    if not ordered_workspaces:
        return

    console.print("\n[bold]Merge Order[/bold] (dependency-based):\n")
    for i, (_, wp_id, branch) in enumerate(None, 1):
        console.print(f"  {i}. {wp_id} ({branch})")
    console.print()


def x_display_merge_order__mutmut_7(
    ordered_workspaces: list[tuple[Path, str, str]],
    console,
) -> None:
    """Display the merge order to the user.

    Args:
        ordered_workspaces: Ordered list of (path, wp_id, branch) tuples
        console: Rich Console for output
    """
    if not ordered_workspaces:
        return

    console.print("\n[bold]Merge Order[/bold] (dependency-based):\n")
    for i, (_, wp_id, branch) in enumerate(ordered_workspaces, None):
        console.print(f"  {i}. {wp_id} ({branch})")
    console.print()


def x_display_merge_order__mutmut_8(
    ordered_workspaces: list[tuple[Path, str, str]],
    console,
) -> None:
    """Display the merge order to the user.

    Args:
        ordered_workspaces: Ordered list of (path, wp_id, branch) tuples
        console: Rich Console for output
    """
    if not ordered_workspaces:
        return

    console.print("\n[bold]Merge Order[/bold] (dependency-based):\n")
    for i, (_, wp_id, branch) in enumerate(1):
        console.print(f"  {i}. {wp_id} ({branch})")
    console.print()


def x_display_merge_order__mutmut_9(
    ordered_workspaces: list[tuple[Path, str, str]],
    console,
) -> None:
    """Display the merge order to the user.

    Args:
        ordered_workspaces: Ordered list of (path, wp_id, branch) tuples
        console: Rich Console for output
    """
    if not ordered_workspaces:
        return

    console.print("\n[bold]Merge Order[/bold] (dependency-based):\n")
    for i, (_, wp_id, branch) in enumerate(ordered_workspaces, ):
        console.print(f"  {i}. {wp_id} ({branch})")
    console.print()


def x_display_merge_order__mutmut_10(
    ordered_workspaces: list[tuple[Path, str, str]],
    console,
) -> None:
    """Display the merge order to the user.

    Args:
        ordered_workspaces: Ordered list of (path, wp_id, branch) tuples
        console: Rich Console for output
    """
    if not ordered_workspaces:
        return

    console.print("\n[bold]Merge Order[/bold] (dependency-based):\n")
    for i, (_, wp_id, branch) in enumerate(ordered_workspaces, 2):
        console.print(f"  {i}. {wp_id} ({branch})")
    console.print()


def x_display_merge_order__mutmut_11(
    ordered_workspaces: list[tuple[Path, str, str]],
    console,
) -> None:
    """Display the merge order to the user.

    Args:
        ordered_workspaces: Ordered list of (path, wp_id, branch) tuples
        console: Rich Console for output
    """
    if not ordered_workspaces:
        return

    console.print("\n[bold]Merge Order[/bold] (dependency-based):\n")
    for i, (_, wp_id, branch) in enumerate(ordered_workspaces, 1):
        console.print(None)
    console.print()

x_display_merge_order__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_display_merge_order__mutmut_1': x_display_merge_order__mutmut_1, 
    'x_display_merge_order__mutmut_2': x_display_merge_order__mutmut_2, 
    'x_display_merge_order__mutmut_3': x_display_merge_order__mutmut_3, 
    'x_display_merge_order__mutmut_4': x_display_merge_order__mutmut_4, 
    'x_display_merge_order__mutmut_5': x_display_merge_order__mutmut_5, 
    'x_display_merge_order__mutmut_6': x_display_merge_order__mutmut_6, 
    'x_display_merge_order__mutmut_7': x_display_merge_order__mutmut_7, 
    'x_display_merge_order__mutmut_8': x_display_merge_order__mutmut_8, 
    'x_display_merge_order__mutmut_9': x_display_merge_order__mutmut_9, 
    'x_display_merge_order__mutmut_10': x_display_merge_order__mutmut_10, 
    'x_display_merge_order__mutmut_11': x_display_merge_order__mutmut_11
}
x_display_merge_order__mutmut_orig.__name__ = 'x_display_merge_order'
