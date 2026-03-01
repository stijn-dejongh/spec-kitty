"""Shared dependency validation utilities for implement command.

This module provides validation logic for work package dependencies,
ensuring that workspaces are created with correct base branches.

Used by both:
- Top-level `spec-kitty implement` command
- Agent `spec-kitty agent workflow implement` command
"""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from specify_cli.core.dependency_graph import parse_wp_dependencies

console = Console()
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


def validate_and_resolve_base(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    args = [wp_id, wp_file, base, feature_slug, repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_validate_and_resolve_base__mutmut_orig, x_validate_and_resolve_base__mutmut_mutants, args, kwargs, None)


def x_validate_and_resolve_base__mutmut_orig(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_1(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = None

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_2(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(None)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_3(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) >= 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_4(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 2:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_5(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is not None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_6(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(None)
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_7(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(None)
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_8(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(None)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_9(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {'XX, XX'.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_10(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(None)
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_11(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, False)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_12(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_13(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    None
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_14(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(None)
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_15(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, True)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_16(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) != 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_17(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 2:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_18(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is not None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_19(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(None)
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_20(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[1]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_21(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(None)
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_22(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(None)
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_23(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[1]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_24(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(None)
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_25(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                None
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_26(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[1]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_27(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(None)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_28(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(2)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_29(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_30(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                None
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_31(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(None)
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_32(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, True)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, False)


def x_validate_and_resolve_base__mutmut_33(
    wp_id: str,
    wp_file: Path,
    base: str | None,
    feature_slug: str,
    repo_root: Path
) -> tuple[str | None, bool]:
    """Validate dependencies and resolve base workspace.

    This function implements the core dependency validation logic:
    - Multi-parent: Returns (None, True) to trigger auto-merge mode
    - Single parent: Errors if --base not provided, validates if provided
    - No dependencies: Accepts provided base or None (branches from main)

    Args:
        wp_id: Work package ID (e.g., "WP01")
        wp_file: Path to WP markdown file
        base: Base WP ID from --base flag (may be None)
        feature_slug: Feature slug (e.g., "010-my-feature")
        repo_root: Repository root path

    Returns:
        Tuple of (base_to_use, auto_merge_mode):
        - base_to_use: The base WP ID to use, or None for main/auto-merge
        - auto_merge_mode: True if should create multi-parent merge base

    Raises:
        typer.Exit: If validation fails (missing --base, invalid base, etc.)
    """
    # Parse dependencies from WP frontmatter
    declared_deps = parse_wp_dependencies(wp_file)

    # Multi-parent dependency handling
    if len(declared_deps) > 1:
        if base is None:
            # Auto-merge mode: Create merge commit combining all dependencies
            console.print(f"\n[cyan]Multi-parent dependency detected:[/cyan]")
            console.print(f"  {wp_id} depends on: {', '.join(declared_deps)}")
            console.print(f"  Auto-creating merge base combining all dependencies...")
            return (None, True)  # Auto-merge mode
        else:
            # User provided explicit base - validate it's in dependencies
            if base not in declared_deps:
                console.print(
                    f"[yellow]Warning:[/yellow] {wp_id} doesn't declare {base} "
                    f"as dependency"
                )
                console.print(f"Declared dependencies: {declared_deps}")
                # Allow but warn (user might know better than parser)
            return (base, False)  # Use provided base, no auto-merge

    # Single dependency handling
    elif len(declared_deps) == 1:
        if base is None:
            # ERROR: Must provide --base for single dependency
            console.print(f"\n[red]Error:[/red] {wp_id} depends on {declared_deps[0]}")
            console.print(f"\nSpecify base workspace:")
            console.print(f"  spec-kitty implement {wp_id} --base {declared_deps[0]}")
            console.print(f"\n[dim]Or for agent commands:[/dim]")
            console.print(
                f"  spec-kitty agent workflow implement {wp_id} "
                f"--base {declared_deps[0]} --agent <name>"
            )
            raise typer.Exit(1)

        # Validate provided base matches dependency
        if base not in declared_deps:
            console.print(
                f"[yellow]Warning:[/yellow] {wp_id} does not declare dependency "
                f"on {base}"
            )
            console.print(f"Declared dependencies: {declared_deps}")
            # Allow but warn (user might know better than parser)

        return (base, False)  # Use provided base

    # No dependencies
    else:
        # Accept any provided base (or None for main)
        return (base, True)

x_validate_and_resolve_base__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_validate_and_resolve_base__mutmut_1': x_validate_and_resolve_base__mutmut_1, 
    'x_validate_and_resolve_base__mutmut_2': x_validate_and_resolve_base__mutmut_2, 
    'x_validate_and_resolve_base__mutmut_3': x_validate_and_resolve_base__mutmut_3, 
    'x_validate_and_resolve_base__mutmut_4': x_validate_and_resolve_base__mutmut_4, 
    'x_validate_and_resolve_base__mutmut_5': x_validate_and_resolve_base__mutmut_5, 
    'x_validate_and_resolve_base__mutmut_6': x_validate_and_resolve_base__mutmut_6, 
    'x_validate_and_resolve_base__mutmut_7': x_validate_and_resolve_base__mutmut_7, 
    'x_validate_and_resolve_base__mutmut_8': x_validate_and_resolve_base__mutmut_8, 
    'x_validate_and_resolve_base__mutmut_9': x_validate_and_resolve_base__mutmut_9, 
    'x_validate_and_resolve_base__mutmut_10': x_validate_and_resolve_base__mutmut_10, 
    'x_validate_and_resolve_base__mutmut_11': x_validate_and_resolve_base__mutmut_11, 
    'x_validate_and_resolve_base__mutmut_12': x_validate_and_resolve_base__mutmut_12, 
    'x_validate_and_resolve_base__mutmut_13': x_validate_and_resolve_base__mutmut_13, 
    'x_validate_and_resolve_base__mutmut_14': x_validate_and_resolve_base__mutmut_14, 
    'x_validate_and_resolve_base__mutmut_15': x_validate_and_resolve_base__mutmut_15, 
    'x_validate_and_resolve_base__mutmut_16': x_validate_and_resolve_base__mutmut_16, 
    'x_validate_and_resolve_base__mutmut_17': x_validate_and_resolve_base__mutmut_17, 
    'x_validate_and_resolve_base__mutmut_18': x_validate_and_resolve_base__mutmut_18, 
    'x_validate_and_resolve_base__mutmut_19': x_validate_and_resolve_base__mutmut_19, 
    'x_validate_and_resolve_base__mutmut_20': x_validate_and_resolve_base__mutmut_20, 
    'x_validate_and_resolve_base__mutmut_21': x_validate_and_resolve_base__mutmut_21, 
    'x_validate_and_resolve_base__mutmut_22': x_validate_and_resolve_base__mutmut_22, 
    'x_validate_and_resolve_base__mutmut_23': x_validate_and_resolve_base__mutmut_23, 
    'x_validate_and_resolve_base__mutmut_24': x_validate_and_resolve_base__mutmut_24, 
    'x_validate_and_resolve_base__mutmut_25': x_validate_and_resolve_base__mutmut_25, 
    'x_validate_and_resolve_base__mutmut_26': x_validate_and_resolve_base__mutmut_26, 
    'x_validate_and_resolve_base__mutmut_27': x_validate_and_resolve_base__mutmut_27, 
    'x_validate_and_resolve_base__mutmut_28': x_validate_and_resolve_base__mutmut_28, 
    'x_validate_and_resolve_base__mutmut_29': x_validate_and_resolve_base__mutmut_29, 
    'x_validate_and_resolve_base__mutmut_30': x_validate_and_resolve_base__mutmut_30, 
    'x_validate_and_resolve_base__mutmut_31': x_validate_and_resolve_base__mutmut_31, 
    'x_validate_and_resolve_base__mutmut_32': x_validate_and_resolve_base__mutmut_32, 
    'x_validate_and_resolve_base__mutmut_33': x_validate_and_resolve_base__mutmut_33
}
x_validate_and_resolve_base__mutmut_orig.__name__ = 'x_validate_and_resolve_base'


def validate_base_workspace_exists(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    args = [base, feature_slug, repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_validate_base_workspace_exists__mutmut_orig, x_validate_base_workspace_exists__mutmut_mutants, args, kwargs, None)


def x_validate_base_workspace_exists__mutmut_orig(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_1(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = None

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_2(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" * f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_3(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root * ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_4(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / "XX.worktreesXX" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_5(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".WORKTREES" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_6(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_7(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(None)
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_8(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(None)
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_9(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(None)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_10(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(2)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_11(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = None

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_12(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        None,
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_13(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=None,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_14(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=None,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_15(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=None
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_16(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_17(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_18(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_19(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_20(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["XXgitXX", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_21(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["GIT", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_22(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "XXrev-parseXX", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_23(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "REV-PARSE", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_24(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "XX--git-dirXX"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_25(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--GIT-DIR"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_26(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=False,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_27(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=True
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_28(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode == 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_29(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 1:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_30(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            None
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_31(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print(None)
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_32(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("XXThis directory may be corrupted. Remove it and re-create:XX")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_33(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("this directory may be corrupted. remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_34(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("THIS DIRECTORY MAY BE CORRUPTED. REMOVE IT AND RE-CREATE:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_35(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(None)
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_36(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(None)
        raise typer.Exit(1)


def x_validate_base_workspace_exists__mutmut_37(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(None)


def x_validate_base_workspace_exists__mutmut_38(
    base: str,
    feature_slug: str,
    repo_root: Path
) -> None:
    """Validate that a base workspace exists and is valid.

    Args:
        base: Base WP ID (e.g., "WP01")
        feature_slug: Feature slug
        repo_root: Repository root path

    Raises:
        typer.Exit: If base workspace doesn't exist or is invalid
    """
    import subprocess

    base_workspace = repo_root / ".worktrees" / f"{feature_slug}-{base}"

    if not base_workspace.exists():
        console.print(f"\n[red]Error:[/red] Base workspace {base} does not exist")
        console.print(f"Implement {base} first: spec-kitty implement {base}")
        raise typer.Exit(1)

    # Verify it's a valid worktree
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=base_workspace,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        console.print(
            f"[red]Error:[/red] {base_workspace} exists but is not a valid worktree"
        )
        console.print("This directory may be corrupted. Remove it and re-create:")
        console.print(f"  rm -rf {base_workspace}")
        console.print(f"  spec-kitty implement {base}")
        raise typer.Exit(2)

x_validate_base_workspace_exists__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_validate_base_workspace_exists__mutmut_1': x_validate_base_workspace_exists__mutmut_1, 
    'x_validate_base_workspace_exists__mutmut_2': x_validate_base_workspace_exists__mutmut_2, 
    'x_validate_base_workspace_exists__mutmut_3': x_validate_base_workspace_exists__mutmut_3, 
    'x_validate_base_workspace_exists__mutmut_4': x_validate_base_workspace_exists__mutmut_4, 
    'x_validate_base_workspace_exists__mutmut_5': x_validate_base_workspace_exists__mutmut_5, 
    'x_validate_base_workspace_exists__mutmut_6': x_validate_base_workspace_exists__mutmut_6, 
    'x_validate_base_workspace_exists__mutmut_7': x_validate_base_workspace_exists__mutmut_7, 
    'x_validate_base_workspace_exists__mutmut_8': x_validate_base_workspace_exists__mutmut_8, 
    'x_validate_base_workspace_exists__mutmut_9': x_validate_base_workspace_exists__mutmut_9, 
    'x_validate_base_workspace_exists__mutmut_10': x_validate_base_workspace_exists__mutmut_10, 
    'x_validate_base_workspace_exists__mutmut_11': x_validate_base_workspace_exists__mutmut_11, 
    'x_validate_base_workspace_exists__mutmut_12': x_validate_base_workspace_exists__mutmut_12, 
    'x_validate_base_workspace_exists__mutmut_13': x_validate_base_workspace_exists__mutmut_13, 
    'x_validate_base_workspace_exists__mutmut_14': x_validate_base_workspace_exists__mutmut_14, 
    'x_validate_base_workspace_exists__mutmut_15': x_validate_base_workspace_exists__mutmut_15, 
    'x_validate_base_workspace_exists__mutmut_16': x_validate_base_workspace_exists__mutmut_16, 
    'x_validate_base_workspace_exists__mutmut_17': x_validate_base_workspace_exists__mutmut_17, 
    'x_validate_base_workspace_exists__mutmut_18': x_validate_base_workspace_exists__mutmut_18, 
    'x_validate_base_workspace_exists__mutmut_19': x_validate_base_workspace_exists__mutmut_19, 
    'x_validate_base_workspace_exists__mutmut_20': x_validate_base_workspace_exists__mutmut_20, 
    'x_validate_base_workspace_exists__mutmut_21': x_validate_base_workspace_exists__mutmut_21, 
    'x_validate_base_workspace_exists__mutmut_22': x_validate_base_workspace_exists__mutmut_22, 
    'x_validate_base_workspace_exists__mutmut_23': x_validate_base_workspace_exists__mutmut_23, 
    'x_validate_base_workspace_exists__mutmut_24': x_validate_base_workspace_exists__mutmut_24, 
    'x_validate_base_workspace_exists__mutmut_25': x_validate_base_workspace_exists__mutmut_25, 
    'x_validate_base_workspace_exists__mutmut_26': x_validate_base_workspace_exists__mutmut_26, 
    'x_validate_base_workspace_exists__mutmut_27': x_validate_base_workspace_exists__mutmut_27, 
    'x_validate_base_workspace_exists__mutmut_28': x_validate_base_workspace_exists__mutmut_28, 
    'x_validate_base_workspace_exists__mutmut_29': x_validate_base_workspace_exists__mutmut_29, 
    'x_validate_base_workspace_exists__mutmut_30': x_validate_base_workspace_exists__mutmut_30, 
    'x_validate_base_workspace_exists__mutmut_31': x_validate_base_workspace_exists__mutmut_31, 
    'x_validate_base_workspace_exists__mutmut_32': x_validate_base_workspace_exists__mutmut_32, 
    'x_validate_base_workspace_exists__mutmut_33': x_validate_base_workspace_exists__mutmut_33, 
    'x_validate_base_workspace_exists__mutmut_34': x_validate_base_workspace_exists__mutmut_34, 
    'x_validate_base_workspace_exists__mutmut_35': x_validate_base_workspace_exists__mutmut_35, 
    'x_validate_base_workspace_exists__mutmut_36': x_validate_base_workspace_exists__mutmut_36, 
    'x_validate_base_workspace_exists__mutmut_37': x_validate_base_workspace_exists__mutmut_37, 
    'x_validate_base_workspace_exists__mutmut_38': x_validate_base_workspace_exists__mutmut_38
}
x_validate_base_workspace_exists__mutmut_orig.__name__ = 'x_validate_base_workspace_exists'


__all__ = [
    "validate_and_resolve_base",
    "validate_base_workspace_exists",
]
