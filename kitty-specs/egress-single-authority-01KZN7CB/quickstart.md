# Quickstart: Verifying Single-Authority Tracker-Egress Verdict

How to confirm the mission's success criteria. All checks are local (`pytest` / `ruff` / `mypy`); no SaaS.

## SC-001 — Enforcement unchanged (full matrix, incl. permit)

Run the enforcement-equivalence matrix over **`granted` + each precedence level (project-local / machine-index / env) + the three refusal states** × the Channel-2 value set × `LOCAL_SUBPROCESS`/`HOSTED_SERVICE`. Assert `refused` and `refusing_channels` are identical to the pre-change output for every cell, and that no previously-refused cell now permits.

```bash
PWHEADLESS=1 uv run pytest tests/sync/tracker/test_tracker_egress_verdict_3108.py -q
```

## SC-002 — Hosted byte-identity

Assert the `HOSTED_SERVICE` Channel-1 refusal message is byte-identical across `NO_RECORD` / `RECORDED_REFUSAL` / `NOT_CONSENTABLE` and to the shipped string (0-byte diff).

## SC-003 — One resolution each

With `resolve_checkout_sync_routing_readonly` and `resolve_project_consent` counted (spy/patch), assert exactly **one** call to each per gated verdict (down from two). This is also the rebuilt form of the old `TestReportingSplitNeverFlipsEnforcement` guarantee.

## SC-004 — Deletion + guards

```bash
# _classify_channel1 and its two non-authoritativeness pins are gone:
grep -rn "_classify_channel1" src/ tests/    # expect: no matches in src/
PWHEADLESS=1 uv run pytest tests/architectural/test_egress_consent_boundary.py tests/invocation/test_adapters.py -q
```

The iterate-all-members `permits_egress` guard (`test_adapters.py`) must stay green — only `GRANTED` permits.

## SC-005 — `sync doctor` parity

Assert `spec-kitty sync doctor` renders the same per-destination Channel-1 state and remedy — including the degraded states — as before the change.

## Whole-seam gates before hand-off

```bash
uv run ruff check src/specify_cli/{invocation/adapters,egress,tracker/egress_verdict}.py src/specify_cli/sync/__init__.py
uv run mypy --strict <changed src files>
PWHEADLESS=1 uv run pytest tests/sync/tracker/ tests/invocation/ tests/architectural/test_egress_consent_boundary.py -q
```
