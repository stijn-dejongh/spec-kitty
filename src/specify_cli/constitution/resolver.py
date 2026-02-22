"""Constitution-centric governance resolver.

Resolves active governance from constitution selections and validates
selected references against available profile/tool catalogs.

Two profile paths are supported:

1. **Legacy / agents.yaml path** (default): ``profile_catalog`` is a
   ``dict[str, AgentEntry]`` keyed by ``agent_key``, built from the
   shallow YAML entries in ``.kittify/constitution/agents.yaml``.

2. **Rich doctrine path** (opt-in): pass ``profile_repository`` (an
   ``AgentProfileRepository``) to have ``resolve_governance`` build the
   catalog from the doctrine's rich ``AgentProfile`` objects (keyed by
   ``profile_id``).  This enables access to the full 6-section model
   (specialization, collaboration contracts, etc.) in the resolution
   result.

If both ``profile_catalog`` and ``profile_repository`` are provided,
``profile_catalog`` takes precedence so callers can fully control the
catalog without the repository being consulted.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Union

from doctrine.agent_profiles.profile import AgentProfile
from doctrine.agent_profiles.repository import AgentProfileRepository
from specify_cli.constitution.schemas import AgentEntry
from specify_cli.constitution.sync import (
    load_agents_config,
    load_directives_config,
    load_governance_config,
)

# A catalog entry can be either the legacy shallow AgentEntry (from agents.yaml)
# or the rich doctrine AgentProfile.
_AnyProfile = Union[AgentEntry, AgentProfile]

DEFAULT_TEMPLATE_SET = "software-dev-default"
DEFAULT_TOOL_REGISTRY: frozenset[str] = frozenset({"spec-kitty", "git", "python", "pytest", "ruff", "mypy", "poetry"})


class GovernanceResolutionError(ValueError):
    """Raised when constitution selections reference unavailable entities."""

    def __init__(self, issues: list[str]) -> None:
        self.issues = issues
        message = "Governance resolution failed:\n- " + "\n- ".join(issues)
        super().__init__(message)


@dataclass(frozen=True)
class GovernanceResolution:
    """Resolved governance activation result.

    ``agent_profiles`` holds whatever profile objects were present in the
    resolved catalog – either ``AgentEntry`` (legacy / agents.yaml path) or
    the rich ``AgentProfile`` (doctrine path, when ``profile_repository`` is
    supplied to ``resolve_governance``).
    """

    paradigms: list[str]
    directives: list[str]
    agent_profiles: list[_AnyProfile]
    tools: list[str]
    template_set: str
    metadata: dict[str, str]
    diagnostics: list[str] = field(default_factory=list)


def resolve_governance(
    repo_root: Path,
    *,
    profile_catalog: dict[str, _AnyProfile] | None = None,
    profile_repository: AgentProfileRepository | None = None,
    tool_registry: set[str] | None = None,
    fallback_template_set: str = DEFAULT_TEMPLATE_SET,
) -> GovernanceResolution:
    """Resolve active governance from constitution-first selection data.

    Args:
        repo_root: Repository root directory.
        profile_catalog: Optional explicit catalog mapping profile key to
            profile object.  When provided it takes precedence over both
            ``profile_repository`` and the agents.yaml fallback.
        profile_repository: Optional ``AgentProfileRepository`` for the rich
            doctrine path.  When provided (and ``profile_catalog`` is *not*),
            the catalog is built from
            ``{p.profile_id: p for p in repository.list_all()}``.
        tool_registry: Set of available tool names.  Falls back to
            ``DEFAULT_TOOL_REGISTRY``.
        fallback_template_set: Template set name used when the constitution
            does not select one.
    """
    governance = load_governance_config(repo_root)
    agents = load_agents_config(repo_root)
    directives_cfg = load_directives_config(repo_root)
    doctrine = governance.doctrine

    if profile_catalog is not None:
        # Caller-supplied catalog wins unconditionally.
        catalog: dict[str, _AnyProfile] = profile_catalog
    elif profile_repository is not None:
        # Rich doctrine path: key by profile_id.
        catalog = {p.profile_id: p for p in profile_repository.list_all()}
    else:
        # Legacy path: shallow AgentEntry objects from agents.yaml.
        catalog = {p.agent_key: p for p in agents.profiles}
    selected_profiles = doctrine.selected_agent_profiles
    diagnostics: list[str] = []

    if selected_profiles:
        missing_profiles = sorted(profile for profile in selected_profiles if profile not in catalog)
        if missing_profiles:
            raise GovernanceResolutionError(
                [
                    "Selected agent profiles are not available: " + ", ".join(missing_profiles),
                    "Update constitution selected_agent_profiles or add matching profiles to agents.yaml.",
                ]
            )
        resolved_profiles = [catalog[profile] for profile in selected_profiles]
        profile_source = "constitution"
    else:
        resolved_profiles = list(catalog.values())
        profile_source = "catalog_fallback"
        diagnostics.append("No selected_agent_profiles provided; using full profile catalog fallback.")

    available_tools = tool_registry or set(DEFAULT_TOOL_REGISTRY)
    selected_tools = doctrine.available_tools
    if selected_tools:
        missing_tools = sorted(tool for tool in selected_tools if tool not in available_tools)
        if missing_tools:
            raise GovernanceResolutionError(
                [
                    "Constitution selected unavailable tools: " + ", ".join(missing_tools),
                    "Update constitution available_tools or register those tools in the runtime tool registry.",
                ]
            )
        resolved_tools = list(selected_tools)
        tools_source = "constitution"
    else:
        resolved_tools = sorted(available_tools)
        tools_source = "registry_fallback"
        diagnostics.append("No available_tools selection provided; using runtime tool registry fallback.")

    if doctrine.selected_directives:
        resolved_directives = list(doctrine.selected_directives)
        directives_source = "constitution"
    else:
        resolved_directives = [directive.id for directive in directives_cfg.directives]
        directives_source = "catalog_fallback"

    if doctrine.template_set:
        template_set = doctrine.template_set
        template_set_source = "constitution"
    else:
        template_set = fallback_template_set
        template_set_source = "fallback"
        diagnostics.append(f"Template set not selected in constitution; fallback '{template_set}' applied.")

    return GovernanceResolution(
        paradigms=list(doctrine.selected_paradigms),
        directives=resolved_directives,
        agent_profiles=resolved_profiles,
        tools=resolved_tools,
        template_set=template_set,
        metadata={
            "profile_source": profile_source,
            "tools_source": tools_source,
            "directives_source": directives_source,
            "template_set_source": template_set_source,
        },
        diagnostics=diagnostics,
    )


def collect_governance_diagnostics(
    repo_root: Path,
    *,
    profile_catalog: dict[str, _AnyProfile] | None = None,
    profile_repository: AgentProfileRepository | None = None,
    tool_registry: set[str] | None = None,
    fallback_template_set: str = DEFAULT_TEMPLATE_SET,
) -> list[str]:
    """Collect diagnostics for planning/runtime checks."""
    try:
        resolution = resolve_governance(
            repo_root,
            profile_catalog=profile_catalog,
            profile_repository=profile_repository,
            tool_registry=tool_registry,
            fallback_template_set=fallback_template_set,
        )
    except GovernanceResolutionError as exc:
        return exc.issues
    return resolution.diagnostics
