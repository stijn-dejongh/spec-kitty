"""Focused tests for the private helpers T006 extracted from
``resolve_status_surface_with_anchor`` (campsite-clean WP01, IC-01).

This WP changes no behaviour: the broader resolver contract stays covered by
``test_surface_resolver_coord_empty_warning.py`` /
``test_surface_resolver_collapse.py`` / ``test_surface_resolver_solo_coord_primary.py``.
These tests call the two extracted private helpers directly, so the behaviour
they hold is pinned at the unit level even before a caller reaches them.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pytest
from mission_runtime import MissionTopology

from specify_cli.coordination.surface_resolver import (
    ResolvedStatusSurface,
    _empty_coord_surface,
    _meta_unreadable_fallback,
)

_LOGGER_NAME = "specify_cli.coordination.surface_resolver"


class TestEmptyCoordSurface:
    """``_empty_coord_surface`` — T006 extraction of the ``CoordState.EMPTY`` branch."""

    def test_lanes_with_coord_warns_and_returns_primary(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        """Today's behaviour (unchanged): the warning fires ONLY for
        ``LANES_WITH_COORD`` — a mission whose lane worktrees were provisioned
        to write into the coord root, so an empty one is genuinely unexpected.
        """
        feature_dir = tmp_path / "kitty-specs" / "demo-mission"
        composed_coord_dir = tmp_path / ".worktrees" / "demo-mission-coord" / "kitty-specs" / "demo-mission"

        with caplog.at_level(logging.WARNING, logger=_LOGGER_NAME):
            surface = _empty_coord_surface(
                feature_dir,
                composed_coord_dir,
                "demo-mission",
                MissionTopology.LANES_WITH_COORD,
            )

        assert isinstance(surface, ResolvedStatusSurface)
        # The returned surface is the PRIMARY dir, never the coord dir.
        assert surface.surface_path == feature_dir / "status.events.jsonl"
        assert surface.primary_anchor == feature_dir

        warnings = [r for r in caplog.records if r.levelno == logging.WARNING and r.name == _LOGGER_NAME]
        assert len(warnings) == 1, "expected exactly one WARNING-level record from the surface resolver logger"

    def test_solo_coord_stays_quiet_and_returns_primary(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        """Today's behaviour (unchanged): a solo (no-lanes) coord mission's empty
        coord root is the EXPECTED steady state pre-first-write — no warning.
        """
        feature_dir = tmp_path / "kitty-specs" / "solo-mission"
        composed_coord_dir = tmp_path / ".worktrees" / "solo-mission-coord" / "kitty-specs" / "solo-mission"

        with caplog.at_level(logging.WARNING, logger=_LOGGER_NAME):
            surface = _empty_coord_surface(
                feature_dir,
                composed_coord_dir,
                "solo-mission",
                MissionTopology.COORD,
            )

        assert surface.surface_path == feature_dir / "status.events.jsonl"
        assert surface.primary_anchor == feature_dir
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING and r.name == _LOGGER_NAME]
        assert warnings == [], "solo coord-topology empty fallback must stay quiet"

    def test_does_no_io(self, tmp_path: Path) -> None:
        """Purity: the helper never creates a directory or file (no side effects)."""
        feature_dir = tmp_path / "kitty-specs" / "pure-mission"
        composed_coord_dir = tmp_path / ".worktrees" / "pure-mission-coord" / "kitty-specs" / "pure-mission"

        _empty_coord_surface(feature_dir, composed_coord_dir, "pure-mission", MissionTopology.COORD)

        assert not feature_dir.exists()
        assert not composed_coord_dir.exists()


class TestMetaUnreadableFallback:
    """``_meta_unreadable_fallback`` — T006 extraction of the second ``meta is None`` arm."""

    def test_prefers_primary_dir_when_it_exists(self, tmp_path: Path) -> None:
        primary_dir = tmp_path / "kitty-specs" / "demo-mission"
        primary_dir.mkdir(parents=True)
        feature_dir = tmp_path / ".worktrees" / "demo-mission-coord" / "kitty-specs" / "demo-mission"

        surface = _meta_unreadable_fallback(primary_dir, feature_dir, "demo-mission")

        assert surface.primary_anchor == primary_dir
        assert surface.surface_path == primary_dir / "status.events.jsonl"

    def test_falls_back_to_feature_dir_when_primary_missing(self, tmp_path: Path) -> None:
        primary_dir = tmp_path / "kitty-specs" / "demo-mission"
        feature_dir = tmp_path / ".worktrees" / "demo-mission-coord" / "kitty-specs" / "demo-mission"
        feature_dir.mkdir(parents=True)

        surface = _meta_unreadable_fallback(primary_dir, feature_dir, "demo-mission")

        assert surface.primary_anchor == feature_dir
        assert surface.surface_path == feature_dir / "status.events.jsonl"

    def test_raises_file_not_found_when_neither_exists(self, tmp_path: Path) -> None:
        primary_dir = tmp_path / "kitty-specs" / "demo-mission"
        feature_dir = tmp_path / ".worktrees" / "demo-mission-coord" / "kitty-specs" / "demo-mission"

        with pytest.raises(FileNotFoundError, match="demo-mission"):
            _meta_unreadable_fallback(primary_dir, feature_dir, "demo-mission")
