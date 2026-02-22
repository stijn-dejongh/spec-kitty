"""Tests for resolve_governance() with rich doctrine AgentProfile.

Verifies the new ``profile_repository`` path in ``resolve_governance()``:
- When ``profile_repository`` is passed (and ``profile_catalog`` is not),
  the catalog is built from rich ``AgentProfile`` objects keyed by
  ``profile_id``.
- The returned ``GovernanceResolution.agent_profiles`` are rich objects.
- ``profile_catalog`` still takes precedence over ``profile_repository``.
- The legacy agents.yaml path (neither arg supplied) still works.
"""

from pathlib import Path

import pytest

from specify_cli.constitution.resolver import (
    GovernanceResolutionError,
    collect_governance_diagnostics,
    resolve_governance,
)
from doctrine.agent_profiles.profile import AgentProfile
from doctrine.agent_profiles.repository import AgentProfileRepository


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_constitution_files(
    root: Path,
    *,
    governance: str,
    agents: str = "profiles: []\nselection: {}\n",
    directives: str = "directives: []\n",
) -> Path:
    """Write minimal constitution YAML files under ``root``."""
    constitution_dir = root / ".kittify" / "constitution"
    constitution_dir.mkdir(parents=True)
    (constitution_dir / "governance.yaml").write_text(governance, encoding="utf-8")
    (constitution_dir / "agents.yaml").write_text(agents, encoding="utf-8")
    (constitution_dir / "directives.yaml").write_text(directives, encoding="utf-8")
    return constitution_dir


def _make_rich_profile(profile_id: str, role: str = "implementer") -> AgentProfile:
    """Build a minimal rich AgentProfile for use in tests."""
    return AgentProfile(
        **{
            "profile-id": profile_id,
            "name": profile_id.replace("-", " ").title(),
            "purpose": f"Testing profile {profile_id}",
            "role": role,
            "specialization": {"primary-focus": f"Focus for {profile_id}"},
        }
    )


def _build_repo_with_profiles(tmp_path: Path, profiles: list[AgentProfile]) -> AgentProfileRepository:
    """Build an AgentProfileRepository from a list of profiles, saved to tmp_path."""
    project_dir = tmp_path / "profiles"
    project_dir.mkdir()
    from ruamel.yaml import YAML

    yaml = YAML()
    yaml.default_flow_style = False

    for profile in profiles:
        yaml_file = project_dir / f"{profile.profile_id}.agent.yaml"
        data = profile.model_dump(by_alias=True, mode="json")
        with yaml_file.open("w") as f:
            yaml.dump(data, f)

    return AgentProfileRepository(shipped_dir=Path("/nonexistent"), project_dir=project_dir)


# ---------------------------------------------------------------------------
# Tests: profile_repository path
# ---------------------------------------------------------------------------


class TestResolveGovernanceWithRepository:
    """resolve_governance() with profile_repository=... (rich doctrine path)."""

    def test_repository_path_returns_rich_profiles(self, tmp_path: Path) -> None:
        """When profile_repository is supplied, agent_profiles are rich AgentProfile objects."""
        _write_constitution_files(
            tmp_path,
            governance="""
doctrine:
  selected_agent_profiles: [codex-implementer]
  available_tools: [git]
""",
        )
        codex = _make_rich_profile("codex-implementer", role="implementer")
        repo = _build_repo_with_profiles(tmp_path, [codex])

        result = resolve_governance(
            tmp_path,
            profile_repository=repo,
            tool_registry={"git"},
        )

        assert len(result.agent_profiles) == 1
        resolved = result.agent_profiles[0]
        assert isinstance(resolved, AgentProfile)
        assert resolved.profile_id == "codex-implementer"

    def test_repository_path_all_profiles_fallback(self, tmp_path: Path) -> None:
        """When no selected_agent_profiles in constitution, all repository profiles are returned."""
        _write_constitution_files(
            tmp_path,
            governance="""
doctrine:
  selected_agent_profiles: []
  available_tools: []
""",
        )
        alice = _make_rich_profile("alice", role="implementer")
        bob = _make_rich_profile("bob", role="reviewer")
        repo = _build_repo_with_profiles(tmp_path, [alice, bob])

        result = resolve_governance(
            tmp_path,
            profile_repository=repo,
            tool_registry={"git"},
        )

        returned_ids = {p.profile_id for p in result.agent_profiles}  # type: ignore[attr-defined]
        assert returned_ids == {"alice", "bob"}
        assert result.metadata["profile_source"] == "catalog_fallback"

    def test_repository_path_missing_profile_raises(self, tmp_path: Path) -> None:
        """Missing profile_id in repository causes GovernanceResolutionError."""
        _write_constitution_files(
            tmp_path,
            governance="""
doctrine:
  selected_agent_profiles: [nonexistent-profile]
""",
        )
        alice = _make_rich_profile("alice")
        repo = _build_repo_with_profiles(tmp_path, [alice])

        with pytest.raises(GovernanceResolutionError) as exc:
            resolve_governance(tmp_path, profile_repository=repo)

        assert "nonexistent-profile" in str(exc.value)

    def test_repository_metadata_source_is_constitution(self, tmp_path: Path) -> None:
        """profile_source is 'constitution' when profiles are explicitly selected."""
        _write_constitution_files(
            tmp_path,
            governance="""
doctrine:
  selected_agent_profiles: [alice]
""",
        )
        alice = _make_rich_profile("alice")
        repo = _build_repo_with_profiles(tmp_path, [alice])

        result = resolve_governance(tmp_path, profile_repository=repo, tool_registry=set())
        assert result.metadata["profile_source"] == "constitution"


