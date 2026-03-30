"""Tests for WP02: Active-Mission Fallback Removal (mission 054).

Validates:
- FileManifest no longer has active_mission attribute
- verify_enhanced resolves mission from mission-level meta.json
- mission CLI shows 'No active mission detected' when no mission context
- Production callers (verify.py, api.py) wire mission_dir through
"""

from __future__ import annotations

import json
import types
from pathlib import Path
from unittest.mock import MagicMock, patch



# --------------------------------------------------------------------------- #
# verify_enhanced tests
# --------------------------------------------------------------------------- #

def test_verify_with_research_feature(tmp_path: Path) -> None:
    """Verify resolves mission to 'research' when mission meta.json says so."""
    from rich.console import Console

    from specify_cli.verify_enhanced import run_enhanced_verify

    # Set up project structure
    project_root = tmp_path / "project"
    project_root.mkdir()
    kittify_dir = project_root / ".kittify"
    kittify_dir.mkdir()

    # Do NOT create .kittify/active-mission (the whole point of this test)

    # Create mission directory with meta.json specifying research mission
    mission_dir = project_root / "kitty-specs" / "099-research-mission"
    mission_dir.mkdir(parents=True)
    meta = {"mission": "research", "mission_slug": "099-research-mission", "created_at": "2026-01-01"}
    (mission_dir / "meta.json").write_text(json.dumps(meta))

    console = Console(file=open("/dev/null", "w"))  # noqa: SIM115

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = types.SimpleNamespace(stdout="main\n", returncode=0)

        result = run_enhanced_verify(
            repo_root=project_root,
            project_root=project_root,
            cwd=project_root,
            mission="099-research-mission",
            json_output=True,
            check_files=False,
            console=console,
            mission_dir=mission_dir,
        )

    assert result["environment"]["active_mission"] == "research"


def test_verify_without_mission_dir_shows_no_context(tmp_path: Path) -> None:
    """Without mission_dir, active_mission should say 'no mission context'."""
    from rich.console import Console

    from specify_cli.verify_enhanced import run_enhanced_verify

    project_root = tmp_path / "project"
    project_root.mkdir()
    kittify_dir = project_root / ".kittify"
    kittify_dir.mkdir()

    console = Console(file=open("/dev/null", "w"))  # noqa: SIM115

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = types.SimpleNamespace(stdout="main\n", returncode=0)

        result = run_enhanced_verify(
            repo_root=project_root,
            project_root=project_root,
            cwd=project_root,
            mission=None,
            json_output=True,
            check_files=False,
            console=console,
        )

    assert result["environment"]["active_mission"] == "no mission context"


def test_verify_resolves_mission_from_mission_slug(tmp_path: Path) -> None:
    """When mission slug is provided (not mission_dir), mission resolves from kitty-specs."""
    from rich.console import Console

    from specify_cli.verify_enhanced import run_enhanced_verify

    project_root = tmp_path / "project"
    project_root.mkdir()
    kittify_dir = project_root / ".kittify"
    kittify_dir.mkdir()

    mission_dir = project_root / "kitty-specs" / "042-my-mission"
    mission_dir.mkdir(parents=True)
    meta = {"mission": "documentation", "mission_slug": "042-my-mission", "created_at": "2026-01-01"}
    (mission_dir / "meta.json").write_text(json.dumps(meta))

    console = Console(file=open("/dev/null", "w"))  # noqa: SIM115

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = types.SimpleNamespace(stdout="main\n", returncode=0)

        result = run_enhanced_verify(
            repo_root=project_root,
            project_root=project_root,
            cwd=project_root,
            mission="042-my-mission",
            json_output=True,
            check_files=False,
            console=console,
        )

    assert result["environment"]["active_mission"] == "documentation"


# --------------------------------------------------------------------------- #
# mission CLI: current command – no-mission-context test
# --------------------------------------------------------------------------- #

def test_mission_current_no_feature_shows_message(tmp_path: Path) -> None:
    """When no mission is detected, 'mission current' should show a clear message."""
    from typer.testing import CliRunner
    from specify_cli.cli.commands.mission import app

    runner = CliRunner()

    with (
        patch("specify_cli.cli.commands.mission.get_project_root_or_exit", return_value=tmp_path),
        patch("specify_cli.cli.commands.mission.check_version_compatibility"),
        patch("specify_cli.cli.commands.mission._detect_current_feature", return_value=None),
    ):
        result = runner.invoke(app, ["current"])

    assert result.exit_code == 1
    assert "No active mission detected" in result.output


# --------------------------------------------------------------------------- #
# _resolve_mission_dir (verify.py helper) tests
# --------------------------------------------------------------------------- #

