# Data Model: Single-Authority Tracker-Egress Verdict

No persisted data changes. This models the in-memory value objects the contract change touches.

## EgressConsent (port enum, `invocation/adapters.py`)

| Member | Meaning | `permits_egress` | Origin |
|--------|---------|:---:|--------|
| `GRANTED` | consent recorded and grants | **True** | `ConsentDecision.granted` |
| `NO_RECORD` | no consent record for the project *(new — split from `DENIED`)* | False | `ConsentLevel.ABSENT` |
| `RECORDED_REFUSAL` | a refusal is recorded *(new — split from `DENIED`)* | False | non-absent, non-granting level |
| `NOT_CONSENTABLE` | no resolvable project identity *(new — split from `DENIED`)* | False | routing has no `project_uuid` |
| `NO_RESOLVER` | no resolver registered | False | unchanged |
| `UNANSWERABLE` | resolver returned an unrecognized/malformed value | False | unchanged (fail-closed) |

**Invariant (C-001)**: exactly one member (`GRANTED`) answers `permits_egress is True`; certified by the iterate-all-members guard. No consumer grant-checks by member identity — all go through `permits_egress`.

## ConsentDecision (`sync/consent.py::resolve_project_consent` — unchanged)

The single consent authority. Fields: `granted: bool`, `level: ConsentLevel`, `project_uuid: str | None`. Both the enforced boolean (`granted`) and the diagnostic member above derive from **one** `ConsentDecision`; `consented_project_uuids` (the current level-erasing wrapper) is no longer the enforcing query.

## Channel-1 diagnostic state (`egress_verdict`)

Derived from the `EgressConsent` member via a total mapping — no second lookup:

| EgressConsent | channel1_state | Notes |
|---------------|----------------|-------|
| `GRANTED` | `granted` | permit path; no refusal-diagnostic derivation runs |
| `NO_RECORD` | `no_record` | remedy: record consent / `sync.enabled` |
| `RECORDED_REFUSAL` | `recorded_refusal` | remedy: change the recorded decision |
| `NOT_CONSENTABLE` | `not_consentable` | remedy: run `spec-kitty init` (carried-but-not-rendered at HOSTED_SERVICE — FR-005 carve-out) |
| `NO_RESOLVER` / `UNANSWERABLE` / import-failure | a **named** degraded state (distinct from `undetermined`) | refuses; never raises |
| `root is None` | `undetermined` | handled outside the classifier; reserved meaning — not reused for the degraded case |

## EgressDecision (new internal value, `egress.py`)

Returned by the single decider `_egress_decision(root, identifiers)`:

- `permits: bool` — equals `EgressConsent.permits_egress`.
- `refusal_message: str | None` — the byte-identical refusal string when refused (composed via `_render_denied_refusal` / `_DENIED_TEMPLATE`); `None` on permit.
- `channel1_state` — the diagnostic member above.

`project_egress_refusal(root, identifiers) -> str | None` becomes a thin wrapper returning `_egress_decision(...).refusal_message`.
