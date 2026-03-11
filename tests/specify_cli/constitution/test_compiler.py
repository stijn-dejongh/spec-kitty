"""Tests for constitution compiler bundle generation."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from specify_cli.constitution.compiler import compile_constitution, write_compiled_constitution
from specify_cli.constitution.interview import apply_answer_overrides, default_interview


def test_compile_constitution_contains_governance_activation_block() -> None:
    interview = default_interview(mission="software-dev", profile="minimal")

    compiled = compile_constitution(mission="software-dev", interview=interview)

    assert compiled.mission == "software-dev"
    assert compiled.template_set == "software-dev-default"
    assert "## Governance Activation" in compiled.markdown
    assert "selected_directives" in compiled.markdown
    assert len(compiled.references) >= 2


def test_compile_constitution_renders_agent_profile_metadata_when_present() -> None:
    interview = default_interview(mission="software-dev", profile="minimal")
    interview = apply_answer_overrides(interview, agent_profile="reviewer", agent_role="reviewer")

    compiled = compile_constitution(mission="software-dev", interview=interview)

    assert "agent_profile: reviewer" in compiled.markdown
    assert "agent_role: reviewer" in compiled.markdown


def test_write_compiled_constitution_writes_bundle(tmp_path: Path) -> None:
    interview = default_interview(mission="software-dev", profile="minimal")
    compiled = compile_constitution(mission="software-dev", interview=interview)

    result = write_compiled_constitution(tmp_path, compiled, force=True)

    assert "constitution.md" in result.files_written
    assert "references.yaml" in result.files_written
    assert (tmp_path / "constitution.md").exists()
    assert (tmp_path / "references.yaml").exists()

    library_files = sorted((tmp_path / "library").glob("*.md"))
    assert library_files


def test_write_compiled_constitution_requires_force_when_existing(tmp_path: Path) -> None:
    interview = default_interview(mission="software-dev", profile="minimal")
    compiled = compile_constitution(mission="software-dev", interview=interview)

    write_compiled_constitution(tmp_path, compiled, force=True)

    with pytest.raises(FileExistsError):
        write_compiled_constitution(tmp_path, compiled, force=False)


def test_compile_with_doctrine_service_none_emits_diagnostic() -> None:
    """Calling compile_constitution without DoctrineService appends the fallback diagnostic."""
    interview = default_interview(mission="software-dev", profile="minimal")

    compiled = compile_constitution(mission="software-dev", interview=interview, doctrine_service=None)

    fallback_msg = (
        "DoctrineService unavailable; using YAML scanning fallback. "
        "Profile-aware compilation requires DoctrineService."
    )
    assert any(fallback_msg in d for d in compiled.diagnostics), (
        f"Expected fallback diagnostic in {compiled.diagnostics}"
    )


def test_compile_with_doctrine_service_uses_repositories() -> None:
    """When DoctrineService is provided, its repositories are queried."""
    interview = default_interview(mission="software-dev", profile="minimal")

    # Build a minimal mock DoctrineService whose repositories return nothing
    # (empty lists / None gets), so the code paths that call .get() and
    # resolve_references_transitively() are exercised.
    mock_service = MagicMock()
    mock_service.directives.list_all.return_value = []
    mock_service.directives.get.return_value = None
    mock_service.tactics.get.return_value = None
    mock_service.styleguides.get.return_value = None
    mock_service.toolguides.get.return_value = None
    mock_service.procedures.get.return_value = None

    compiled = compile_constitution(
        mission="software-dev",
        interview=interview,
        doctrine_service=mock_service,
    )

    # The fallback diagnostic must NOT be present when service is provided
    fallback_msg = "DoctrineService unavailable"
    assert not any(fallback_msg in d for d in compiled.diagnostics), (
        f"Unexpected fallback diagnostic when DoctrineService is present: {compiled.diagnostics}"
    )
    # The compilation still succeeds and produces a valid bundle
    assert compiled.mission == "software-dev"
    assert "## Governance Activation" in compiled.markdown


def test_compile_with_doctrine_service_unresolved_refs_in_diagnostics() -> None:
    """Unresolvable references are recorded as diagnostics when DoctrineService is used."""
    # Mock service whose directives.get() always returns None → every directive
    # that the interview selects will be unresolved by the walker.
    mock_service = MagicMock()
    mock_service.directives.get.return_value = None
    mock_service.tactics.get.return_value = None
    mock_service.styleguides.get.return_value = None
    mock_service.toolguides.get.return_value = None
    mock_service.procedures.get.return_value = None

    # Force a known directive into the interview so we can assert on it
    interview_with_directive = default_interview(mission="software-dev", profile="minimal")
    object.__setattr__(interview_with_directive, "selected_directives", ["DIRECTIVE_MISSING"])

    compiled = compile_constitution(
        mission="software-dev",
        interview=interview_with_directive,
        doctrine_service=mock_service,
    )

    # At least one "Unresolved reference" diagnostic must appear
    assert any("Unresolved reference" in d for d in compiled.diagnostics), (
        f"Expected unresolved-reference diagnostic; got: {compiled.diagnostics}"
    )
