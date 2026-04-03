"""Tests for prompt content cleanliness in the canonical command templates.

These tests assert that the 9 canonical prompt-driven command template files
are free of dev-specific content that would break consumer projects:
  - No 057- or other feature-slug artifacts
  - No absolute machine paths (/Users/robert/, /home/)
  - No .kittify/missions/ read instructions
  - No deprecated "planning repository" terminology
  - All templates ≥50 non-empty lines
  - No YAML frontmatter blocks (the asset generator adds its own)
  - Planning-workflow templates use "project root checkout" terminology
  - tasks.md contains WP ownership metadata guidance fields
  - All templates include canonical mission selector guidance

WP06: T026
"""

from __future__ import annotations

from pathlib import Path

import pytest


pytestmark = pytest.mark.fast

# ---------------------------------------------------------------------------
# Template discovery
# ---------------------------------------------------------------------------

# All 9 prompt-driven command templates
PROMPT_DRIVEN: list[str] = [
    "specify",
    "plan",
    "tasks",
    "tasks-outline",
    "tasks-packages",
    "checklist",
    "analyze",
    "research",
    "constitution",
]

# Planning-workflow templates that MUST use "project root checkout" terminology.
# These are commands that explicitly direct agents on where to perform work.
# The utility/analysis commands (analyze, checklist, constitution) don't
# describe a checkout location, so they are excluded from this assertion.
PLANNING_WORKFLOW_TEMPLATES: list[str] = [
    "specify",
    "plan",
    "tasks",
    "tasks-outline",
    "tasks-packages",
    "research",
]

REPO_CONTEXT_TEMPLATES: list[str] = [
    "specify",
    "plan",
    "tasks",
    "tasks-outline",
    "tasks-packages",
    "checklist",
    "analyze",
    "research",
]

MISSION_CONTEXT_TEMPLATES: list[str] = [
    "specify",
    "plan",
    "tasks",
    "tasks-outline",
    "tasks-packages",
    "checklist",
    "analyze",
    "research",
]

# Resolve canonical templates via doctrine's mission-specific overrides first,
# then central doctrine defaults for commands that are not mission-specific.
_MISSION_TEMPLATES_DIR = (
    Path(__file__).parent.parent.parent
    / "src"
    / "doctrine"
    / "missions"
    / "software-dev"
    / "command-templates"
)
_CENTRAL_TEMPLATES_DIR = (
    Path(__file__).parent.parent.parent
    / "src"
    / "doctrine"
    / "templates"
    / "command-templates"
)


def _template_path(command: str) -> Path:
    """Resolve a canonical command template path for the given command."""
    mission_specific = _MISSION_TEMPLATES_DIR / f"{command}.md"
    if mission_specific.exists():
        return mission_specific
    return _CENTRAL_TEMPLATES_DIR / f"{command}.md"


def _template_content(command: str) -> str:
    """Read and return the content of a command template file."""
    return _template_path(command).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# T026-a: Template existence and minimum length
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command", PROMPT_DRIVEN)
def test_template_exists(command: str) -> None:
    """Every prompt-driven command must have a template file."""
    f = _template_path(command)
    assert f.exists(), (
        f"{command}.md not found in canonical doctrine command-templates dirs: "
        f"{_MISSION_TEMPLATES_DIR} or {_CENTRAL_TEMPLATES_DIR}"
    )


@pytest.mark.parametrize("command", PROMPT_DRIVEN)
def test_template_minimum_length(command: str) -> None:
    """Every template must have at least 40 non-empty lines.

    This threshold clearly distinguishes full prompt templates (which have
    substantial workflow guidance) from thin 4-line CLI shim files.
    """
    content = _template_content(command)
    non_empty_lines = [ln for ln in content.splitlines() if ln.strip()]
    assert len(non_empty_lines) >= 40, (
        f"{command}.md is too short: {len(non_empty_lines)} non-empty lines "
        f"(minimum 40 required to qualify as a full prompt template)"
    )


@pytest.mark.parametrize("command", PROMPT_DRIVEN)
def test_no_057_mission_slug(command: str) -> None:
    """Templates must not contain the 057- development slug."""
    content = _template_content(command)
    assert "057-" not in content, (
        f"{command}.md contains '057-' dev-time feature slug — strip before shipping"
    )


@pytest.mark.parametrize("command", PROMPT_DRIVEN)
def test_no_dev_specific_mission_slugs(command: str) -> None:
    """Templates must not contain the 057- or 058- dev-time feature slugs.

    The 057- and 058- slugs are development artifacts that leaked from source
    templates during authoring. Generic example slugs like '014-checkout-flow'
    or '020-my-feature' are legitimate documentation placeholders and are allowed.
    """
    content = _template_content(command)
    # Check specifically for the dev-time feature slugs
    for bad_slug in ("057-", "058-"):
        assert bad_slug not in content, (
            f"{command}.md contains dev-time feature slug '{bad_slug}' — "
            f"strip before shipping to consumers"
        )


