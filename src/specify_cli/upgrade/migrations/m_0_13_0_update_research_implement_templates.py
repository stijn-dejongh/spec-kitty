"""Migration: Update research implement.md with CSV schema documentation.

This migration was originally designed to add the "Research CSV Schemas"
section to all agent implement slash commands for research missions.

As of WP10 (canonical context architecture), command templates were removed
in favor of shim generation.  This migration is permanently inert.
"""

from __future__ import annotations

from pathlib import Path

from ..registry import MigrationRegistry
from .base import BaseMigration, MigrationResult


@MigrationRegistry.register
class UpdateResearchImplementTemplatesMigration(BaseMigration):
    """Add Research CSV Schemas section to research implement slash commands.

    This migration:
    1. Loads the canonical research implement.md template from packaged missions
    2. Copies it to all agent slash command directories
    3. Only updates research templates (not software-dev)
    4. Skips agents that don't have research templates
    """

    migration_id = "0.13.0_update_research_implement_templates"
    description = "Add CSV schema docs to research implement slash commands"
    target_version = "0.13.0"

    MISSION_NAME = "research"
    TEMPLATE_FILE = "implement.md"
    SLASH_COMMAND_FILE = "spec-kitty.implement.md"

    def detect(self, project_path: Path) -> bool:  # noqa: ARG002
        """Always returns False — command templates removed in WP10 (canonical context architecture).

        Shim generation (spec-kitty agent shim) now replaces template-based agent commands.
        This migration is retained for history but is permanently inert.
        """
        return False

    def can_apply(self, project_path: Path) -> tuple[bool, str]:  # noqa: ARG002
        """Always returns False — command templates removed in WP10."""
        return (
            False,
            "Command templates were removed in WP10 (canonical context architecture). "
            "Shim generation replaces template-based commands.",
        )

    def apply(self, project_path: Path, dry_run: bool = False) -> MigrationResult:  # noqa: ARG002
        """Always returns no-op — command templates removed in WP10 (canonical context architecture).

        Shim generation (spec-kitty agent shim) now replaces template-based agent commands.
        This migration is retained for history but is permanently inert.
        """
        return MigrationResult(
            success=True,
            changes_made=["No-op: command templates removed in WP10 (canonical context architecture)"],
            errors=[],
            warnings=[],
        )
