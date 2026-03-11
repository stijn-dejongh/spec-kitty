"""Transitive reference resolver for doctrine governance artifacts.

Follows directive → tactic → styleguide/toolguide/procedure chains using
depth-first traversal. Detects and breaks cycles without infinite loops.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol, cast

if TYPE_CHECKING:
    from doctrine.service import DoctrineService
    from doctrine.directives.models import Directive
    from doctrine.procedures.models import Procedure
    from doctrine.styleguides.models import Styleguide
    from doctrine.tactics.models import Tactic
    from doctrine.toolguides.models import Toolguide


class _GetterRepository(Protocol):
    def get(self, artifact_id: str) -> object | None: ...

@dataclass
class ResolvedReferenceGraph:
    """Transitive closure of governance artifacts from a set of starting directives."""

    directives: list[str] = field(default_factory=list)
    tactics: list[str] = field(default_factory=list)
    styleguides: list[str] = field(default_factory=list)
    toolguides: list[str] = field(default_factory=list)
    procedures: list[str] = field(default_factory=list)
    unresolved: list[tuple[str, str]] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        """True when all referenced artifacts were resolved."""
        return len(self.unresolved) == 0


# Maps ReferenceType string values to artifact_type keys used in traversal.
_REF_TYPE_MAP: dict[str, str] = {
    "styleguide": "styleguides",
    "toolguide": "toolguides",
    "procedure": "procedures",
    "tactic": "tactics",
    "directive": "directives",
}


class _Walker:
    """Stateful DFS walker for building a ResolvedReferenceGraph."""

    def __init__(self, doctrine_service: DoctrineService) -> None:
        self._svc = doctrine_service
        self._visited: set[tuple[str, str]] = set()
        self.graph = ResolvedReferenceGraph()

    def walk(self, artifact_type: str, artifact_id: str) -> None:
        """Walk one artifact, following its references recursively."""
        key = (artifact_type, artifact_id)
        if key in self._visited:
            return
        self._visited.add(key)

        handler = getattr(self, f"_handle_{artifact_type}", None)
        if handler is not None:
            handler(artifact_id)

    def walk_ref(self, ref_type: str, ref_id: str) -> None:
        """Resolve a ReferenceType string to an artifact_type and walk it."""
        mapped = _REF_TYPE_MAP.get(ref_type)
        if mapped is not None:
            self.walk(mapped, ref_id)

    # ------------------------------------------------------------------
    # Per-artifact-type handlers
    # ------------------------------------------------------------------

    def _handle_directives(self, artifact_id: str) -> None:
        directive = cast("Directive | None", _safe_get(self._svc.directives, artifact_id))
        if directive is None:
            self.graph.unresolved.append(("directives", artifact_id))
            return
        self.graph.directives.append(artifact_id)
        for tactic_id in (directive.tactic_refs or []):
            self.walk("tactics", tactic_id)

    def _handle_tactics(self, artifact_id: str) -> None:
        tactic = cast("Tactic | None", _safe_get(self._svc.tactics, artifact_id))
        if tactic is None:
            self.graph.unresolved.append(("tactics", artifact_id))
            return
        self.graph.tactics.append(artifact_id)
        for ref in (tactic.references or []):
            self.walk_ref(str(ref.type), ref.id)
        for step in (tactic.steps or []):
            for ref in (step.references or []):
                self.walk_ref(str(ref.type), ref.id)

    def _handle_styleguides(self, artifact_id: str) -> None:
        sg = cast("Styleguide | None", _safe_get(self._svc.styleguides, artifact_id))
        if sg is None:
            self.graph.unresolved.append(("styleguides", artifact_id))
            return
        self.graph.styleguides.append(artifact_id)

    def _handle_toolguides(self, artifact_id: str) -> None:
        tg = cast("Toolguide | None", _safe_get(self._svc.toolguides, artifact_id))
        if tg is None:
            self.graph.unresolved.append(("toolguides", artifact_id))
            return
        self.graph.toolguides.append(artifact_id)

    def _handle_procedures(self, artifact_id: str) -> None:
        proc = cast("Procedure | None", _safe_get(self._svc.procedures, artifact_id))
        if proc is None:
            self.graph.unresolved.append(("procedures", artifact_id))
            return
        self.graph.procedures.append(artifact_id)


def resolve_references_transitively(
    directive_ids: list[str],
    doctrine_service: DoctrineService,
) -> ResolvedReferenceGraph:
    """Resolve directive references transitively via depth-first traversal.

    Follows the chain: directive → tactics → styleguides/toolguides/procedures.
    Cycles are broken by tracking visited (type, id) pairs.
    Missing artifacts are recorded in the unresolved list without stopping traversal.

    Args:
        directive_ids: Starting directive IDs to resolve from.
        doctrine_service: Provides access to doctrine artifact repositories.

    Returns:
        ResolvedReferenceGraph with all reachable artifacts and unresolved references.
    """
    walker = _Walker(doctrine_service)
    for directive_id in directive_ids:
        walker.walk("directives", directive_id)
    return walker.graph


def _safe_get(
    repository: _GetterRepository,
    artifact_id: str,
) -> object | None:
    """Call repository.get(id) safely, returning None on any error."""
    try:
        artifact = repository.get(artifact_id)
    except Exception:  # noqa: BLE001
        return None
    return artifact


__all__ = [
    "ResolvedReferenceGraph",
    "resolve_references_transitively",
]
