"""Dependency graph utilities for work package relationships.

This module provides functions for parsing, validating, and analyzing
dependency relationships between work packages in Spec Kitty features.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from specify_cli.frontmatter import FrontmatterError, read_frontmatter
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


def parse_wp_dependencies(wp_file: Path) -> list[str]:
    args = [wp_file]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_parse_wp_dependencies__mutmut_orig, x_parse_wp_dependencies__mutmut_mutants, args, kwargs, None)


def x_parse_wp_dependencies__mutmut_orig(wp_file: Path) -> list[str]:
    """Parse dependencies from WP frontmatter.

    Uses FrontmatterManager for consistent parsing across CLI.

    Args:
        wp_file: Path to work package markdown file

    Returns:
        List of WP IDs this WP depends on (e.g., ["WP01", "WP02"])
        Returns empty list if no dependencies or parsing fails

    Examples:
        >>> wp_file = Path("tasks/WP02.md")
        >>> deps = parse_wp_dependencies(wp_file)
        >>> print(deps)  # ["WP01"]
    """
    try:
        # Use FrontmatterManager for consistent parsing
        frontmatter, _ = read_frontmatter(wp_file)

        # Extract dependencies field (FrontmatterManager already defaults to [])
        dependencies = frontmatter.get("dependencies", [])

        # Validate dependencies is a list
        if not isinstance(dependencies, list):
            return []

        return dependencies

    except (FrontmatterError, OSError):
        # Return empty list on any parsing error
        return []


def x_parse_wp_dependencies__mutmut_1(wp_file: Path) -> list[str]:
    """Parse dependencies from WP frontmatter.

    Uses FrontmatterManager for consistent parsing across CLI.

    Args:
        wp_file: Path to work package markdown file

    Returns:
        List of WP IDs this WP depends on (e.g., ["WP01", "WP02"])
        Returns empty list if no dependencies or parsing fails

    Examples:
        >>> wp_file = Path("tasks/WP02.md")
        >>> deps = parse_wp_dependencies(wp_file)
        >>> print(deps)  # ["WP01"]
    """
    try:
        # Use FrontmatterManager for consistent parsing
        frontmatter, _ = None

        # Extract dependencies field (FrontmatterManager already defaults to [])
        dependencies = frontmatter.get("dependencies", [])

        # Validate dependencies is a list
        if not isinstance(dependencies, list):
            return []

        return dependencies

    except (FrontmatterError, OSError):
        # Return empty list on any parsing error
        return []


def x_parse_wp_dependencies__mutmut_2(wp_file: Path) -> list[str]:
    """Parse dependencies from WP frontmatter.

    Uses FrontmatterManager for consistent parsing across CLI.

    Args:
        wp_file: Path to work package markdown file

    Returns:
        List of WP IDs this WP depends on (e.g., ["WP01", "WP02"])
        Returns empty list if no dependencies or parsing fails

    Examples:
        >>> wp_file = Path("tasks/WP02.md")
        >>> deps = parse_wp_dependencies(wp_file)
        >>> print(deps)  # ["WP01"]
    """
    try:
        # Use FrontmatterManager for consistent parsing
        frontmatter, _ = read_frontmatter(None)

        # Extract dependencies field (FrontmatterManager already defaults to [])
        dependencies = frontmatter.get("dependencies", [])

        # Validate dependencies is a list
        if not isinstance(dependencies, list):
            return []

        return dependencies

    except (FrontmatterError, OSError):
        # Return empty list on any parsing error
        return []


def x_parse_wp_dependencies__mutmut_3(wp_file: Path) -> list[str]:
    """Parse dependencies from WP frontmatter.

    Uses FrontmatterManager for consistent parsing across CLI.

    Args:
        wp_file: Path to work package markdown file

    Returns:
        List of WP IDs this WP depends on (e.g., ["WP01", "WP02"])
        Returns empty list if no dependencies or parsing fails

    Examples:
        >>> wp_file = Path("tasks/WP02.md")
        >>> deps = parse_wp_dependencies(wp_file)
        >>> print(deps)  # ["WP01"]
    """
    try:
        # Use FrontmatterManager for consistent parsing
        frontmatter, _ = read_frontmatter(wp_file)

        # Extract dependencies field (FrontmatterManager already defaults to [])
        dependencies = None

        # Validate dependencies is a list
        if not isinstance(dependencies, list):
            return []

        return dependencies

    except (FrontmatterError, OSError):
        # Return empty list on any parsing error
        return []


def x_parse_wp_dependencies__mutmut_4(wp_file: Path) -> list[str]:
    """Parse dependencies from WP frontmatter.

    Uses FrontmatterManager for consistent parsing across CLI.

    Args:
        wp_file: Path to work package markdown file

    Returns:
        List of WP IDs this WP depends on (e.g., ["WP01", "WP02"])
        Returns empty list if no dependencies or parsing fails

    Examples:
        >>> wp_file = Path("tasks/WP02.md")
        >>> deps = parse_wp_dependencies(wp_file)
        >>> print(deps)  # ["WP01"]
    """
    try:
        # Use FrontmatterManager for consistent parsing
        frontmatter, _ = read_frontmatter(wp_file)

        # Extract dependencies field (FrontmatterManager already defaults to [])
        dependencies = frontmatter.get(None, [])

        # Validate dependencies is a list
        if not isinstance(dependencies, list):
            return []

        return dependencies

    except (FrontmatterError, OSError):
        # Return empty list on any parsing error
        return []


def x_parse_wp_dependencies__mutmut_5(wp_file: Path) -> list[str]:
    """Parse dependencies from WP frontmatter.

    Uses FrontmatterManager for consistent parsing across CLI.

    Args:
        wp_file: Path to work package markdown file

    Returns:
        List of WP IDs this WP depends on (e.g., ["WP01", "WP02"])
        Returns empty list if no dependencies or parsing fails

    Examples:
        >>> wp_file = Path("tasks/WP02.md")
        >>> deps = parse_wp_dependencies(wp_file)
        >>> print(deps)  # ["WP01"]
    """
    try:
        # Use FrontmatterManager for consistent parsing
        frontmatter, _ = read_frontmatter(wp_file)

        # Extract dependencies field (FrontmatterManager already defaults to [])
        dependencies = frontmatter.get("dependencies", None)

        # Validate dependencies is a list
        if not isinstance(dependencies, list):
            return []

        return dependencies

    except (FrontmatterError, OSError):
        # Return empty list on any parsing error
        return []


def x_parse_wp_dependencies__mutmut_6(wp_file: Path) -> list[str]:
    """Parse dependencies from WP frontmatter.

    Uses FrontmatterManager for consistent parsing across CLI.

    Args:
        wp_file: Path to work package markdown file

    Returns:
        List of WP IDs this WP depends on (e.g., ["WP01", "WP02"])
        Returns empty list if no dependencies or parsing fails

    Examples:
        >>> wp_file = Path("tasks/WP02.md")
        >>> deps = parse_wp_dependencies(wp_file)
        >>> print(deps)  # ["WP01"]
    """
    try:
        # Use FrontmatterManager for consistent parsing
        frontmatter, _ = read_frontmatter(wp_file)

        # Extract dependencies field (FrontmatterManager already defaults to [])
        dependencies = frontmatter.get([])

        # Validate dependencies is a list
        if not isinstance(dependencies, list):
            return []

        return dependencies

    except (FrontmatterError, OSError):
        # Return empty list on any parsing error
        return []


def x_parse_wp_dependencies__mutmut_7(wp_file: Path) -> list[str]:
    """Parse dependencies from WP frontmatter.

    Uses FrontmatterManager for consistent parsing across CLI.

    Args:
        wp_file: Path to work package markdown file

    Returns:
        List of WP IDs this WP depends on (e.g., ["WP01", "WP02"])
        Returns empty list if no dependencies or parsing fails

    Examples:
        >>> wp_file = Path("tasks/WP02.md")
        >>> deps = parse_wp_dependencies(wp_file)
        >>> print(deps)  # ["WP01"]
    """
    try:
        # Use FrontmatterManager for consistent parsing
        frontmatter, _ = read_frontmatter(wp_file)

        # Extract dependencies field (FrontmatterManager already defaults to [])
        dependencies = frontmatter.get("dependencies", )

        # Validate dependencies is a list
        if not isinstance(dependencies, list):
            return []

        return dependencies

    except (FrontmatterError, OSError):
        # Return empty list on any parsing error
        return []


def x_parse_wp_dependencies__mutmut_8(wp_file: Path) -> list[str]:
    """Parse dependencies from WP frontmatter.

    Uses FrontmatterManager for consistent parsing across CLI.

    Args:
        wp_file: Path to work package markdown file

    Returns:
        List of WP IDs this WP depends on (e.g., ["WP01", "WP02"])
        Returns empty list if no dependencies or parsing fails

    Examples:
        >>> wp_file = Path("tasks/WP02.md")
        >>> deps = parse_wp_dependencies(wp_file)
        >>> print(deps)  # ["WP01"]
    """
    try:
        # Use FrontmatterManager for consistent parsing
        frontmatter, _ = read_frontmatter(wp_file)

        # Extract dependencies field (FrontmatterManager already defaults to [])
        dependencies = frontmatter.get("XXdependenciesXX", [])

        # Validate dependencies is a list
        if not isinstance(dependencies, list):
            return []

        return dependencies

    except (FrontmatterError, OSError):
        # Return empty list on any parsing error
        return []


def x_parse_wp_dependencies__mutmut_9(wp_file: Path) -> list[str]:
    """Parse dependencies from WP frontmatter.

    Uses FrontmatterManager for consistent parsing across CLI.

    Args:
        wp_file: Path to work package markdown file

    Returns:
        List of WP IDs this WP depends on (e.g., ["WP01", "WP02"])
        Returns empty list if no dependencies or parsing fails

    Examples:
        >>> wp_file = Path("tasks/WP02.md")
        >>> deps = parse_wp_dependencies(wp_file)
        >>> print(deps)  # ["WP01"]
    """
    try:
        # Use FrontmatterManager for consistent parsing
        frontmatter, _ = read_frontmatter(wp_file)

        # Extract dependencies field (FrontmatterManager already defaults to [])
        dependencies = frontmatter.get("DEPENDENCIES", [])

        # Validate dependencies is a list
        if not isinstance(dependencies, list):
            return []

        return dependencies

    except (FrontmatterError, OSError):
        # Return empty list on any parsing error
        return []


def x_parse_wp_dependencies__mutmut_10(wp_file: Path) -> list[str]:
    """Parse dependencies from WP frontmatter.

    Uses FrontmatterManager for consistent parsing across CLI.

    Args:
        wp_file: Path to work package markdown file

    Returns:
        List of WP IDs this WP depends on (e.g., ["WP01", "WP02"])
        Returns empty list if no dependencies or parsing fails

    Examples:
        >>> wp_file = Path("tasks/WP02.md")
        >>> deps = parse_wp_dependencies(wp_file)
        >>> print(deps)  # ["WP01"]
    """
    try:
        # Use FrontmatterManager for consistent parsing
        frontmatter, _ = read_frontmatter(wp_file)

        # Extract dependencies field (FrontmatterManager already defaults to [])
        dependencies = frontmatter.get("dependencies", [])

        # Validate dependencies is a list
        if isinstance(dependencies, list):
            return []

        return dependencies

    except (FrontmatterError, OSError):
        # Return empty list on any parsing error
        return []

x_parse_wp_dependencies__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_parse_wp_dependencies__mutmut_1': x_parse_wp_dependencies__mutmut_1, 
    'x_parse_wp_dependencies__mutmut_2': x_parse_wp_dependencies__mutmut_2, 
    'x_parse_wp_dependencies__mutmut_3': x_parse_wp_dependencies__mutmut_3, 
    'x_parse_wp_dependencies__mutmut_4': x_parse_wp_dependencies__mutmut_4, 
    'x_parse_wp_dependencies__mutmut_5': x_parse_wp_dependencies__mutmut_5, 
    'x_parse_wp_dependencies__mutmut_6': x_parse_wp_dependencies__mutmut_6, 
    'x_parse_wp_dependencies__mutmut_7': x_parse_wp_dependencies__mutmut_7, 
    'x_parse_wp_dependencies__mutmut_8': x_parse_wp_dependencies__mutmut_8, 
    'x_parse_wp_dependencies__mutmut_9': x_parse_wp_dependencies__mutmut_9, 
    'x_parse_wp_dependencies__mutmut_10': x_parse_wp_dependencies__mutmut_10
}
x_parse_wp_dependencies__mutmut_orig.__name__ = 'x_parse_wp_dependencies'


def build_dependency_graph(feature_dir: Path) -> dict[str, list[str]]:
    args = [feature_dir]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_build_dependency_graph__mutmut_orig, x_build_dependency_graph__mutmut_mutants, args, kwargs, None)


def x_build_dependency_graph__mutmut_orig(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_1(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = None

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_2(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name != "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_3(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "XXtasksXX":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_4(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "TASKS":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_5(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = None
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_6(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = None

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_7(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir * "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_8(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "XXtasksXX"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_9(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "TASKS"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_10(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_11(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(None):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_12(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob(None)):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_13(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("XXWP*.mdXX")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_14(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("wp*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_15(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.MD")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_16(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = None
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_17(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(None)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_18(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_19(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            break

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_20(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = None
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_21(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(None)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_22(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = None

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_23(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get(None)

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_24(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("XXwork_package_idXX")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_25(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("WORK_PACKAGE_ID")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_26(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id or frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_27(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id == filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_28(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    None
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_29(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = None

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_30(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id and filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_31(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            break

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_32(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = None
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_33(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(None)
        graph[wp_id] = dependencies

    return graph


def x_build_dependency_graph__mutmut_34(feature_dir: Path) -> dict[str, list[str]]:
    """Build dependency graph from all WPs in feature.

    Scans tasks/ directory for WP files and parses their dependencies.
    Validates that filename WP ID matches frontmatter work_package_id.

    Args:
        feature_dir: Path to feature directory (contains tasks/ subdirectory)
                    OR path to tasks directory directly

    Returns:
        Adjacency list mapping WP ID to list of dependencies
        Example: {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}

    Examples:
        >>> feature_dir = Path("kitty-specs/010-feature")
        >>> graph = build_dependency_graph(feature_dir)
        >>> print(graph)  # {"WP01": [], "WP02": ["WP01"]}
    """
    graph = {}

    # Support both feature_dir and tasks_dir as input
    if feature_dir.name == "tasks":
        # Already pointing to tasks directory
        tasks_dir = feature_dir
    else:
        # Pointing to feature directory, append tasks/
        tasks_dir = feature_dir / "tasks"

    if not tasks_dir.exists():
        return graph

    # Find all WP markdown files
    for wp_file in sorted(tasks_dir.glob("WP*.md")):
        # Extract WP ID from filename (e.g., WP01-title.md → WP01)
        filename_wp_id = extract_wp_id_from_filename(wp_file.name)
        if not filename_wp_id:
            continue

        # Parse frontmatter to get canonical work_package_id
        try:
            frontmatter, _ = read_frontmatter(wp_file)
            frontmatter_wp_id = frontmatter.get("work_package_id")

            # Verify filename matches frontmatter (catch misnamed files)
            if frontmatter_wp_id and frontmatter_wp_id != filename_wp_id:
                raise ValueError(
                    f"WP ID mismatch: filename {filename_wp_id} vs frontmatter {frontmatter_wp_id} "
                    f"in {wp_file}"
                )

            wp_id = frontmatter_wp_id or filename_wp_id

        except (FrontmatterError, OSError):
            # If frontmatter read fails, skip this file
            continue

        # Parse dependencies from frontmatter
        dependencies = parse_wp_dependencies(wp_file)
        graph[wp_id] = None

    return graph

x_build_dependency_graph__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_build_dependency_graph__mutmut_1': x_build_dependency_graph__mutmut_1, 
    'x_build_dependency_graph__mutmut_2': x_build_dependency_graph__mutmut_2, 
    'x_build_dependency_graph__mutmut_3': x_build_dependency_graph__mutmut_3, 
    'x_build_dependency_graph__mutmut_4': x_build_dependency_graph__mutmut_4, 
    'x_build_dependency_graph__mutmut_5': x_build_dependency_graph__mutmut_5, 
    'x_build_dependency_graph__mutmut_6': x_build_dependency_graph__mutmut_6, 
    'x_build_dependency_graph__mutmut_7': x_build_dependency_graph__mutmut_7, 
    'x_build_dependency_graph__mutmut_8': x_build_dependency_graph__mutmut_8, 
    'x_build_dependency_graph__mutmut_9': x_build_dependency_graph__mutmut_9, 
    'x_build_dependency_graph__mutmut_10': x_build_dependency_graph__mutmut_10, 
    'x_build_dependency_graph__mutmut_11': x_build_dependency_graph__mutmut_11, 
    'x_build_dependency_graph__mutmut_12': x_build_dependency_graph__mutmut_12, 
    'x_build_dependency_graph__mutmut_13': x_build_dependency_graph__mutmut_13, 
    'x_build_dependency_graph__mutmut_14': x_build_dependency_graph__mutmut_14, 
    'x_build_dependency_graph__mutmut_15': x_build_dependency_graph__mutmut_15, 
    'x_build_dependency_graph__mutmut_16': x_build_dependency_graph__mutmut_16, 
    'x_build_dependency_graph__mutmut_17': x_build_dependency_graph__mutmut_17, 
    'x_build_dependency_graph__mutmut_18': x_build_dependency_graph__mutmut_18, 
    'x_build_dependency_graph__mutmut_19': x_build_dependency_graph__mutmut_19, 
    'x_build_dependency_graph__mutmut_20': x_build_dependency_graph__mutmut_20, 
    'x_build_dependency_graph__mutmut_21': x_build_dependency_graph__mutmut_21, 
    'x_build_dependency_graph__mutmut_22': x_build_dependency_graph__mutmut_22, 
    'x_build_dependency_graph__mutmut_23': x_build_dependency_graph__mutmut_23, 
    'x_build_dependency_graph__mutmut_24': x_build_dependency_graph__mutmut_24, 
    'x_build_dependency_graph__mutmut_25': x_build_dependency_graph__mutmut_25, 
    'x_build_dependency_graph__mutmut_26': x_build_dependency_graph__mutmut_26, 
    'x_build_dependency_graph__mutmut_27': x_build_dependency_graph__mutmut_27, 
    'x_build_dependency_graph__mutmut_28': x_build_dependency_graph__mutmut_28, 
    'x_build_dependency_graph__mutmut_29': x_build_dependency_graph__mutmut_29, 
    'x_build_dependency_graph__mutmut_30': x_build_dependency_graph__mutmut_30, 
    'x_build_dependency_graph__mutmut_31': x_build_dependency_graph__mutmut_31, 
    'x_build_dependency_graph__mutmut_32': x_build_dependency_graph__mutmut_32, 
    'x_build_dependency_graph__mutmut_33': x_build_dependency_graph__mutmut_33, 
    'x_build_dependency_graph__mutmut_34': x_build_dependency_graph__mutmut_34
}
x_build_dependency_graph__mutmut_orig.__name__ = 'x_build_dependency_graph'


def extract_wp_id_from_filename(filename: str) -> Optional[str]:
    args = [filename]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_extract_wp_id_from_filename__mutmut_orig, x_extract_wp_id_from_filename__mutmut_mutants, args, kwargs, None)


def x_extract_wp_id_from_filename__mutmut_orig(filename: str) -> Optional[str]:
    """Extract WP ID from filename.

    Args:
        filename: WP file name (e.g., "WP01-title.md" or "WP02.md")

    Returns:
        WP ID (e.g., "WP01") or None if invalid format

    Examples:
        >>> extract_wp_id_from_filename("WP01-setup.md")
        'WP01'
        >>> extract_wp_id_from_filename("invalid.md")
        None
    """
    match = re.match(r"^(WP\d{2})", filename)
    return match.group(1) if match else None


def x_extract_wp_id_from_filename__mutmut_1(filename: str) -> Optional[str]:
    """Extract WP ID from filename.

    Args:
        filename: WP file name (e.g., "WP01-title.md" or "WP02.md")

    Returns:
        WP ID (e.g., "WP01") or None if invalid format

    Examples:
        >>> extract_wp_id_from_filename("WP01-setup.md")
        'WP01'
        >>> extract_wp_id_from_filename("invalid.md")
        None
    """
    match = None
    return match.group(1) if match else None


def x_extract_wp_id_from_filename__mutmut_2(filename: str) -> Optional[str]:
    """Extract WP ID from filename.

    Args:
        filename: WP file name (e.g., "WP01-title.md" or "WP02.md")

    Returns:
        WP ID (e.g., "WP01") or None if invalid format

    Examples:
        >>> extract_wp_id_from_filename("WP01-setup.md")
        'WP01'
        >>> extract_wp_id_from_filename("invalid.md")
        None
    """
    match = re.match(None, filename)
    return match.group(1) if match else None


def x_extract_wp_id_from_filename__mutmut_3(filename: str) -> Optional[str]:
    """Extract WP ID from filename.

    Args:
        filename: WP file name (e.g., "WP01-title.md" or "WP02.md")

    Returns:
        WP ID (e.g., "WP01") or None if invalid format

    Examples:
        >>> extract_wp_id_from_filename("WP01-setup.md")
        'WP01'
        >>> extract_wp_id_from_filename("invalid.md")
        None
    """
    match = re.match(r"^(WP\d{2})", None)
    return match.group(1) if match else None


def x_extract_wp_id_from_filename__mutmut_4(filename: str) -> Optional[str]:
    """Extract WP ID from filename.

    Args:
        filename: WP file name (e.g., "WP01-title.md" or "WP02.md")

    Returns:
        WP ID (e.g., "WP01") or None if invalid format

    Examples:
        >>> extract_wp_id_from_filename("WP01-setup.md")
        'WP01'
        >>> extract_wp_id_from_filename("invalid.md")
        None
    """
    match = re.match(filename)
    return match.group(1) if match else None


def x_extract_wp_id_from_filename__mutmut_5(filename: str) -> Optional[str]:
    """Extract WP ID from filename.

    Args:
        filename: WP file name (e.g., "WP01-title.md" or "WP02.md")

    Returns:
        WP ID (e.g., "WP01") or None if invalid format

    Examples:
        >>> extract_wp_id_from_filename("WP01-setup.md")
        'WP01'
        >>> extract_wp_id_from_filename("invalid.md")
        None
    """
    match = re.match(r"^(WP\d{2})", )
    return match.group(1) if match else None


def x_extract_wp_id_from_filename__mutmut_6(filename: str) -> Optional[str]:
    """Extract WP ID from filename.

    Args:
        filename: WP file name (e.g., "WP01-title.md" or "WP02.md")

    Returns:
        WP ID (e.g., "WP01") or None if invalid format

    Examples:
        >>> extract_wp_id_from_filename("WP01-setup.md")
        'WP01'
        >>> extract_wp_id_from_filename("invalid.md")
        None
    """
    match = re.match(r"XX^(WP\d{2})XX", filename)
    return match.group(1) if match else None


def x_extract_wp_id_from_filename__mutmut_7(filename: str) -> Optional[str]:
    """Extract WP ID from filename.

    Args:
        filename: WP file name (e.g., "WP01-title.md" or "WP02.md")

    Returns:
        WP ID (e.g., "WP01") or None if invalid format

    Examples:
        >>> extract_wp_id_from_filename("WP01-setup.md")
        'WP01'
        >>> extract_wp_id_from_filename("invalid.md")
        None
    """
    match = re.match(r"^(wp\d{2})", filename)
    return match.group(1) if match else None


def x_extract_wp_id_from_filename__mutmut_8(filename: str) -> Optional[str]:
    """Extract WP ID from filename.

    Args:
        filename: WP file name (e.g., "WP01-title.md" or "WP02.md")

    Returns:
        WP ID (e.g., "WP01") or None if invalid format

    Examples:
        >>> extract_wp_id_from_filename("WP01-setup.md")
        'WP01'
        >>> extract_wp_id_from_filename("invalid.md")
        None
    """
    match = re.match(r"^(WP\d{2})", filename)
    return match.group(None) if match else None


def x_extract_wp_id_from_filename__mutmut_9(filename: str) -> Optional[str]:
    """Extract WP ID from filename.

    Args:
        filename: WP file name (e.g., "WP01-title.md" or "WP02.md")

    Returns:
        WP ID (e.g., "WP01") or None if invalid format

    Examples:
        >>> extract_wp_id_from_filename("WP01-setup.md")
        'WP01'
        >>> extract_wp_id_from_filename("invalid.md")
        None
    """
    match = re.match(r"^(WP\d{2})", filename)
    return match.group(2) if match else None

x_extract_wp_id_from_filename__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_extract_wp_id_from_filename__mutmut_1': x_extract_wp_id_from_filename__mutmut_1, 
    'x_extract_wp_id_from_filename__mutmut_2': x_extract_wp_id_from_filename__mutmut_2, 
    'x_extract_wp_id_from_filename__mutmut_3': x_extract_wp_id_from_filename__mutmut_3, 
    'x_extract_wp_id_from_filename__mutmut_4': x_extract_wp_id_from_filename__mutmut_4, 
    'x_extract_wp_id_from_filename__mutmut_5': x_extract_wp_id_from_filename__mutmut_5, 
    'x_extract_wp_id_from_filename__mutmut_6': x_extract_wp_id_from_filename__mutmut_6, 
    'x_extract_wp_id_from_filename__mutmut_7': x_extract_wp_id_from_filename__mutmut_7, 
    'x_extract_wp_id_from_filename__mutmut_8': x_extract_wp_id_from_filename__mutmut_8, 
    'x_extract_wp_id_from_filename__mutmut_9': x_extract_wp_id_from_filename__mutmut_9
}
x_extract_wp_id_from_filename__mutmut_orig.__name__ = 'x_extract_wp_id_from_filename'


def detect_cycles(graph: dict[str, list[str]]) -> list[list[str]] | None:
    args = [graph]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_detect_cycles__mutmut_orig, x_detect_cycles__mutmut_mutants, args, kwargs, None)


def x_detect_cycles__mutmut_orig(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_1(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = None
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_2(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 1, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_3(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 2, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_4(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 3
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_5(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = None
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_6(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = None

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_7(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = None
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_8(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(None)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_9(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(None, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_10(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, None):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_11(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get([]):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_12(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, ):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_13(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = None

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_14(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(None, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_15(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, None)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_16(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_17(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, )

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_18(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color != GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_19(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor not in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_20(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = None
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_21(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(None)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_22(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.rindex(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_23(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(None)
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_24(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] - [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_25(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color != WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_26(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(None, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_27(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, None)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_28(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_29(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, )

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_30(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = None

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_31(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] != WHITE:
            dfs(wp, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_32(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(None, [])

    return cycles if cycles else None


def x_detect_cycles__mutmut_33(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, None)

    return cycles if cycles else None


def x_detect_cycles__mutmut_34(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs([])

    return cycles if cycles else None


def x_detect_cycles__mutmut_35(graph: dict[str, list[str]]) -> list[list[str]] | None:
    """Detect circular dependencies using DFS with coloring.

    Uses depth-first search with three-color marking (white/gray/black)
    to detect back edges, which indicate cycles.

    Args:
        graph: Adjacency list mapping WP ID to dependencies

    Returns:
        List of cycles (each cycle is a list of WP IDs) or None if acyclic

    Complexity:
        O(V + E) where V = vertices (WPs), E = edges (dependencies)

    Examples:
        >>> graph = {"WP01": ["WP02"], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # [["WP01", "WP02", "WP01"]]

        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> cycles = detect_cycles(graph)
        >>> print(cycles)  # None (acyclic)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {wp: WHITE for wp in graph}
    cycles = []

    def dfs(node: str, path: list[str]) -> None:
        """DFS traversal with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, []):
            neighbor_color = color.get(neighbor, WHITE)

            if neighbor_color == GRAY:
                # Back edge found - cycle detected
                if neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            elif neighbor_color == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    # Run DFS from each unvisited node
    for wp in graph:
        if color[wp] == WHITE:
            dfs(wp, )

    return cycles if cycles else None

x_detect_cycles__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_detect_cycles__mutmut_1': x_detect_cycles__mutmut_1, 
    'x_detect_cycles__mutmut_2': x_detect_cycles__mutmut_2, 
    'x_detect_cycles__mutmut_3': x_detect_cycles__mutmut_3, 
    'x_detect_cycles__mutmut_4': x_detect_cycles__mutmut_4, 
    'x_detect_cycles__mutmut_5': x_detect_cycles__mutmut_5, 
    'x_detect_cycles__mutmut_6': x_detect_cycles__mutmut_6, 
    'x_detect_cycles__mutmut_7': x_detect_cycles__mutmut_7, 
    'x_detect_cycles__mutmut_8': x_detect_cycles__mutmut_8, 
    'x_detect_cycles__mutmut_9': x_detect_cycles__mutmut_9, 
    'x_detect_cycles__mutmut_10': x_detect_cycles__mutmut_10, 
    'x_detect_cycles__mutmut_11': x_detect_cycles__mutmut_11, 
    'x_detect_cycles__mutmut_12': x_detect_cycles__mutmut_12, 
    'x_detect_cycles__mutmut_13': x_detect_cycles__mutmut_13, 
    'x_detect_cycles__mutmut_14': x_detect_cycles__mutmut_14, 
    'x_detect_cycles__mutmut_15': x_detect_cycles__mutmut_15, 
    'x_detect_cycles__mutmut_16': x_detect_cycles__mutmut_16, 
    'x_detect_cycles__mutmut_17': x_detect_cycles__mutmut_17, 
    'x_detect_cycles__mutmut_18': x_detect_cycles__mutmut_18, 
    'x_detect_cycles__mutmut_19': x_detect_cycles__mutmut_19, 
    'x_detect_cycles__mutmut_20': x_detect_cycles__mutmut_20, 
    'x_detect_cycles__mutmut_21': x_detect_cycles__mutmut_21, 
    'x_detect_cycles__mutmut_22': x_detect_cycles__mutmut_22, 
    'x_detect_cycles__mutmut_23': x_detect_cycles__mutmut_23, 
    'x_detect_cycles__mutmut_24': x_detect_cycles__mutmut_24, 
    'x_detect_cycles__mutmut_25': x_detect_cycles__mutmut_25, 
    'x_detect_cycles__mutmut_26': x_detect_cycles__mutmut_26, 
    'x_detect_cycles__mutmut_27': x_detect_cycles__mutmut_27, 
    'x_detect_cycles__mutmut_28': x_detect_cycles__mutmut_28, 
    'x_detect_cycles__mutmut_29': x_detect_cycles__mutmut_29, 
    'x_detect_cycles__mutmut_30': x_detect_cycles__mutmut_30, 
    'x_detect_cycles__mutmut_31': x_detect_cycles__mutmut_31, 
    'x_detect_cycles__mutmut_32': x_detect_cycles__mutmut_32, 
    'x_detect_cycles__mutmut_33': x_detect_cycles__mutmut_33, 
    'x_detect_cycles__mutmut_34': x_detect_cycles__mutmut_34, 
    'x_detect_cycles__mutmut_35': x_detect_cycles__mutmut_35
}
x_detect_cycles__mutmut_orig.__name__ = 'x_detect_cycles'


def validate_dependencies(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    args = [wp_id, declared_deps, graph]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_validate_dependencies__mutmut_orig, x_validate_dependencies__mutmut_mutants, args, kwargs, None)


def x_validate_dependencies__mutmut_orig(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_1(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = None
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_2(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = None

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_3(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(None)

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_4(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"XX^WP\d{2}$XX")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_5(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^wp\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_6(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_7(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(None):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_8(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(None)
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_9(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            break

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_10(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep != wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_11(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(None)
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_12(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            break

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_13(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_14(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(None)

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_15(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = None
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_16(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = None

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_17(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = None
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_18(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(None)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_19(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id not in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_20(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(None)
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_21(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(None)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_22(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {'XX → XX'.join(cycle)}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_23(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                return

    is_valid = len(errors) == 0
    return is_valid, errors


def x_validate_dependencies__mutmut_24(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = None
    return is_valid, errors


def x_validate_dependencies__mutmut_25(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) != 0
    return is_valid, errors


def x_validate_dependencies__mutmut_26(
    wp_id: str,
    declared_deps: list[str],
    graph: dict[str, list[str]]
) -> tuple[bool, list[str]]:
    """Validate that WP's dependencies are valid.

    Checks:
    - Dependencies exist in graph
    - No self-dependencies
    - No circular dependencies
    - Valid WP ID format

    Args:
        wp_id: Work package ID being validated
        declared_deps: List of dependency WP IDs
        graph: Complete dependency graph

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all validations pass
        - error_messages: List of error descriptions (empty if valid)

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"]}
        >>> is_valid, errors = validate_dependencies("WP02", ["WP01"], graph)
        >>> print(is_valid)  # True

        >>> is_valid, errors = validate_dependencies("WP02", ["WP99"], graph)
        >>> print(is_valid)  # False
        >>> print(errors)  # ["Dependency WP99 not found in graph"]
    """
    errors = []
    wp_pattern = re.compile(r"^WP\d{2}$")

    # Validate each dependency
    for dep in declared_deps:
        # Check format
        if not wp_pattern.match(dep):
            errors.append(f"Invalid WP ID format: {dep} (must be WP## like WP01)")
            continue

        # Check self-dependency
        if dep == wp_id:
            errors.append(f"Cannot depend on self: {wp_id} → {wp_id}")
            continue

        # Check dependency exists in graph
        if dep not in graph:
            errors.append(f"Dependency {dep} not found in graph")

    # Check for circular dependencies
    # Build temporary graph with this WP's dependencies to check for cycles
    test_graph = graph.copy()
    test_graph[wp_id] = declared_deps

    cycles = detect_cycles(test_graph)
    if cycles:
        for cycle in cycles:
            if wp_id in cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")
                break

    is_valid = len(errors) == 1
    return is_valid, errors

x_validate_dependencies__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_validate_dependencies__mutmut_1': x_validate_dependencies__mutmut_1, 
    'x_validate_dependencies__mutmut_2': x_validate_dependencies__mutmut_2, 
    'x_validate_dependencies__mutmut_3': x_validate_dependencies__mutmut_3, 
    'x_validate_dependencies__mutmut_4': x_validate_dependencies__mutmut_4, 
    'x_validate_dependencies__mutmut_5': x_validate_dependencies__mutmut_5, 
    'x_validate_dependencies__mutmut_6': x_validate_dependencies__mutmut_6, 
    'x_validate_dependencies__mutmut_7': x_validate_dependencies__mutmut_7, 
    'x_validate_dependencies__mutmut_8': x_validate_dependencies__mutmut_8, 
    'x_validate_dependencies__mutmut_9': x_validate_dependencies__mutmut_9, 
    'x_validate_dependencies__mutmut_10': x_validate_dependencies__mutmut_10, 
    'x_validate_dependencies__mutmut_11': x_validate_dependencies__mutmut_11, 
    'x_validate_dependencies__mutmut_12': x_validate_dependencies__mutmut_12, 
    'x_validate_dependencies__mutmut_13': x_validate_dependencies__mutmut_13, 
    'x_validate_dependencies__mutmut_14': x_validate_dependencies__mutmut_14, 
    'x_validate_dependencies__mutmut_15': x_validate_dependencies__mutmut_15, 
    'x_validate_dependencies__mutmut_16': x_validate_dependencies__mutmut_16, 
    'x_validate_dependencies__mutmut_17': x_validate_dependencies__mutmut_17, 
    'x_validate_dependencies__mutmut_18': x_validate_dependencies__mutmut_18, 
    'x_validate_dependencies__mutmut_19': x_validate_dependencies__mutmut_19, 
    'x_validate_dependencies__mutmut_20': x_validate_dependencies__mutmut_20, 
    'x_validate_dependencies__mutmut_21': x_validate_dependencies__mutmut_21, 
    'x_validate_dependencies__mutmut_22': x_validate_dependencies__mutmut_22, 
    'x_validate_dependencies__mutmut_23': x_validate_dependencies__mutmut_23, 
    'x_validate_dependencies__mutmut_24': x_validate_dependencies__mutmut_24, 
    'x_validate_dependencies__mutmut_25': x_validate_dependencies__mutmut_25, 
    'x_validate_dependencies__mutmut_26': x_validate_dependencies__mutmut_26
}
x_validate_dependencies__mutmut_orig.__name__ = 'x_validate_dependencies'


def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    args = [graph]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_topological_sort__mutmut_orig, x_topological_sort__mutmut_mutants, args, kwargs, None)


def x_topological_sort__mutmut_orig(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_1(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = None
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_2(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 1 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_3(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = None

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_4(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = None
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_5(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep not in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_6(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(None)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_7(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = None
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_8(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree != 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_9(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 1]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_10(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = None
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_11(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = None
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_12(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(None)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_13(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(1)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_14(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(None)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_15(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(None):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_16(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(None, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_17(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, None)):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_18(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get([])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_19(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, )):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_20(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] = 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_21(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] += 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_22(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 2
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_23(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] != 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_24(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 1:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_25(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(None)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_26(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) == len(graph):
        raise ValueError("Graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_27(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError(None)

    return result


def x_topological_sort__mutmut_28(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("XXGraph contains a cycle - cannot topologically sortXX")

    return result


def x_topological_sort__mutmut_29(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("graph contains a cycle - cannot topologically sort")

    return result


def x_topological_sort__mutmut_30(graph: dict[str, list[str]]) -> list[str]:
    """Return nodes in topological order (dependencies before dependents).

    Uses Kahn's algorithm:
    1. Find all nodes with no incoming edges (no dependencies)
    2. Remove them from graph, add to result
    3. Repeat until graph is empty

    Args:
        graph: Adjacency list where graph[node] = [dependencies]
               Note: This is REVERSE of typical adjacency (edges point to deps)

    Returns:
        List of node IDs in topological order

    Raises:
        ValueError: If graph contains a cycle (use detect_cycles() first)

    Example:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01", "WP02"]}
        >>> topological_sort(graph)
        ['WP01', 'WP02', 'WP03']
    """
    # Build in-degree map and reverse adjacency
    in_degree: dict[str, int] = {node: 0 for node in graph}
    reverse_adj: dict[str, list[str]] = {node: [] for node in graph}

    for node, deps in graph.items():
        in_degree[node] = len(deps)
        for dep in deps:
            if dep in reverse_adj:
                reverse_adj[dep].append(node)

    # Start with nodes that have no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()  # Stable ordering for determinism

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        # "Remove" this node by decrementing in-degree of dependents
        for dependent in sorted(reverse_adj.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()  # Maintain sorted order

    if len(result) != len(graph):
        raise ValueError("GRAPH CONTAINS A CYCLE - CANNOT TOPOLOGICALLY SORT")

    return result

x_topological_sort__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_topological_sort__mutmut_1': x_topological_sort__mutmut_1, 
    'x_topological_sort__mutmut_2': x_topological_sort__mutmut_2, 
    'x_topological_sort__mutmut_3': x_topological_sort__mutmut_3, 
    'x_topological_sort__mutmut_4': x_topological_sort__mutmut_4, 
    'x_topological_sort__mutmut_5': x_topological_sort__mutmut_5, 
    'x_topological_sort__mutmut_6': x_topological_sort__mutmut_6, 
    'x_topological_sort__mutmut_7': x_topological_sort__mutmut_7, 
    'x_topological_sort__mutmut_8': x_topological_sort__mutmut_8, 
    'x_topological_sort__mutmut_9': x_topological_sort__mutmut_9, 
    'x_topological_sort__mutmut_10': x_topological_sort__mutmut_10, 
    'x_topological_sort__mutmut_11': x_topological_sort__mutmut_11, 
    'x_topological_sort__mutmut_12': x_topological_sort__mutmut_12, 
    'x_topological_sort__mutmut_13': x_topological_sort__mutmut_13, 
    'x_topological_sort__mutmut_14': x_topological_sort__mutmut_14, 
    'x_topological_sort__mutmut_15': x_topological_sort__mutmut_15, 
    'x_topological_sort__mutmut_16': x_topological_sort__mutmut_16, 
    'x_topological_sort__mutmut_17': x_topological_sort__mutmut_17, 
    'x_topological_sort__mutmut_18': x_topological_sort__mutmut_18, 
    'x_topological_sort__mutmut_19': x_topological_sort__mutmut_19, 
    'x_topological_sort__mutmut_20': x_topological_sort__mutmut_20, 
    'x_topological_sort__mutmut_21': x_topological_sort__mutmut_21, 
    'x_topological_sort__mutmut_22': x_topological_sort__mutmut_22, 
    'x_topological_sort__mutmut_23': x_topological_sort__mutmut_23, 
    'x_topological_sort__mutmut_24': x_topological_sort__mutmut_24, 
    'x_topological_sort__mutmut_25': x_topological_sort__mutmut_25, 
    'x_topological_sort__mutmut_26': x_topological_sort__mutmut_26, 
    'x_topological_sort__mutmut_27': x_topological_sort__mutmut_27, 
    'x_topological_sort__mutmut_28': x_topological_sort__mutmut_28, 
    'x_topological_sort__mutmut_29': x_topological_sort__mutmut_29, 
    'x_topological_sort__mutmut_30': x_topological_sort__mutmut_30
}
x_topological_sort__mutmut_orig.__name__ = 'x_topological_sort'


def get_dependents(wp_id: str, graph: dict[str, list[str]]) -> list[str]:
    args = [wp_id, graph]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_dependents__mutmut_orig, x_get_dependents__mutmut_mutants, args, kwargs, None)


def x_get_dependents__mutmut_orig(wp_id: str, graph: dict[str, list[str]]) -> list[str]:
    """Get list of WPs that depend on this WP (inverse graph query).

    Builds inverse graph and returns direct dependents only (not transitive).

    Args:
        wp_id: Work package ID to query
        graph: Dependency graph (adjacency list)

    Returns:
        List of WP IDs that directly depend on wp_id
        Returns empty list if no dependents or WP not in graph

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}
        >>> deps = get_dependents("WP01", graph)
        >>> print(sorted(deps))  # ["WP02", "WP03"]

        >>> deps = get_dependents("WP02", graph)
        >>> print(deps)  # []
    """
    # Build inverse graph: wp -> list of wps that depend on it
    inverse_graph: dict[str, list[str]] = {wp: [] for wp in graph}

    for wp, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in inverse_graph:
                inverse_graph[dependency] = []
            inverse_graph[dependency].append(wp)

    return inverse_graph.get(wp_id, [])


def x_get_dependents__mutmut_1(wp_id: str, graph: dict[str, list[str]]) -> list[str]:
    """Get list of WPs that depend on this WP (inverse graph query).

    Builds inverse graph and returns direct dependents only (not transitive).

    Args:
        wp_id: Work package ID to query
        graph: Dependency graph (adjacency list)

    Returns:
        List of WP IDs that directly depend on wp_id
        Returns empty list if no dependents or WP not in graph

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}
        >>> deps = get_dependents("WP01", graph)
        >>> print(sorted(deps))  # ["WP02", "WP03"]

        >>> deps = get_dependents("WP02", graph)
        >>> print(deps)  # []
    """
    # Build inverse graph: wp -> list of wps that depend on it
    inverse_graph: dict[str, list[str]] = None

    for wp, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in inverse_graph:
                inverse_graph[dependency] = []
            inverse_graph[dependency].append(wp)

    return inverse_graph.get(wp_id, [])


def x_get_dependents__mutmut_2(wp_id: str, graph: dict[str, list[str]]) -> list[str]:
    """Get list of WPs that depend on this WP (inverse graph query).

    Builds inverse graph and returns direct dependents only (not transitive).

    Args:
        wp_id: Work package ID to query
        graph: Dependency graph (adjacency list)

    Returns:
        List of WP IDs that directly depend on wp_id
        Returns empty list if no dependents or WP not in graph

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}
        >>> deps = get_dependents("WP01", graph)
        >>> print(sorted(deps))  # ["WP02", "WP03"]

        >>> deps = get_dependents("WP02", graph)
        >>> print(deps)  # []
    """
    # Build inverse graph: wp -> list of wps that depend on it
    inverse_graph: dict[str, list[str]] = {wp: [] for wp in graph}

    for wp, dependencies in graph.items():
        for dependency in dependencies:
            if dependency in inverse_graph:
                inverse_graph[dependency] = []
            inverse_graph[dependency].append(wp)

    return inverse_graph.get(wp_id, [])


def x_get_dependents__mutmut_3(wp_id: str, graph: dict[str, list[str]]) -> list[str]:
    """Get list of WPs that depend on this WP (inverse graph query).

    Builds inverse graph and returns direct dependents only (not transitive).

    Args:
        wp_id: Work package ID to query
        graph: Dependency graph (adjacency list)

    Returns:
        List of WP IDs that directly depend on wp_id
        Returns empty list if no dependents or WP not in graph

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}
        >>> deps = get_dependents("WP01", graph)
        >>> print(sorted(deps))  # ["WP02", "WP03"]

        >>> deps = get_dependents("WP02", graph)
        >>> print(deps)  # []
    """
    # Build inverse graph: wp -> list of wps that depend on it
    inverse_graph: dict[str, list[str]] = {wp: [] for wp in graph}

    for wp, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in inverse_graph:
                inverse_graph[dependency] = None
            inverse_graph[dependency].append(wp)

    return inverse_graph.get(wp_id, [])


def x_get_dependents__mutmut_4(wp_id: str, graph: dict[str, list[str]]) -> list[str]:
    """Get list of WPs that depend on this WP (inverse graph query).

    Builds inverse graph and returns direct dependents only (not transitive).

    Args:
        wp_id: Work package ID to query
        graph: Dependency graph (adjacency list)

    Returns:
        List of WP IDs that directly depend on wp_id
        Returns empty list if no dependents or WP not in graph

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}
        >>> deps = get_dependents("WP01", graph)
        >>> print(sorted(deps))  # ["WP02", "WP03"]

        >>> deps = get_dependents("WP02", graph)
        >>> print(deps)  # []
    """
    # Build inverse graph: wp -> list of wps that depend on it
    inverse_graph: dict[str, list[str]] = {wp: [] for wp in graph}

    for wp, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in inverse_graph:
                inverse_graph[dependency] = []
            inverse_graph[dependency].append(None)

    return inverse_graph.get(wp_id, [])


def x_get_dependents__mutmut_5(wp_id: str, graph: dict[str, list[str]]) -> list[str]:
    """Get list of WPs that depend on this WP (inverse graph query).

    Builds inverse graph and returns direct dependents only (not transitive).

    Args:
        wp_id: Work package ID to query
        graph: Dependency graph (adjacency list)

    Returns:
        List of WP IDs that directly depend on wp_id
        Returns empty list if no dependents or WP not in graph

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}
        >>> deps = get_dependents("WP01", graph)
        >>> print(sorted(deps))  # ["WP02", "WP03"]

        >>> deps = get_dependents("WP02", graph)
        >>> print(deps)  # []
    """
    # Build inverse graph: wp -> list of wps that depend on it
    inverse_graph: dict[str, list[str]] = {wp: [] for wp in graph}

    for wp, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in inverse_graph:
                inverse_graph[dependency] = []
            inverse_graph[dependency].append(wp)

    return inverse_graph.get(None, [])


def x_get_dependents__mutmut_6(wp_id: str, graph: dict[str, list[str]]) -> list[str]:
    """Get list of WPs that depend on this WP (inverse graph query).

    Builds inverse graph and returns direct dependents only (not transitive).

    Args:
        wp_id: Work package ID to query
        graph: Dependency graph (adjacency list)

    Returns:
        List of WP IDs that directly depend on wp_id
        Returns empty list if no dependents or WP not in graph

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}
        >>> deps = get_dependents("WP01", graph)
        >>> print(sorted(deps))  # ["WP02", "WP03"]

        >>> deps = get_dependents("WP02", graph)
        >>> print(deps)  # []
    """
    # Build inverse graph: wp -> list of wps that depend on it
    inverse_graph: dict[str, list[str]] = {wp: [] for wp in graph}

    for wp, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in inverse_graph:
                inverse_graph[dependency] = []
            inverse_graph[dependency].append(wp)

    return inverse_graph.get(wp_id, None)


def x_get_dependents__mutmut_7(wp_id: str, graph: dict[str, list[str]]) -> list[str]:
    """Get list of WPs that depend on this WP (inverse graph query).

    Builds inverse graph and returns direct dependents only (not transitive).

    Args:
        wp_id: Work package ID to query
        graph: Dependency graph (adjacency list)

    Returns:
        List of WP IDs that directly depend on wp_id
        Returns empty list if no dependents or WP not in graph

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}
        >>> deps = get_dependents("WP01", graph)
        >>> print(sorted(deps))  # ["WP02", "WP03"]

        >>> deps = get_dependents("WP02", graph)
        >>> print(deps)  # []
    """
    # Build inverse graph: wp -> list of wps that depend on it
    inverse_graph: dict[str, list[str]] = {wp: [] for wp in graph}

    for wp, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in inverse_graph:
                inverse_graph[dependency] = []
            inverse_graph[dependency].append(wp)

    return inverse_graph.get([])


def x_get_dependents__mutmut_8(wp_id: str, graph: dict[str, list[str]]) -> list[str]:
    """Get list of WPs that depend on this WP (inverse graph query).

    Builds inverse graph and returns direct dependents only (not transitive).

    Args:
        wp_id: Work package ID to query
        graph: Dependency graph (adjacency list)

    Returns:
        List of WP IDs that directly depend on wp_id
        Returns empty list if no dependents or WP not in graph

    Examples:
        >>> graph = {"WP01": [], "WP02": ["WP01"], "WP03": ["WP01"]}
        >>> deps = get_dependents("WP01", graph)
        >>> print(sorted(deps))  # ["WP02", "WP03"]

        >>> deps = get_dependents("WP02", graph)
        >>> print(deps)  # []
    """
    # Build inverse graph: wp -> list of wps that depend on it
    inverse_graph: dict[str, list[str]] = {wp: [] for wp in graph}

    for wp, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in inverse_graph:
                inverse_graph[dependency] = []
            inverse_graph[dependency].append(wp)

    return inverse_graph.get(wp_id, )

x_get_dependents__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_dependents__mutmut_1': x_get_dependents__mutmut_1, 
    'x_get_dependents__mutmut_2': x_get_dependents__mutmut_2, 
    'x_get_dependents__mutmut_3': x_get_dependents__mutmut_3, 
    'x_get_dependents__mutmut_4': x_get_dependents__mutmut_4, 
    'x_get_dependents__mutmut_5': x_get_dependents__mutmut_5, 
    'x_get_dependents__mutmut_6': x_get_dependents__mutmut_6, 
    'x_get_dependents__mutmut_7': x_get_dependents__mutmut_7, 
    'x_get_dependents__mutmut_8': x_get_dependents__mutmut_8
}
x_get_dependents__mutmut_orig.__name__ = 'x_get_dependents'


__all__ = [
    "build_dependency_graph",
    "detect_cycles",
    "get_dependents",
    "parse_wp_dependencies",
    "topological_sort",
    "validate_dependencies",
]