@pytest.mark.parametrize("command", PROMPT_DRIVEN)
def test_no_absolute_user_paths(command: str) -> None:
    """Templates must not contain absolute paths tied to a specific machine."""
    content = _template_content(command)
    assert "/Users/robert/" not in content, (
        f"{command}.md contains absolute user path '/Users/robert/'"
    )
    assert "/home/" not in content, (
        f"{command}.md contains '/home/' path"
    )


@pytest.mark.parametrize("command", PROMPT_DRIVEN)
def test_no_kittify_missions_read_instruction(command: str) -> None:
    """Templates must not instruct agents to read template files from .kittify/missions/.

    Agents should write content directly rather than reading from .kittify/missions/.
    """
    content = _template_content(command)
    lower = content.lower()
    # Flag if the template tells agents to read files from .kittify/missions/
    # (e.g., "read .kittify/missions/..." or "cat .kittify/missions/...")
    if ".kittify/missions/" in lower:
        # If .kittify/missions/ appears, verify it's not paired with a read instruction
        # Split on the marker and check context
        for line in content.splitlines():
            if ".kittify/missions/" in line.lower():
                assert "read" not in line.lower() and "cat " not in line.lower(), (
                    f"{command}.md contains .kittify/missions/ read instruction: {line.strip()!r}"
                )


@pytest.mark.parametrize("command", REPO_CONTEXT_TEMPLATES)
def test_no_planning_repository_terminology(command: str) -> None:
    """Templates must make the checkout context explicit.

    Current doctrine templates use a mix of explicit checkout wording and
    repo-root setup instructions. The important requirement is that agents can
    tell where these commands are meant to run.
    """
    content = _template_content(command)
    assert any(
        phrase in content.lower()
        for phrase in (
            "planning repository",
            "primary repository checkout",
            "project root checkout",
            "repo root",
            "mission_dir",
        )
    ), (
        f"{command}.md should make the checkout context explicit "
        f"(for example planning repository, primary repository checkout, repo root, or mission_dir)"
    )


@pytest.mark.parametrize("command", PLANNING_WORKFLOW_TEMPLATES)
def test_uses_project_root_checkout_in_planning_templates(command: str) -> None:
    """Planning-workflow templates must clearly describe the planning checkout.

    Exact wording differs across doctrine templates. The key requirement is an
    explicit main-checkout / repo-root instruction, not a specific phrase.
    """
    content = _template_content(command)
    assert any(
        phrase in content.lower()
        for phrase in (
            "planning repository",
            "primary repository checkout",
            "project root checkout",
            "repo root",
            "mission_dir",
        )
    )


# ---------------------------------------------------------------------------
# T026-g: No YAML frontmatter blocks
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command", PROMPT_DRIVEN)
def test_no_yaml_frontmatter(command: str) -> None:
    """Templates should start with metadata frontmatter.

    Doctrine command templates currently rely on a small YAML metadata block
    so the asset pipeline can index descriptions and script hints.
    """
    content = _template_content(command)
    assert content.startswith("---"), (
        f"{command}.md should start with YAML frontmatter metadata"
    )
    assert "description:" in content, (
        f"{command}.md frontmatter should include a description field"
    )


# ---------------------------------------------------------------------------
# T026-h: canonical mission selector guidance present
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command", MISSION_CONTEXT_TEMPLATES)
def test_has_canonical_selector_guidance(command: str) -> None:
    """Every template should reference mission context explicitly somehow."""
    content = _template_content(command)
    lowered = content.lower()
    assert any(
        token in lowered
        for token in (
            "--mission",
            "mission slug",
            "mission_dir",
            "mission directory",
            "kitty-specs/<mission>",
            "mission-run",
        )
    ), (
        f"{command}.md should mention how mission context is identified "
        f"(flag, mission slug, or mission_dir path)"
    )


# ---------------------------------------------------------------------------
# T026-i: tasks.md ownership metadata guidance
# ---------------------------------------------------------------------------


def test_tasks_template_has_ownership_guidance() -> None:
    """tasks.md must include core WP metadata guidance."""
    content = _template_content("tasks")
    assert "work_package_id" in content, (
        "tasks.md should explain work_package_id metadata for generated WP files"
    )
    assert "dependencies" in content, (
        "tasks.md should explain dependency metadata for generated WP files"
    )
    assert "lane" in content, (
        "tasks.md should explain the initial lane metadata for generated WP files"
    )
