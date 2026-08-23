"""Org-tier governance-profile fail-loud coverage (#3629 p2, WP03 / T016).

Two tiers author governance selections; before this WP only the built-in tier
was read and guarded. An org pack carries its governance at
``<pack_root>/mission_types/<type>/governance-profile.yaml`` -- a path no
extraction pass ever read, so an org-tier ``selected_*`` typo was neither minted
into the DRG nor caught (a total no-op). This module pins the net-new behaviour:

* :func:`doctrine.drg.org_governance.collect_org_governance_scope_edges` +
  :func:`doctrine.drg.org_pack_loader.load_org_pack` mint the org-tier
  ``mission_type --scope--> <artifact>`` edges so a selection reaches the merged
  DRG (T014); and
* :func:`doctrine.drg.validator.assert_governance_scope_resolves` escalates a
  dangling governance-scope target to a ``ValueError`` naming
  ``mission_type:field=id`` *post-merge* (T015) -- while an ordinary org edge
  keeps merge's WARN semantics.

The guard is driven end-to-end (build a real built-in + org merged DRG, then call
the validator) plus in isolation against a hand-built graph. Both a fictional
selection (raises) and a valid selection (resolves, no false positive, scope edge
minted) are covered.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from doctrine.drg.merge import merge_three_layers
from doctrine.drg.models import DRGEdge, DRGGraph, DRGNode, NodeKind, Relation
from doctrine.drg.org_pack_loader import load_org_pack
from doctrine.drg.validator import (
    assert_governance_scope_resolves,
    validate_governance_scope_edges,
)

pytestmark = [pytest.mark.unit, pytest.mark.corpus]

_MISSION_TYPE = "custom-analysis"
_VALID_PROFILE = "researcher-robbie"


def _graph(*nodes: DRGNode, edges: list[DRGEdge] | None = None) -> DRGGraph:
    return DRGGraph(
        schema_version="1.0",
        generated_at="2026-08-23T00:00:00Z",
        generated_by="test_org_governance_failloud",
        nodes=list(nodes),
        edges=list(edges or []),
    )


def _built_in() -> DRGGraph:
    """A minimal built-in layer carrying the source + a resolvable target node."""
    return _graph(
        DRGNode(urn=f"mission_type:{_MISSION_TYPE}", kind=NodeKind.MISSION_TYPE),
        DRGNode(urn=f"agent_profile:{_VALID_PROFILE}", kind=NodeKind.AGENT_PROFILE),
    )


def _write_org_pack(pack_root: Path, selected_agent_profiles: list[str]) -> None:
    """Materialise an org pack whose per-type governance profile selects profiles.

    Writes the ``drg/fragment.yaml`` :func:`load_org_pack` requires plus the
    org-tier ``mission_types/<type>/governance-profile.yaml`` this WP teaches the
    loader to read.
    """
    drg_dir = pack_root / "drg"
    drg_dir.mkdir(parents=True)
    (drg_dir / "fragment.yaml").write_text("nodes: []\nedges: []\n", encoding="utf-8")

    profile_dir = pack_root / "mission_types" / _MISSION_TYPE
    profile_dir.mkdir(parents=True)
    (profile_dir / "governance-profile.yaml").write_text(
        yaml.safe_dump(
            {
                "id": _MISSION_TYPE,
                "mission_type": _MISSION_TYPE,
                "selected_agent_profiles": selected_agent_profiles,
            }
        ),
        encoding="utf-8",
    )


def _merged_with_selection(pack_root: Path, selected: list[str]) -> DRGGraph:
    _write_org_pack(pack_root, selected)
    fragment = load_org_pack("gov-pack", pack_root, 1)
    return merge_three_layers(_built_in(), [fragment], None)


# ---------------------------------------------------------------------------
# End-to-end: org pack -> load_org_pack -> merge -> validator
# ---------------------------------------------------------------------------


class TestOrgGovernanceScopeEndToEnd:
    def test_fictional_selection_fails_loud_naming_the_id(self, tmp_path: Path) -> None:
        merged = _merged_with_selection(tmp_path / "pack", ["does-not-exist"])

        with pytest.raises(
            ValueError,
            match=rf"{_MISSION_TYPE}:selected_agent_profiles=does-not-exist",
        ):
            assert_governance_scope_resolves(merged)

    def test_valid_selection_resolves_and_mints_its_scope_edge(
        self, tmp_path: Path
    ) -> None:
        merged = _merged_with_selection(tmp_path / "pack", [_VALID_PROFILE])

        # No false positive: a resolvable selection must not raise.
        assert_governance_scope_resolves(merged)

        scope_targets = {
            edge.target
            for edge in merged.edges
            if edge.source == f"mission_type:{_MISSION_TYPE}"
            and edge.relation is Relation.SCOPE
        }
        assert f"agent_profile:{_VALID_PROFILE}" in scope_targets, (
            "the org-tier governance selection must reach the merged DRG as a "
            "mission_type --scope--> edge, not be silently unread"
        )


# ---------------------------------------------------------------------------
# Validator isolation (hand-built merged graph)
# ---------------------------------------------------------------------------


class TestValidateGovernanceScopeEdges:
    def test_reports_dangling_governance_scope_target(self) -> None:
        graph = _graph(
            DRGNode(urn="mission_type:plan", kind=NodeKind.MISSION_TYPE),
            edges=[
                DRGEdge(
                    source="mission_type:plan",
                    target="tactic:phantom-tactic",
                    relation=Relation.SCOPE,
                )
            ],
        )

        assert validate_governance_scope_edges(graph) == [
            "plan:selected_tactics=phantom-tactic"
        ]

    def test_resolvable_target_is_silent(self) -> None:
        graph = _graph(
            DRGNode(urn="mission_type:plan", kind=NodeKind.MISSION_TYPE),
            DRGNode(urn="tactic:real-tactic", kind=NodeKind.TACTIC),
            edges=[
                DRGEdge(
                    source="mission_type:plan",
                    target="tactic:real-tactic",
                    relation=Relation.SCOPE,
                )
            ],
        )

        assert validate_governance_scope_edges(graph) == []

    def test_action_grain_scope_edge_is_not_a_governance_scope_edge(self) -> None:
        """An ``action:`` scoped edge keeps merge's WARN semantics, not escalation.

        Only ``mission_type --scope-->`` is the governance signature; a dangling
        action-grain scope edge must not be swept into the governance guard.
        """
        graph = _graph(
            DRGNode(urn="action:plan/discover", kind=NodeKind.ACTION),
            edges=[
                DRGEdge(
                    source="action:plan/discover",
                    target="tactic:phantom-tactic",
                    relation=Relation.SCOPE,
                )
            ],
        )

        assert validate_governance_scope_edges(graph) == []
