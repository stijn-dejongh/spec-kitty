"""Interview answer model for constitution generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from ruamel.yaml import YAML

from specify_cli.constitution.catalog import DoctrineCatalog, load_doctrine_catalog
from specify_cli.constitution.resolver import DEFAULT_TOOL_REGISTRY


QUESTION_ORDER: tuple[str, ...] = (
    "project_intent",
    "languages_frameworks",
    "testing_requirements",
    "quality_gates",
    "review_policy",
    "performance_targets",
    "deployment_constraints",
    "documentation_policy",
    "risk_boundaries",
    "amendment_process",
    "exception_policy",
)

MINIMAL_QUESTION_ORDER: tuple[str, ...] = (
    "project_intent",
    "languages_frameworks",
    "testing_requirements",
    "quality_gates",
    "review_policy",
    "performance_targets",
    "deployment_constraints",
)


QUESTION_PROMPTS: dict[str, str] = {
    "project_intent": "What is the core user outcome this project optimizes for?",
    "languages_frameworks": "What languages/frameworks are expected?",
    "testing_requirements": "What testing and coverage expectations apply?",
    "quality_gates": "What quality gates must pass before merge?",
    "review_policy": "What review/approval policy should contributors follow?",
    "performance_targets": "What performance targets matter most (or N/A)?",
    "deployment_constraints": "What deployment/platform constraints apply?",
    "documentation_policy": "What documentation standards should be enforced?",
    "risk_boundaries": "What safety, privacy, or reliability boundaries are non-negotiable?",
    "amendment_process": "How should constitution changes be proposed and approved?",
    "exception_policy": "How should exceptions to the constitution be handled?",
}

_DEFAULT_MISSION_PARADIGMS: dict[str, tuple[str, ...]] = {
    "software-dev": ("domain-driven-design", "test-first"),
}

_DEFAULT_MISSION_DIRECTIVES: dict[str, tuple[str, ...]] = {
    # Prefer doctrine-backed test-first defaults for software delivery rather than
    # selecting the entire directive catalog.
    "software-dev": ("DIRECTIVE_004", "DIRECTIVE_027"),
}


_UNSET = object()


@dataclass(frozen=True)
class ConstitutionInterview:
    """Persisted interview answers used to compile constitution artifacts."""

    mission: str
    profile: str
    answers: dict[str, str]
    selected_paradigms: list[str]
    selected_directives: list[str]
    available_tools: list[str]
    agent_profile: str | None = None
    agent_role: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": "1.0.0",
            "mission": self.mission,
            "profile": self.profile,
            "answers": dict(self.answers),
            "selected_paradigms": list(self.selected_paradigms),
            "selected_directives": list(self.selected_directives),
            "available_tools": list(self.available_tools),
            "agent_profile": self.agent_profile,
            "agent_role": self.agent_role,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> ConstitutionInterview:
        mission = str(data.get("mission", "software-dev")).strip() or "software-dev"
        profile = str(data.get("profile", "minimal")).strip() or "minimal"
        raw_answers = data.get("answers")
        answers: dict[str, str]
        if isinstance(raw_answers, dict):
            answers = {str(k): str(v) for k, v in raw_answers.items()}
        else:
            answers = {}

        return cls(
            mission=mission,
            profile=profile,
            answers=answers,
            selected_paradigms=_normalize_list(data.get("selected_paradigms")),
            selected_directives=_normalize_list(data.get("selected_directives")),
            available_tools=_normalize_list(data.get("available_tools")),
            agent_profile=_normalize_optional_string(data.get("agent_profile")),
            agent_role=_normalize_optional_string(data.get("agent_role")),
        )


def default_interview(
    *,
    mission: str,
    profile: str = "minimal",
    doctrine_catalog: DoctrineCatalog | None = None,
) -> ConstitutionInterview:
    """Return deterministic default interview answers."""
    catalog = doctrine_catalog or load_doctrine_catalog()

    answers: dict[str, str] = {
        "project_intent": "Deliver predictable, testable changes with clear reviewability.",
        "languages_frameworks": "Python 3.11+, pytest, and repo-local tooling.",
        "testing_requirements": "pytest with 80%+ coverage and test-first behavior for risky changes.",
        "quality_gates": "Tests pass, lint clean, type checks pass, and no unresolved review findings.",
        "review_policy": "At least one focused reviewer approves before merge.",
        "performance_targets": "CLI operations should complete quickly (typically under 2 seconds).",
        "deployment_constraints": "Must run on macOS and Linux developer environments.",
        "documentation_policy": "Update docs whenever command behavior or workflow semantics change.",
        "risk_boundaries": "Do not relax quality/security standards without explicit maintainer approval.",
        "amendment_process": "Changes are proposed via PR and reviewed before adoption.",
        "exception_policy": "Exceptions must be documented in PR notes with scope and sunset criteria.",
    }

    if profile == "minimal":
        answers = {key: answers[key] for key in MINIMAL_QUESTION_ORDER}

    default_paradigms = _resolve_default_selection(
        mission=mission,
        configured=_DEFAULT_MISSION_PARADIGMS,
        available=catalog.paradigms,
    )
    default_directives = _resolve_default_selection(
        mission=mission,
        configured=_DEFAULT_MISSION_DIRECTIVES,
        available=catalog.directives,
    )

    return ConstitutionInterview(
        mission=mission,
        profile=profile,
        answers=answers,
        selected_paradigms=default_paradigms or sorted(catalog.paradigms),
        selected_directives=default_directives or sorted(catalog.directives),
        available_tools=sorted(DEFAULT_TOOL_REGISTRY),
    )


def read_interview_answers(path: Path) -> ConstitutionInterview | None:
    """Read interview answers from YAML, returning None when missing/invalid."""
    if not path.exists():
        return None

    yaml = YAML(typ="safe")
    try:
        data = yaml.load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return None

    if not isinstance(data, dict):
        return None

    return ConstitutionInterview.from_dict(data)


def write_interview_answers(path: Path, interview: ConstitutionInterview) -> None:
    """Persist interview answers to YAML."""
    path.parent.mkdir(parents=True, exist_ok=True)
    yaml = YAML()
    yaml.default_flow_style = False
    with path.open("w", encoding="utf-8") as handle:
        yaml.dump(interview.to_dict(), handle)


def apply_answer_overrides(
    interview: ConstitutionInterview,
    *,
    answers: dict[str, str] | None = None,
    selected_paradigms: Iterable[str] | None = None,
    selected_directives: Iterable[str] | None = None,
    available_tools: Iterable[str] | None = None,
    agent_profile: str | None | object = _UNSET,
    agent_role: str | None | object = _UNSET,
) -> ConstitutionInterview:
    """Return an updated interview with selected fields overridden."""
    merged_answers = dict(interview.answers)
    if answers:
        for key, value in answers.items():
            if value is None:
                continue
            merged_answers[str(key)] = str(value)

    return ConstitutionInterview(
        mission=interview.mission,
        profile=interview.profile,
        answers=merged_answers,
        selected_paradigms=_normalize_iterable(
            selected_paradigms,
            fallback=interview.selected_paradigms,
        ),
        selected_directives=_normalize_iterable(
            selected_directives,
            fallback=interview.selected_directives,
        ),
        available_tools=_normalize_iterable(
            available_tools,
            fallback=interview.available_tools,
        ),
        agent_profile=interview.agent_profile if agent_profile is _UNSET else _normalize_optional_string(agent_profile),
        agent_role=interview.agent_role if agent_role is _UNSET else _normalize_optional_string(agent_role),
    )


def _normalize_iterable(values: Iterable[str] | None, *, fallback: list[str]) -> list[str]:
    if values is None:
        return list(fallback)
    normalized: list[str] = []
    for value in values:
        item = str(value).strip()
        if item and item not in normalized:
            normalized.append(item)
    return normalized


def _normalize_list(raw: object) -> list[str]:
    if isinstance(raw, str):
        return _normalize_csv(raw)
    if isinstance(raw, list):
        return _normalize_iterable(raw, fallback=[])
    return []


def _normalize_csv(raw: str) -> list[str]:
    parts = [part.strip() for part in raw.split(",")]
    return [part for part in parts if part]


def _normalize_optional_string(raw: object) -> str | None:
    if raw is None:
        return None
    value = str(raw).strip()
    return value or None


def _resolve_default_selection(
    *,
    mission: str,
    configured: dict[str, tuple[str, ...]],
    available: frozenset[str],
) -> list[str]:
    selected: list[str] = []
    for candidate in configured.get(mission, ()):
        if candidate in available and candidate not in selected:
            selected.append(candidate)
    return selected
