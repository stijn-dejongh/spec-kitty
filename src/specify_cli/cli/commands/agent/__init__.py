"""Agent command namespace for AI agents to execute spec-kitty workflows programmatically."""

import typer

from . import config, context, feature, mission_run, profile, release, status, tasks, workflow
from specify_cli.cli.commands import shim as shim_module

app = typer.Typer(
    name="agent", help="Commands for AI agents to execute spec-kitty workflows programmatically", no_args_is_help=True
)

# Register sub-apps for each command module
app.add_typer(config.app, name="config")
app.add_typer(mission_run.app, name="mission-run")
app.add_typer(mission_run.app, name="mission")
app.add_typer(feature.app, name="feature")
app.add_typer(tasks.app, name="tasks")
app.add_typer(context.app, name="context")
app.add_typer(profile.app, name="profile")
app.add_typer(release.app, name="release")
app.add_typer(workflow.app, name="workflow")
app.add_typer(status.app, name="status")
app.add_typer(shim_module.app, name="shim")


@app.command("check-prerequisites")
def check_prerequisites_alias(
    feature_slug: str | None = typer.Option(None, "--feature", hidden=True, help="[Deprecated] Use --mission"),
    mission: str | None = typer.Option(None, "--mission", help="Mission slug"),
    json_output: bool = typer.Option(False, "--json", help="Output JSON format"),
    paths_only: bool = typer.Option(False, "--paths-only", help="Only output path variables"),
    include_tasks: bool = typer.Option(False, "--include-tasks", help="Include tasks.md in validation"),
    require_tasks: bool = typer.Option(False, "--require-tasks", hidden=True, help="Deprecated alias for --include-tasks"),
) -> None:
    """Deprecated forwarding alias for agent feature check-prerequisites."""
    feature.check_prerequisites(
        feature=mission or feature_slug,
        json_output=json_output,
        paths_only=paths_only,
        include_tasks=include_tasks,
        require_tasks=require_tasks,
    )


__all__ = ["app"]
