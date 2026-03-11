"""End-to-end integration for profile-aware constitution compilation."""

from __future__ import annotations

from pathlib import Path

from ruamel.yaml import YAML

from doctrine.service import DoctrineService
from specify_cli.constitution.catalog import DoctrineCatalog
from specify_cli.constitution.compiler import compile_constitution, write_compiled_constitution
from specify_cli.constitution.interview import apply_answer_overrides, default_interview
from specify_cli.constitution.resolver import resolve_governance_for_profile


def _write_yaml(path: Path, data: dict[object, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    yaml = YAML()
    yaml.default_flow_style = False
    with path.open("w", encoding="utf-8") as handle:
        yaml.dump(data, handle)


def test_profile_aware_constitution_compilation_resolves_transitive_references(tmp_path: Path) -> None:
    shipped_root = tmp_path / "doctrine"
    output_dir = tmp_path / "repo" / ".kittify" / "constitution"

    _write_yaml(
        shipped_root / "directives" / "shipped" / "001-review.directive.yaml",
        {
            "schema_version": "1.0",
            "id": "REVIEW_FIRST",
            "title": "Review First",
            "intent": "Review code thoroughly.",
            "enforcement": "required",
            "tactic_refs": ["review-tactic"],
        },
    )
    _write_yaml(
        shipped_root / "tactics" / "shipped" / "review-tactic.tactic.yaml",
        {
            "schema_version": "1.0",
            "id": "review-tactic",
            "name": "Review Tactic",
            "purpose": "Drive review workflows.",
            "steps": [
                {
                    "title": "Review the change",
                    "description": "Inspect the implementation carefully.",
                    "references": [
                        {
                            "name": "Review Style",
                            "type": "styleguide",
                            "id": "review-style",
                            "when": "Always",
                        }
                    ],
                }
            ],
            "references": [],
        },
    )
    _write_yaml(
        shipped_root / "styleguides" / "shipped" / "review-style.styleguide.yaml",
        {
            "schema_version": "1.0",
            "id": "review-style",
            "title": "Review Style",
            "scope": "code",
            "principles": ["Be precise"],
        },
    )
    _write_yaml(
        shipped_root / "directives" / "shipped" / "002-interview.directive.yaml",
        {
            "schema_version": "1.0",
            "id": "INTERVIEW_ONLY",
            "title": "Interview Directive",
            "intent": "Interview-selected directive.",
            "enforcement": "advisory",
            "tactic_refs": [],
        },
    )
    _write_yaml(
        shipped_root / "agent_profiles" / "shipped" / "reviewer.agent.yaml",
        {
            "profile-id": "reviewer",
            "name": "Reviewer",
            "role": "reviewer",
            "purpose": "Review changes.",
            "specialization": {
                "primary-focus": "review",
                "secondary-awareness": "code quality",
                "avoidance-boundary": "implementation",
                "success-definition": "find issues before merge",
            },
            "directive-references": [
                {"code": "REVIEW_FIRST", "name": "Review First", "rationale": "Review every change."}
            ],
        },
    )
    _write_yaml(
        shipped_root / "missions" / "software-dev" / "mission.yaml",
        {
            "name": "software-dev",
            "description": "Software development mission.",
        },
    )

    doctrine_service = DoctrineService(shipped_root=shipped_root)
    doctrine_catalog = DoctrineCatalog(
        paradigms=frozenset(),
        directives=frozenset({"REVIEW_FIRST", "INTERVIEW_ONLY"}),
        template_sets=frozenset({"software-dev-default"}),
        tactics=frozenset({"review-tactic"}),
        styleguides=frozenset({"review-style"}),
        toolguides=frozenset(),
        procedures=frozenset(),
        profiles=frozenset({"reviewer"}),
    )
    interview = default_interview(mission="software-dev", profile="minimal")
    interview = apply_answer_overrides(
        interview,
        selected_paradigms=[],
        selected_directives=["INTERVIEW_ONLY"],
    )

    resolution = resolve_governance_for_profile("reviewer", "reviewer", doctrine_service, interview)
    compiled = compile_constitution(
        mission="software-dev",
        interview=apply_answer_overrides(
            interview,
            selected_directives=resolution.directives,
            agent_profile=resolution.profile_id,
            agent_role=resolution.role,
        ),
        doctrine_catalog=doctrine_catalog,
        doctrine_service=doctrine_service,
    )
    result = write_compiled_constitution(output_dir, compiled, force=True)

    assert resolution.directives == ["REVIEW_FIRST", "INTERVIEW_ONLY"]
    assert resolution.tactics == ["review-tactic"]
    assert resolution.styleguides == ["review-style"]
    assert compiled.diagnostics == []
    assert "constitution.md" in result.files_written
    assert "agent_profile: reviewer" in compiled.markdown
    assert any(ref.kind == "tactic" and ref.title == "Review Tactic" for ref in compiled.references)
    assert any(ref.kind == "styleguide" and ref.title == "Review Style" for ref in compiled.references)
