"""Error types for context resolution and persistence."""

from __future__ import annotations


class ContextResolutionError(Exception):
    """Base class for context resolution failures."""


class MissionNotFoundError(ContextResolutionError):
    """Mission slug does not match any kitty-specs/ directory."""


# Backward-compatible alias during the mission-first cutover.
FeatureNotFoundError = MissionNotFoundError


class WorkPackageNotFoundError(ContextResolutionError):
    """wp_code not found in the mission's tasks/ directory."""


class MissingArgumentError(ContextResolutionError):
    """Required argument (wp_code or mission_slug) was not provided."""


class MissingIdentityError(ContextResolutionError):
    """project_uuid or mission_id is not assigned in project metadata."""


class ContextNotFoundError(Exception):
    """Persisted context token file does not exist."""


class ContextCorruptedError(Exception):
    """Persisted context token file contains invalid JSON."""