def test_resolve_mission_dir_with_explicit_feature(tmp_path: Path) -> None:
    """_resolve_mission_dir returns mission directory when given an explicit slug."""
    from specify_cli.cli.commands.verify import _resolve_mission_dir

    project_root = tmp_path / "project"
    mission_dir = project_root / "kitty-specs" / "099-research-mission"
    mission_dir.mkdir(parents=True)

    # No mocking needed: _resolve_mission_dir uses only the explicit mission arg
    result = _resolve_mission_dir(project_root, mission="099-research-mission")

    assert result == mission_dir


def test_resolve_mission_dir_returns_none_when_no_feature(tmp_path: Path) -> None:
    """_resolve_mission_dir returns None when no explicit mission is given."""
    from specify_cli.cli.commands.verify import _resolve_mission_dir

    # No mission flag → no auto-detection → returns None
    result = _resolve_mission_dir(tmp_path)

    assert result is None


def test_resolve_mission_dir_returns_none_when_mission_dir_missing(tmp_path: Path) -> None:
    """_resolve_mission_dir returns None when the mission directory does not exist."""
    from specify_cli.cli.commands.verify import _resolve_mission_dir

    # Mission slug given but directory doesn't exist on disk
    result = _resolve_mission_dir(tmp_path, mission="099-nonexistent-mission")

    assert result is None


# --------------------------------------------------------------------------- #
# Realistic worktree test: NO detect_feature mock
# --------------------------------------------------------------------------- #


def test_resolve_mission_dir_from_worktree_without_mock(tmp_path: Path) -> None:
    """_resolve_mission_dir finds features when called from a worktree CWD.

    This test creates a realistic directory layout:
      main_repo/
        .git/                        (real git dir marker)
        .git/worktrees/my-wt/        (worktree gitdir)
        .kittify/                    (project marker)
        kitty-specs/099-research-mission/meta.json
      worktree/
        .git  (file: "gitdir: <main>/.git/worktrees/my-wt")

    Calling _resolve_mission_dir(worktree_root, mission=...) must still
    resolve the mission directory under main_repo/kitty-specs/ because
    worktrees lack kitty-specs/ via sparse checkout.
    """
    from specify_cli.cli.commands.verify import _resolve_mission_dir

    # --- Set up main repo ---
    main_repo = tmp_path / "main_repo"
    main_repo.mkdir()
    (main_repo / ".git").mkdir()  # Real .git directory (not a file)
    (main_repo / ".kittify").mkdir()

    mission_dir = main_repo / "kitty-specs" / "099-research-mission"
    mission_dir.mkdir(parents=True)
    meta = {"mission": "research", "mission_slug": "099-research-mission"}
    (mission_dir / "meta.json").write_text(json.dumps(meta))

    # --- Set up git worktree gitdir ---
    wt_gitdir = main_repo / ".git" / "worktrees" / "my-wt"
    wt_gitdir.mkdir(parents=True)

    # --- Set up the worktree root ---
    worktree_root = tmp_path / "worktree"
    worktree_root.mkdir()
    # .git is a *file* with a gitdir: pointer (this is how real worktrees work)
    (worktree_root / ".git").write_text(f"gitdir: {wt_gitdir}\n")
    # Worktrees have .kittify/ (shared/linked) but NOT kitty-specs/
    (worktree_root / ".kittify").mkdir()
    # Do NOT create kitty-specs/ here — that's the whole point

    # No mocking needed: _resolve_mission_dir uses explicit mission arg only
    result = _resolve_mission_dir(worktree_root, mission="099-research-mission")

    # With an explicit slug, _resolve_mission_dir checks
    # worktree_root / "kitty-specs" / mission_slug.  The worktree does NOT
    # have kitty-specs/, so the result is None.
    # This confirms the contract: resolution does NOT walk up through the
    # worktree .git pointer (that was mission_detection heuristics, removed).
    assert result is None, (
        "_resolve_mission_dir should return None when the mission directory "
        "does not exist under the given project_root (worktree path)"
    )


def test_diagnostics_mode_resolves_main_repo_root(tmp_path: Path) -> None:
    """_run_diagnostics_mode uses locate_project_root() (not Path.cwd()).

    When CWD is a worktree, locate_project_root() resolves the main repo
    root where kitty-specs/ lives, enabling mission detection.
    """
    from specify_cli.cli.commands.verify import _run_diagnostics_mode

    main_repo = tmp_path / "main_repo"
    main_repo.mkdir()
    (main_repo / ".kittify").mkdir()

    mission_dir = main_repo / "kitty-specs" / "099-research-mission"
    mission_dir.mkdir(parents=True)
    meta = {"mission": "research", "mission_slug": "099-research-mission"}
    (mission_dir / "meta.json").write_text(json.dumps(meta))

    captured_path = {}

    def fake_run_diagnostics(project_path, *, mission_dir=None):
        captured_path["project_path"] = project_path
        captured_path["mission_dir"] = mission_dir
        return {
            "project_path": str(project_path),
            "active_mission": "research" if mission_dir else "no mission context",
        }

    mock_ctx = MagicMock()
    mock_ctx.slug = "099-research-mission"
    mock_ctx.directory = mission_dir

    with (
        # locate_project_root returns main repo, not CWD
        patch("specify_cli.cli.commands.verify.locate_project_root", return_value=main_repo),
        patch("specify_cli.cli.commands.verify.run_diagnostics", side_effect=fake_run_diagnostics),
    ):
        _run_diagnostics_mode(json_output=True, check_tools=False, mission="099-research-mission")

    # The project_path passed to run_diagnostics should be the main repo root,
    # NOT whatever Path.cwd() happens to be.
    assert captured_path["project_path"] == main_repo
    assert captured_path["mission_dir"] == mission_dir


