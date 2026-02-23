"""Tests for profile inheritance resolution and matching integration."""

from __future__ import annotations

from pathlib import Path

import pytest

from doctrine.agent_profiles.profile import TaskContext
from doctrine.agent_profiles.repository import AgentProfileRepository


@pytest.fixture
def inheritance_repo(tmp_path: Path) -> AgentProfileRepository:
    shipped = tmp_path / "shipped"
    shipped.mkdir()

    (shipped / "implementer.agent.yaml").write_text(
        """profile-id: implementer
name: Implementer
purpose: Build features
routing-priority: 70
specialization:
  primary-focus: implementation
specialization-context:
  languages: [python, javascript]
  frameworks: [django]
  domain-keywords: [api]
collaboration:
  handoff-to: [reviewer]
mode-defaults:
  - mode: analysis
    description: Analyze first
    use-case: plan
initialization-declaration: hello
""",
        encoding="utf-8",
    )

    (shipped / "python-pedro.agent.yaml").write_text(
        """profile-id: python-pedro
name: Python Pedro
purpose: Python specialist
specializes-from: implementer
specialization:
  primary-focus: python implementation
specialization-context:
  languages: [python]
mode-defaults:
  - mode: creative
    description: explore
    use-case: spike
""",
        encoding="utf-8",
    )

    (shipped / "backend-pedro.agent.yaml").write_text(
        """profile-id: backend-pedro
name: Backend Pedro
purpose: Backend specialist
specializes-from: python-pedro
specialization:
  primary-focus: backend apis
""",
        encoding="utf-8",
    )

    return AgentProfileRepository(shipped_dir=shipped, project_dir=None)


def test_resolve_profile_inherits_missing_fields(inheritance_repo: AgentProfileRepository) -> None:
    resolved = inheritance_repo.resolve_profile("python-pedro")

    assert resolved.collaboration.handoff_to == ["reviewer"]
    assert resolved.specialization_context is not None
    assert resolved.specialization_context.languages == ["python"]
    assert resolved.specialization_context.frameworks == ["django"]


def test_resolve_profile_supports_multi_level_chain(inheritance_repo: AgentProfileRepository) -> None:
    resolved = inheritance_repo.resolve_profile("backend-pedro")

    assert resolved.specialization.primary_focus == "backend apis"
    assert resolved.specialization_context is not None
    assert resolved.specialization_context.languages == ["python"]
    assert resolved.specialization_context.frameworks == ["django"]


def test_resolve_profile_missing_parent_warns_and_returns_child(tmp_path: Path) -> None:
    shipped = tmp_path / "shipped"
    shipped.mkdir()
    (shipped / "orphan.agent.yaml").write_text(
        """profile-id: orphan
name: Orphan
purpose: orphan
specializes-from: missing-parent
specialization:
  primary-focus: orphan
""",
        encoding="utf-8",
    )

    repo = AgentProfileRepository(shipped_dir=shipped, project_dir=None)

    with pytest.warns(UserWarning, match="missing parent"):
        resolved = repo.resolve_profile("orphan")

    assert resolved.profile_id == "orphan"
    assert resolved.specializes_from == "missing-parent"


def test_resolve_profile_cycle_raises(tmp_path: Path) -> None:
    shipped = tmp_path / "shipped"
    shipped.mkdir()
    (shipped / "a.agent.yaml").write_text(
        """profile-id: a
name: A
purpose: a
specializes-from: b
specialization:
  primary-focus: a
""",
        encoding="utf-8",
    )
    (shipped / "b.agent.yaml").write_text(
        """profile-id: b
name: B
purpose: b
specializes-from: a
specialization:
  primary-focus: b
""",
        encoding="utf-8",
    )

    repo = AgentProfileRepository(shipped_dir=shipped, project_dir=None)

    with pytest.raises(ValueError, match="Cycle detected"):
        repo.resolve_profile("a")


def test_matching_uses_resolved_profile_context(inheritance_repo: AgentProfileRepository) -> None:
    context = TaskContext(language="python", framework="django", complexity="high")
    best = inheritance_repo.find_best_match(context)

    assert best is not None
    # backend-pedro inherits django framework through the chain and has the most specific focus.
    assert best.profile_id in {"python-pedro", "backend-pedro"}