# ---------------------------------------------------------------------------
# Tests: profile_catalog takes precedence over profile_repository
# ---------------------------------------------------------------------------


class TestCatalogPrecedence:
    """profile_catalog wins over profile_repository when both are supplied."""

    def test_catalog_beats_repository(self, tmp_path: Path) -> None:
        """When both profile_catalog and profile_repository are supplied, catalog wins."""
        _write_constitution_files(
            tmp_path,
            governance="""
doctrine:
  selected_agent_profiles: [catalog-profile]
  available_tools: []
""",
        )
        # Repository has a different profile
        repo_profile = _make_rich_profile("repo-profile")
        repo = _build_repo_with_profiles(tmp_path, [repo_profile])

        # Catalog has the requested profile
        catalog_profile = _make_rich_profile("catalog-profile")
        catalog = {"catalog-profile": catalog_profile}

        result = resolve_governance(
            tmp_path,
            profile_catalog=catalog,
            profile_repository=repo,
            tool_registry=set(),
        )

        assert len(result.agent_profiles) == 1
        assert result.agent_profiles[0].profile_id == "catalog-profile"  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Tests: legacy agents.yaml path still works
# ---------------------------------------------------------------------------


class TestLegacyAgentYamlPath:
    """The default path (neither profile_catalog nor profile_repository) still works."""

    def test_legacy_path_returns_agent_entries(self, tmp_path: Path) -> None:
        """Without repository/catalog, AgentEntry objects from agents.yaml are returned."""
        _write_constitution_files(
            tmp_path,
            governance="""
doctrine:
  selected_agent_profiles: [codex]
  available_tools: [git]
""",
            agents="""
profiles:
  - agent_key: codex
    role: implementer
  - agent_key: claude
    role: reviewer
selection: {}
""",
        )

        result = resolve_governance(tmp_path, tool_registry={"git"})

        assert len(result.agent_profiles) == 1
        resolved = result.agent_profiles[0]
        # Legacy path: AgentEntry has agent_key
        assert resolved.agent_key == "codex"  # type: ignore[attr-defined]

    def test_legacy_path_fallback_uses_all_entries(self, tmp_path: Path) -> None:
        """Legacy path with no selection returns all agents.yaml entries."""
        _write_constitution_files(
            tmp_path,
            governance="doctrine: {}\n",
            agents="""
profiles:
  - agent_key: codex
    role: implementer
  - agent_key: claude
    role: reviewer
selection: {}
""",
        )

        result = resolve_governance(tmp_path, tool_registry={"git"})
        keys = {p.agent_key for p in result.agent_profiles}  # type: ignore[attr-defined]
        assert keys == {"codex", "claude"}


# ---------------------------------------------------------------------------
# Tests: collect_governance_diagnostics with repository
# ---------------------------------------------------------------------------


class TestCollectDiagnosticsWithRepository:
    """collect_governance_diagnostics() forwards profile_repository."""

    def test_diagnostics_with_valid_repository(self, tmp_path: Path) -> None:
        """No errors for valid constitution + repository combination."""
        _write_constitution_files(
            tmp_path,
            governance="""
doctrine:
  selected_agent_profiles: [alice]
  available_tools: []
""",
        )
        alice = _make_rich_profile("alice")
        repo = _build_repo_with_profiles(tmp_path, [alice])

        diagnostics = collect_governance_diagnostics(tmp_path, profile_repository=repo)
        # There should be no hard-failure errors; only informational diagnostics
        assert not any("unavailable" in d for d in diagnostics)

    def test_diagnostics_reports_missing_profile(self, tmp_path: Path) -> None:
        """Missing profile via repository surfaces in diagnostics."""
        _write_constitution_files(
            tmp_path,
            governance="""
doctrine:
  selected_agent_profiles: [ghost-profile]
""",
        )
        alice = _make_rich_profile("alice")
        repo = _build_repo_with_profiles(tmp_path, [alice])

        diagnostics = collect_governance_diagnostics(tmp_path, profile_repository=repo)
        assert any("ghost-profile" in d for d in diagnostics)
