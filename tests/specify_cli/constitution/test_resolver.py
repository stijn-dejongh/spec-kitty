"""Tests for constitution-centric governance resolver."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from specify_cli.constitution.interview import default_interview
from specify_cli.constitution.resolver import (
    GovernanceResolutionError,
    collect_governance_diagnostics,
    resolve_governance,
    resolve_governance_for_profile,
)


def _write_constitution_files(
    root: Path,
    *,
    governance: str,
    directives: str = "directives: []\n",
) -> Path:
    constitution_dir = root / ".kittify" / "constitution"
    constitution_dir.mkdir(parents=True)
    (constitution_dir / "governance.yaml").write_text(governance, encoding="utf-8")
    (constitution_dir / "directives.yaml").write_text(directives, encoding="utf-8")
    return constitution_dir


def test_resolve_governance_reads_constitution_selections_first(tmp_path: Path) -> None:
    _write_constitution_files(
        tmp_path,
        governance="""
doctrine:
  selected_paradigms: [test-first]
  selected_directives: [TEST_FIRST]
  available_tools: [git]
  template_set: software-dev-default
""",
        directives="""
directives:
  - id: TEST_FIRST
    title: Keep tests strict
""",
    )

    result = resolve_governance(tmp_path, tool_registry={"git", "python", "pytest"})

    assert result.paradigms == ["test-first"]
    assert result.directives == ["TEST_FIRST"]
    assert result.tools == ["git"]
    assert result.template_set == "software-dev-default"
    assert result.metadata["template_set_source"] == "constitution"


def test_resolve_governance_missing_paradigm_hard_fails(tmp_path: Path) -> None:
    _write_constitution_files(
        tmp_path,
        governance="""
doctrine:
  selected_paradigms: [missing-paradigm]
""",
    )

    with pytest.raises(GovernanceResolutionError) as exc:
        resolve_governance(tmp_path)

    assert "missing-paradigm" in str(exc.value)


def test_resolve_governance_missing_directive_hard_fails(tmp_path: Path) -> None:
    _write_constitution_files(
        tmp_path,
        governance="""
doctrine:
  selected_directives: [NOT_A_DIRECTIVE]
""",
    )

    with pytest.raises(GovernanceResolutionError) as exc:
        resolve_governance(tmp_path)

    assert "NOT_A_DIRECTIVE" in str(exc.value)


def test_resolve_governance_missing_tool_hard_fails(tmp_path: Path) -> None:
    _write_constitution_files(
        tmp_path,
        governance="""
doctrine:
  available_tools: [imaginary-tool]
""",
    )

    with pytest.raises(GovernanceResolutionError) as exc:
        resolve_governance(tmp_path, tool_registry={"git", "python"})

    assert "imaginary-tool" in str(exc.value)


def test_resolve_governance_missing_template_set_hard_fails(tmp_path: Path) -> None:
    _write_constitution_files(
        tmp_path,
        governance="""
doctrine:
  template_set: missing-template-set
""",
    )

    with pytest.raises(GovernanceResolutionError) as exc:
        resolve_governance(tmp_path)

    assert "missing-template-set" in str(exc.value)


def test_resolve_governance_template_set_fallback_visible(tmp_path: Path) -> None:
    _write_constitution_files(
        tmp_path,
        governance="""
doctrine:
  available_tools: []
""",
    )

    result = resolve_governance(
        tmp_path,
        tool_registry={"git"},
        fallback_template_set="fallback-pack",
    )

    assert result.template_set == "fallback-pack"
    assert result.metadata["template_set_source"] == "fallback"
    assert any("fallback-pack" in line for line in result.diagnostics)


def test_resolver_does_not_read_mission_files(tmp_path: Path) -> None:
    _write_constitution_files(
        tmp_path,
        governance="doctrine: {}\n",
    )
    mission_file = tmp_path / "src" / "doctrine" / "missions" / "software-dev" / "mission.yaml"
    mission_file.parent.mkdir(parents=True)
    mission_file.write_text("::invalid-yaml::\n\tbad")

    result = resolve_governance(tmp_path, tool_registry={"git"})
    assert result.tools == ["git"]


def test_collect_governance_diagnostics_reports_failures(tmp_path: Path) -> None:
    _write_constitution_files(
        tmp_path,
        governance="""
doctrine:
  selected_directives: [NOT_A_DIRECTIVE]
""",
    )

    diagnostics = collect_governance_diagnostics(tmp_path)
    assert diagnostics
    assert any("NOT_A_DIRECTIVE" in line for line in diagnostics)


def test_resolve_governance_for_profile_merges_profile_directives_first() -> None:
    interview = default_interview(mission="software-dev", profile="minimal")
    interview = default_interview(mission="software-dev", profile="minimal")
    object.__setattr__(interview, "selected_directives", ["INTERVIEW_DIRECTIVE", "PROFILE_DIRECTIVE"])

    profile = SimpleNamespace(
        profile_id="reviewer",
        directive_references=[
            SimpleNamespace(code="PROFILE_DIRECTIVE"),
            SimpleNamespace(code="PROFILE_SECOND"),
        ],
    )
    doctrine_service = MagicMock()
    doctrine_service.agent_profiles.resolve_profile.return_value = profile
    doctrine_service.directives.get.side_effect = lambda artifact_id: SimpleNamespace(
        id=artifact_id,
        title=artifact_id,
        intent=f"Intent for {artifact_id}",
        tactic_refs=[],
    )
    doctrine_service.tactics.get.return_value = None
    doctrine_service.styleguides.get.return_value = None
    doctrine_service.toolguides.get.return_value = None
    doctrine_service.procedures.get.return_value = None

    resolution = resolve_governance_for_profile("reviewer", "reviewer", doctrine_service, interview)

    assert resolution.profile_id == "reviewer"
    assert resolution.role == "reviewer"
    assert resolution.directives == ["PROFILE_DIRECTIVE", "PROFILE_SECOND", "INTERVIEW_DIRECTIVE"]
    assert resolution.metadata["directives_source"] == "profile+interview"


def test_resolve_governance_for_profile_missing_profile_raises_value_error() -> None:
    interview = default_interview(mission="software-dev", profile="minimal")
    doctrine_service = MagicMock()
    doctrine_service.agent_profiles.resolve_profile.side_effect = KeyError("missing")

    with pytest.raises(ValueError) as exc:
        resolve_governance_for_profile("missing", None, doctrine_service, interview)

    assert "missing" in str(exc.value)


def test_resolve_governance_for_profile_records_unresolved_references_in_diagnostics() -> None:
    interview = default_interview(mission="software-dev", profile="minimal")
    object.__setattr__(interview, "selected_directives", [])

    profile = SimpleNamespace(
        profile_id="reviewer",
        directive_references=[SimpleNamespace(code="MISSING_DIRECTIVE")],
    )
    doctrine_service = MagicMock()
    doctrine_service.agent_profiles.resolve_profile.return_value = profile
    doctrine_service.directives.get.return_value = None
    doctrine_service.tactics.get.return_value = None
    doctrine_service.styleguides.get.return_value = None
    doctrine_service.toolguides.get.return_value = None
    doctrine_service.procedures.get.return_value = None

    resolution = resolve_governance_for_profile("reviewer", None, doctrine_service, interview)

    assert resolution.directives == ["MISSING_DIRECTIVE"]
    assert any("MISSING_DIRECTIVE" in line for line in resolution.diagnostics)
