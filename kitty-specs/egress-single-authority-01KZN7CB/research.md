# Research: Single-Authority Tracker-Egress Verdict

Phase 0 output. The mission is a contained refactor on a well-understood seam, so "research" here resolves the three design decisions the post-spec squad flagged as open, each with rationale and rejected alternatives.

## Decision 1 — How the decision-carrying state reaches the verdict without a second resolution (the M2 crux)

**Decision**: Introduce a single internal decider in `egress.py` — `_egress_decision(root, identifiers) -> EgressDecision(permits: bool, refusal_message: str | None, channel1_state)` — that resolves consent **once** (`resolve_project_consent`) plus routing once, and returns both the byte-identical refusal string and the diagnostic state. `project_egress_refusal` becomes a thin wrapper returning only `refusal_message` (its existing `str | None` contract, so `saas_client/client.py` and other string consumers are untouched). `egress_verdict._resolve_channel1` calls `_egress_decision` directly and reads both `permits` and `channel1_state` from that one evaluation.

**Rationale**: Satisfies FR-002 (single authority) and NFR-004 (one resolution) simultaneously, while keeping `project_egress_refusal`'s public string contract intact for the widen SaaS transport (NFR-002 for that surface). The byte-identical string and the state come from the same `ConsentDecision`, so they can never disagree.

**Alternatives rejected**:
- *Change `project_egress_refusal`'s return type to carry both* — hits its other consumer `saas_client/client.py:171`, which wants a bare `str | None`, and would ripple the contract further than needed.
- *Have `egress_verdict` call `resolve_egress_consent` for the state and `project_egress_refusal` for the string* — resolves consent/routing **twice**, regressing NFR-004 (the mission's own second goal).

## Decision 2 — The consent authority and the degraded-state mapping

**Decision**: `resolve_project_consent` (returning `ConsentDecision{granted, level, project_uuid}`) is the single consent authority. The registered resolver in `sync/__init__.py` calls it **once** and maps to an `EgressConsent` member:
- `granted` → `GRANTED`
- not granted, `ConsentLevel.ABSENT` → `NO_RECORD`
- not granted, a recorded refusal level → `RECORDED_REFUSAL`
- routing has no `project_uuid` (no resolvable identity) → `NOT_CONSENTABLE`
- resolver not registered → `NO_RESOLVER`; any unrecognized/degraded answer → `UNANSWERABLE`
- resolver import failure (never reaches `resolve_egress_consent`) → the decider maps this to a named degraded state (**not** `undetermined`, which is reserved for `root is None`) and refuses.

**Rationale**: The enforcing path already wraps `resolve_project_consent(...).granted` via `consented_project_uuids` (level-erasing). Reading the full `ConsentDecision` once recovers the three refusal reasons *and* the grant verdict from one call, so enforcement equivalence holds by construction (`consented_project_uuids.granted == decision.granted`). Every non-`GRANTED` member answers `permits_egress is False` (C-001).

**Alternatives rejected**:
- *Keep `consented_project_uuids` for enforcement and re-derive `.level` separately* — that is the current two-authority split; it is exactly what this mission deletes.

## Decision 3 — Rebuilding the enforcement guarantee (C-003)

**Decision**: `TestReportingSplitNeverFlipsEnforcement` (which today monkeypatches `_classify_channel1` to disagree) is **rebuilt**, not re-pointed: once `_classify_channel1` is deleted there is no second authority to force into conflict. The replacement asserts the property *structurally* — exactly one `resolve_checkout_sync_routing_readonly` and one `resolve_project_consent` on the verdict path (NFR-004/SC-003) — plus the `_classify_channel1` symbol-absence pin (SC-004), plus the full enforcement-equivalence matrix (SC-001) that includes the permit row.

**Rationale**: With a single authority the divergence-injection premise is structurally impossible, so the guard must assert single-resolution rather than agreement-under-injection. The enforcement matrix (incl. permit + precedence levels) is what actually certifies C-001 now.

**Alternatives rejected**:
- *Keep the old test by leaving a vestigial classifier to monkeypatch* — violates C-002 (delete, not migrate) and re-introduces the second path.

## Open clarifications

None. Both user-facing decisions (split the enum; fresh feat branch) were resolved at specify time; the three design decisions above are engineering choices resolved here and will be re-examined by the post-plan squad.
