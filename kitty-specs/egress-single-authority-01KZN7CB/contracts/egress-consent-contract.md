# Contract: Egress-Consent Decision Surfaces

No HTTP/REST surface — these are the internal Python contracts the mission changes. Each row is a behavioural contract a test pins.

## 1. Registered resolver (`sync/__init__.py`)

- **Before**: `Callable[[Path], bool]` — returns grant/deny only.
- **After**: returns a decision-carrying value the port maps to an `EgressConsent` member, computed from **one** `resolve_project_consent` + one routing resolution.
- **Contract**: given a project state, returns the member per the [data-model](../data-model.md) mapping; never raises; a missing resolver ⇒ `NO_RESOLVER`.

## 2. `resolve_egress_consent` (`invocation/adapters.py`)

- **Contract**: maps the resolver's return to `EgressConsent`. **Only a recognized grant permits**; a bare `bool`, `None`, or any unrecognized value ⇒ a refusing member (`UNANSWERABLE`), **never** a permit and **never** a raise. A raw non-`EgressConsent` value must never reach a `permits_egress` call.
- **Pinned by**: re-pointed `test_resolve_egress_consent_*` (incl. the `None`/stale-answer refusal) + the iterate-all-members `permits_egress` guard.

## 3. `_egress_decision` + `project_egress_refusal` (`egress.py`)

- `_egress_decision(root, identifiers) -> EgressDecision(permits, refusal_message, channel1_state)` — **one** consent+routing resolution; returns the byte-identical refusal string and the diagnostic state together.
- `project_egress_refusal(root, identifiers) -> str | None` — thin wrapper = `_egress_decision(...).refusal_message`. **Unchanged public contract**; its consumers (`saas_client/client.py`, others) see no difference.
- `_refusal_for_verdict` — the `DENIED` branch re-pointed so `NO_RECORD` / `RECORDED_REFUSAL` / `NOT_CONSENTABLE` all render `_DENIED_TEMPLATE` (no fall-through to `_UNRECOGNISED_VERDICT_TEMPLATE`).
- **Contract**: the HOSTED_SERVICE refusal string is byte-identical across all three refusal members (NFR-002).

## 4. `egress_verdict._resolve_channel1` (`tracker/egress_verdict.py`)

- **After**: consumes `_egress_decision`'s `(permits, refusal_message, channel1_state)`. `_classify_channel1` and its independent routing/consent resolution are **deleted**.
- **Contract**: `refused` / `refusing_channels` are computed exactly as before from `permits`; `channel1_state` comes from the same decision; the verdict resolves consent/routing exactly once (NFR-004).

## Consumers verified unaffected (FR-004)

- `propagator.py` — reads `permits_egress` only; a refusing member behaves as `DENIED` did. Must remain raise-free (NFR-003).
- `saas_client/client.py` — consumes `project_egress_refusal`'s `str | None`; unchanged.
