"""Acceptance contract tests for governance mission workflow bootstrap artifacts."""

from __future__ import annotations

from pathlib import Path

from ruamel.yaml import YAML


REPO_ROOT = Path(__file__).resolve().parents[2]
DIRECTIVE_014 = REPO_ROOT / "src" / "doctrine" / "directives" / "014-work-log-creation.directive.yaml"
DIRECTIVE_015 = REPO_ROOT / "src" / "doctrine" / "directives" / "015-store-prompts.directive.yaml"
TACTIC_WORK_LOG = REPO_ROOT / "src" / "doctrine" / "tactics" / "work-log-template-usage.tactic.yaml"
TACTIC_PROMPT_DOC = (
    REPO_ROOT / "src" / "doctrine" / "tactics" / "prompt-documentation-template-usage.tactic.yaml"
)
TEMPLATE_WORK_LOG = REPO_ROOT / "src" / "doctrine" / "templates" / "generic" / "work-log-template.md"
TEMPLATE_PROMPT_DOC = (
    REPO_ROOT / "src" / "doctrine" / "templates" / "generic" / "prompt-documentation-template.md"
)
JOURNEY_005 = REPO_ROOT / "architecture" / "journeys" / "005-governance-mission-constitution-operations.md"
JOURNEYS_INDEX = REPO_ROOT / "architecture" / "journeys" / "README.md"


def _load_yaml(path: Path) -> dict:
    yaml = YAML(typ="safe")
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.load(handle) or {}
    assert isinstance(payload, dict), f"Expected mapping root in {path}"
    return payload


def test_directives_014_and_015_reference_template_backed_tactics() -> None:
    """Directives 014/015 must route through explicit template-usage tactics."""
    d014 = _load_yaml(DIRECTIVE_014)
    d015 = _load_yaml(DIRECTIVE_015)

    assert "work-log-template-usage" in (d014.get("tactic_refs") or [])
    assert "prompt-documentation-template-usage" in (d015.get("tactic_refs") or [])


def test_template_usage_tactics_point_to_local_templates() -> None:
    """Template usage tactics must mention concrete doctrine template paths."""
    tactic_014 = _load_yaml(TACTIC_WORK_LOG)
    tactic_015 = _load_yaml(TACTIC_PROMPT_DOC)

    joined_014 = "\n".join(
        str(step.get("description", "")) for step in tactic_014.get("steps", []) if isinstance(step, dict)
    )
    joined_015 = "\n".join(
        str(step.get("description", "")) for step in tactic_015.get("steps", []) if isinstance(step, dict)
    )

    assert "src/doctrine/templates/generic/work-log-template.md" in joined_014
    assert "src/doctrine/templates/generic/prompt-documentation-template.md" in joined_015

    assert TEMPLATE_WORK_LOG.exists(), f"Missing template: {TEMPLATE_WORK_LOG}"
    assert TEMPLATE_PROMPT_DOC.exists(), f"Missing template: {TEMPLATE_PROMPT_DOC}"


def test_governance_mission_journey_is_present_and_indexed() -> None:
    """A dedicated governance-mission workflow journey must exist and be indexed."""
    assert JOURNEY_005.exists(), f"Missing journey: {JOURNEY_005}"

    index_text = JOURNEYS_INDEX.read_text(encoding="utf-8")
    assert "005-governance-mission-constitution-operations.md" in index_text


def test_governance_mission_journey_covers_command_flow_and_directives() -> None:
    """Journey must describe curation + constitution review/alter command flow."""
    text = JOURNEY_005.read_text(encoding="utf-8")

    required_snippets = [
        "codex generic: kitty-aware",
        "/spec-kitty.doctrine curate",
        "spec-kitty constitution status",
        "spec-kitty constitution sync",
        "/spec-kitty.constitution",
        "Directive 011",
        "Directive 014",
        "Directive 015",
        "## Acceptance Scenarios",
    ]

    missing = [snippet for snippet in required_snippets if snippet not in text]
    assert missing == [], "Governance mission journey is missing required flow snippets:\n" + "\n".join(
        f"  - {snippet}" for snippet in missing
    )
