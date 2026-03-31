"""Legacy feature-named compatibility surface for agent mission workflows.

The canonical CLI surface is ``agent mission-run`` with mission terminology.
This module keeps older internal tests and generated assets functional without
restoring feature naming to the main command tree.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Annotated

import typer

from specify_cli.cli.commands.accept import accept as _canonical_accept
from specify_cli.cli.commands.merge import merge as _canonical_merge

from . import mission_run as _mission_run

app = typer.Typer(
    name="feature",
    help="Legacy compatibility wrapper around agent mission-run commands.",
    no_args_is_help=True,
)

console = _mission_run.console

locate_project_root = _mission_run.locate_project_root
is_git_repo = _mission_run.is_git_repo
is_worktree_context = _mission_run.is_worktree_context
get_current_branch = _mission_run.get_current_branch
safe_commit = _mission_run.safe_commit
run_command = _mission_run.run_command
top_level_accept = _canonical_accept
top_level_merge = _canonical_merge
validate_mission_structure = _mission_run.validate_mission_structure
run_git_preflight = _mission_run.run_git_preflight
build_git_preflight_failure_payload = _mission_run.build_git_preflight_failure_payload


def get_next_feature_number(repo_root: Path) -> int:
    """Compatibility alias for legacy feature numbering helper."""
    return _mission_run.get_next_mission_number(repo_root)


def _find_latest_feature_worktree(repo_root: Path) -> Path | None:
    """Compatibility alias for legacy helper name."""
    return _mission_run._find_latest_mission_worktree(repo_root)


def _find_feature_worktree(repo_root: Path, feature: str) -> Path | None:
    """Compatibility alias for legacy helper name."""
    return _mission_run._find_mission_worktree(repo_root, feature)


def _get_current_branch(repo_root: Path) -> str:
    """Compatibility alias for legacy helper name."""
    return _mission_run._get_current_branch(repo_root)


def _sync_create_globals() -> None:
    _mission_run.locate_project_root = locate_project_root
    _mission_run.is_git_repo = is_git_repo
    _mission_run.is_worktree_context = is_worktree_context
    _mission_run.get_current_branch = get_current_branch
    _mission_run.get_next_mission_number = get_next_feature_number
    _mission_run.safe_commit = safe_commit
    _mission_run.run_command = run_command


def _sync_runtime_globals() -> None:
    _mission_run.locate_project_root = locate_project_root
    _mission_run.validate_mission_structure = validate_mission_structure
    _mission_run.run_git_preflight = run_git_preflight
    _mission_run.build_git_preflight_failure_payload = build_git_preflight_failure_payload
    _mission_run.safe_commit = safe_commit
    _mission_run.run_command = run_command


@app.command("create-feature")
def create_feature(
    feature_name: Annotated[str, typer.Argument(help="Mission slug (legacy compatibility wrapper)")],
    json_output: Annotated[bool, typer.Option("--json", help="Output JSON format")] = False,
    target_branch: Annotated[str | None, typer.Option("--target-branch", help="Target branch (defaults to current branch)")] = None,
) -> None:
    """Legacy wrapper for mission creation using feature terminology."""
    _sync_create_globals()
    _mission_run.create_mission(
        mission_name=feature_name,
        mission_type=None,
        mission_legacy=None,
        json_output=json_output,
        target_branch=target_branch,
    )


@app.command("check-prerequisites")
def check_prerequisites(
    feature: Annotated[str | None, typer.Option("--mission", help="Legacy alias for mission slug")] = None,
    json_output: Annotated[bool, typer.Option("--json", help="Output JSON format")] = False,
    paths_only: Annotated[bool, typer.Option("--paths-only", help="Only output path variables")] = False,
    include_tasks: Annotated[bool, typer.Option("--include-tasks", help="Include tasks.md in validation")] = False,
    require_tasks: Annotated[
        bool,
        typer.Option("--require-tasks", hidden=True, help="Deprecated alias for --include-tasks"),
    ] = False,
) -> None:
    """Legacy wrapper for mission prerequisite validation."""
    _sync_runtime_globals()
    _mission_run.check_prerequisites(
        mission=feature,
        json_output=json_output,
        paths_only=paths_only,
        include_tasks=include_tasks,
        require_tasks=require_tasks,
    )


@app.command("setup-plan")
def setup_plan(
    feature: Annotated[str | None, typer.Option("--mission", help="Legacy alias for mission slug")] = None,
    json_output: Annotated[bool, typer.Option("--json", help="Output JSON format")] = False,
) -> None:
    """Legacy wrapper for mission plan setup."""
    _sync_runtime_globals()
    _mission_run.setup_plan(mission=feature, json_output=json_output)


@app.command("finalize-tasks")
def finalize_tasks(
    feature: Annotated[str | None, typer.Option("--mission", help="Legacy alias for mission slug")] = None,
    json_output: Annotated[bool, typer.Option("--json", help="Output JSON format")] = False,
    validate_only: Annotated[
        bool,
        typer.Option("--validate-only", help="Run validations without committing"),
    ] = False,
) -> None:
    """Legacy wrapper for mission task finalization."""
    _sync_runtime_globals()
    _mission_run.finalize_tasks(
        mission=feature,
        json_output=json_output,
        validate_only=validate_only,
    )


@app.command("accept")
def accept_feature(
    mission: Annotated[str | None, typer.Option("--mission", help="Mission slug")] = None,
    feature: Annotated[str | None, typer.Option("--feature", hidden=True, help="[Deprecated] Use --mission")] = None,
    mode: Annotated[str, typer.Option("--mode", help="Acceptance mode: auto, pr, local, checklist")] = "auto",
    json_output: Annotated[bool, typer.Option("--json", help="Output results as JSON for agent parsing")] = False,
    lenient: Annotated[bool, typer.Option("--lenient", help="Skip strict metadata validation")] = False,
    no_commit: Annotated[bool, typer.Option("--no-commit", help="Skip auto-commit (report only)")] = False,
) -> None:
    """Legacy wrapper for mission acceptance."""
    mission_slug = mission or feature
    try:
        top_level_accept(
            feature=mission_slug,
            mode=mode,
            actor=None,
            test=[],
            json_output=json_output,
            lenient=lenient,
            no_commit=no_commit,
            allow_fail=False,
        )
    except TypeError:
        try:
            _canonical_accept(
                mission=mission_slug,
                mode=mode,
                actor=None,
                test=[],
                json_output=json_output,
                lenient=lenient,
                no_commit=no_commit,
                allow_fail=False,
            )
        except typer.Exit:
            raise
        except Exception as exc:
            if json_output:
                _mission_run._emit_json({"error": str(exc), "success": False})
            else:
                console.print(f"[red]Error:[/red] {exc}")
            raise typer.Exit(1) from exc
    except typer.Exit:
        raise
    except Exception as exc:
        if json_output:
            _mission_run._emit_json({"error": str(exc), "success": False})
        else:
            console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1) from exc


@app.command("merge")
def merge_feature(
    mission: Annotated[str | None, typer.Option("--mission", help="Mission slug")] = None,
    feature: Annotated[str | None, typer.Option("--feature", hidden=True, help="[Deprecated] Use --mission")] = None,
    target: Annotated[str | None, typer.Option("--target", help="Target branch to merge into")] = None,
    strategy: Annotated[str, typer.Option("--strategy", help="Merge strategy: merge, squash, rebase")] = "merge",
    push: Annotated[bool, typer.Option("--push", help="Push to origin after merging")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Show actions without executing")] = False,
    keep_branch: Annotated[bool, typer.Option("--keep-branch", help="Keep branch after merge")] = False,
    keep_worktree: Annotated[bool, typer.Option("--keep-worktree", help="Keep worktree after merge")] = False,
    auto_retry: Annotated[
        bool,
        typer.Option(
            "--auto-retry/--no-auto-retry",
            help="Auto-navigate to a deterministic mission worktree if in wrong location",
        ),
    ] = False,
) -> None:
    """Legacy wrapper for mission merge."""
    mission_slug = mission or feature
    if auto_retry and not os.environ.get("SPEC_KITTY_AUTORETRY"):
        repo_root = locate_project_root()
        if repo_root is None:
            raise typer.Exit(1)
        current_branch = _get_current_branch(repo_root)
        if len(current_branch) < 4 or not current_branch[:3].isdigit() or current_branch[3] != "-":
            if not mission_slug:
                console.print(
                    f"[red]Error:[/red] Not on mission branch ({current_branch}). "
                    "Auto-retry requires --mission to choose a deterministic mission worktree."
                )
                raise typer.Exit(1)
            retry_worktree = _find_feature_worktree(repo_root, mission_slug)
            if retry_worktree is None:
                console.print(
                    f"[red]Error:[/red] Could not find worktree for mission {mission_slug} "
                    f"under {repo_root / '.worktrees'}."
                )
                raise typer.Exit(1)
            console.print(
                f"[yellow]Auto-retry:[/yellow] Not on mission branch ({current_branch}). Running merge in {retry_worktree.name}"
            )
            env = dict(os.environ)
            env["SPEC_KITTY_AUTORETRY"] = "1"
            retry_cmd = ["spec-kitty", "agent", "feature", "merge", "--mission", mission_slug]
            if target:
                retry_cmd.extend(["--target", target])
            retry_cmd.extend(["--strategy", strategy])
            if push:
                retry_cmd.append("--push")
            if dry_run:
                retry_cmd.append("--dry-run")
            if keep_branch:
                retry_cmd.append("--keep-branch")
            if keep_worktree:
                retry_cmd.append("--keep-worktree")
            retry_cmd.append("--no-auto-retry")
            result = subprocess.run(retry_cmd, cwd=retry_worktree, env=env, check=False)
            raise SystemExit(result.returncode)

    try:
        top_level_merge(
            strategy=strategy,
            delete_branch=not keep_branch,
            remove_worktree=not keep_worktree,
            push=push,
            target_branch=target,
            dry_run=dry_run,
            feature=mission_slug,
            resume=False,
            abort=False,
        )
    except TypeError:
        try:
            _canonical_merge(
                strategy=strategy,
                delete_branch=not keep_branch,
                remove_worktree=not keep_worktree,
                push=push,
                target_branch=target,
                dry_run=dry_run,
                mission=mission_slug,
                resume=False,
                abort=False,
            )
        except typer.Exit:
            raise
        except Exception as exc:
            _mission_run._emit_json({"error": str(exc), "success": False})
            raise typer.Exit(1) from exc
    except typer.Exit:
        raise
    except Exception as exc:
        _mission_run._emit_json({"error": str(exc), "success": False})
        raise typer.Exit(1) from exc


__all__ = [
    "app",
    "accept_feature",
    "build_git_preflight_failure_payload",
    "check_prerequisites",
    "console",
    "create_feature",
    "finalize_tasks",
    "get_current_branch",
    "get_next_feature_number",
    "is_git_repo",
    "is_worktree_context",
    "locate_project_root",
    "merge_feature",
    "run_command",
    "run_git_preflight",
    "safe_commit",
    "setup_plan",
    "top_level_accept",
    "top_level_merge",
    "validate_mission_structure",
    "_find_feature_worktree",
    "_find_latest_feature_worktree",
    "_get_current_branch",
]
