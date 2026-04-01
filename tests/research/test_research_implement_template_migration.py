"""Tests for research implement template migration (0.13.0).

As of WP10 (canonical context architecture), this migration is permanently
inert.  Tests validate that detect(), can_apply(), and apply() all return
the expected inert results, and that the canonical template source in the
doctrine package still exists with the correct schema content.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from specify_cli.upgrade.migrations.m_0_13_0_update_research_implement_templates import (
    UpdateResearchImplementTemplatesMigration,
)

pytestmark = pytest.mark.fast


class TestInertMigration:
    """All three migration entry-points are permanently inert (WP10)."""

    def test_detect_always_false(self, tmp_path):
        """detect() returns False regardless of project state."""
        migration = UpdateResearchImplementTemplatesMigration()
        assert migration.detect(tmp_path) is False

    def test_can_apply_always_false(self, tmp_path):
        """can_apply() returns (False, <reason>)."""
        migration = UpdateResearchImplementTemplatesMigration()
        can_apply, reason = migration.can_apply(tmp_path)

        assert can_apply is False
        assert "WP10" in reason

    def test_apply_returns_success_noop(self, tmp_path):
        """apply() returns success with a no-op change message."""
        migration = UpdateResearchImplementTemplatesMigration()
        result = migration.apply(tmp_path, dry_run=False)

        assert result.success is True
        assert len(result.errors) == 0
        assert any("No-op" in c or "no-op" in c.lower() for c in result.changes_made)

    def test_apply_dry_run_returns_success_noop(self, tmp_path):
        """apply(dry_run=True) also returns success with no-op."""
        migration = UpdateResearchImplementTemplatesMigration()
        result = migration.apply(tmp_path, dry_run=True)

        assert result.success is True
        assert len(result.errors) == 0

    def test_migration_metadata(self):
        """Migration retains correct metadata for the registry."""
        migration = UpdateResearchImplementTemplatesMigration()
        assert migration.migration_id == "0.13.0_update_research_implement_templates"
        assert migration.target_version == "0.13.0"


class TestTemplateContent:
    """Tests for template content quality in doctrine package."""

    def test_template_source_exists(self):
        """Test that research implement template source file exists."""
        repo_root = Path(__file__).resolve().parents[2]
        template_path = (
            repo_root / "src" / "doctrine" / "missions" / "research" / "command-templates" / "implement.md"
        )
        assert template_path.exists()

        content = template_path.read_text()

        # Should have all required sections
        assert "Research CSV Schemas" in content
        assert "evidence-log.csv Schema" in content
        assert "source-register.csv Schema" in content
        assert "CRITICAL - DO NOT MODIFY HEADERS" in content

    def test_template_has_correct_schemas(self):
        """Test template documents correct canonical schemas."""
        repo_root = Path(__file__).resolve().parents[2]
        template_path = (
            repo_root / "src" / "doctrine" / "missions" / "research" / "command-templates" / "implement.md"
        )
        content = template_path.read_text()

        # Evidence log schema
        assert "timestamp,source_type,citation,key_finding,confidence,notes" in content

        # Source register schema
        assert "source_id,citation,url,accessed_date,relevance,status" in content