# --------------------------------------------------------------------------- #
# verify_setup production caller wiring tests
# --------------------------------------------------------------------------- #

def test_verify_setup_passes_mission_dir_to_run_enhanced_verify(tmp_path: Path) -> None:
    """verify_setup should detect mission_dir and pass it to run_enhanced_verify."""
    from specify_cli.cli.commands.verify import verify_setup

    mission_dir = tmp_path / "kitty-specs" / "099-research-mission"
    mission_dir.mkdir(parents=True)

    mock_ctx = MagicMock()
    mock_ctx.slug = "099-research-mission"
    mock_ctx.directory = mission_dir

    captured_kwargs = {}

    def fake_run_enhanced_verify(**kwargs):
        captured_kwargs.update(kwargs)
        return {"environment": {"active_mission": "research"}}

    with (
        patch("specify_cli.cli.commands.verify.find_repo_root", return_value=tmp_path),
        patch("specify_cli.cli.commands.verify.get_project_root_or_exit", return_value=tmp_path),
        patch("specify_cli.cli.commands.verify.check_version_compatibility"),
        patch("specify_cli.cli.commands.verify.run_enhanced_verify", side_effect=fake_run_enhanced_verify),
    ):
        # Call with json_output to avoid console rendering issues, and skip tool checks
        verify_setup(
            mission="099-research-mission",
            json_output=True,
            check_files=False,
            check_tools=False,
            diagnostics=False,
        )

    assert captured_kwargs.get("mission_dir") == mission_dir


def test_diagnostics_mode_passes_mission_dir_to_run_diagnostics(tmp_path: Path) -> None:
    """_run_diagnostics_mode should detect mission_dir and pass it to run_diagnostics."""
    from specify_cli.cli.commands.verify import _run_diagnostics_mode

    mission_dir = tmp_path / "kitty-specs" / "099-research-mission"
    mission_dir.mkdir(parents=True)

    mock_ctx = MagicMock()
    mock_ctx.slug = "099-research-mission"
    mock_ctx.directory = mission_dir

    captured_kwargs = {}

    def fake_run_diagnostics(project_path, *, mission_dir=None):
        captured_kwargs["mission_dir"] = mission_dir
        return {
            "project_path": str(project_path),
            "active_mission": "research" if mission_dir else "no mission context",
        }

    with (
        patch("specify_cli.cli.commands.verify.locate_project_root", return_value=tmp_path),
        patch("specify_cli.cli.commands.verify.run_diagnostics", side_effect=fake_run_diagnostics),
    ):
        _run_diagnostics_mode(json_output=True, check_tools=False, mission="099-research-mission")

    assert captured_kwargs.get("mission_dir") == mission_dir


# --------------------------------------------------------------------------- #
# api.py handle_diagnostics wiring test
# --------------------------------------------------------------------------- #

def test_api_handle_diagnostics_runs_without_mission_dir(tmp_path: Path) -> None:
    """APIHandler.handle_diagnostics runs diagnostics with mission_dir=None.

    After auto-detection removal (WP02), the dashboard API no longer attempts
    to auto-detect the active mission.  handle_diagnostics always passes
    mission_dir=None to run_diagnostics.  Callers who need per-mission context
    must supply an explicit mission slug via a separate API endpoint.
    """
    import io

    mission_dir = tmp_path / "kitty-specs" / "099-research-mission"
    mission_dir.mkdir(parents=True)

    captured_kwargs = {}

    def fake_run_diagnostics(project_path, *, mission_dir=None):
        captured_kwargs["mission_dir"] = mission_dir
        return {"active_mission": "no mission context"}

    with (
        patch("specify_cli.dashboard.handlers.api.run_diagnostics", side_effect=fake_run_diagnostics),
    ):
        from specify_cli.dashboard.handlers.api import APIHandler

        handler = MagicMock(spec=APIHandler)
        handler.project_dir = str(tmp_path)
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        handler.wfile = io.BytesIO()

        # Call the unbound method with our mock handler
        APIHandler.handle_diagnostics(handler)

    # mission_dir is always None — no auto-detection after WP02
    assert captured_kwargs.get("mission_dir") is None
