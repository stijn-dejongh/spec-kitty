# Quickstart: Doctrine-Controlled Transition Gates

## For a doctrine/pack author — declare a gate on a transition
1. In your step contract, add a gate binding:
   ```yaml
   steps:
     - id: status_transition
       on_transition: for_review
       gate:
         ref: urn:gate-handler:pre-review-regression   # Path A (shipped handler)
         mechanism: handler
   ```
2. Activate the declaring doctrine via charter (`charter activate …`). Only
   charter-active gates fire (FR-003).
3. Cross `move-task --to for_review` — the gate runs; the operator sees a verdict
   or a calm outcome (FR-014).

## For a consumer repo — ship your OWN gate (Path B, executable)
1. Author a gate asset in your org pack:
   ```yaml
   # my-gate.asset.yaml
   id: my-regression-gate
   mime: text/x-python
   path: gates/my_regression_gate.py
   entrypoint: "my_regression_gate:run"
   interpreter: python
   ```
   The entrypoint receives a `TransitionContext` and must emit one `GateVerdict`.
2. Bind it in a step contract (`mechanism: asset`, `ref: urn:asset:my-regression-gate`) + a `ScopeSource` for your layout.
3. Enable execution (default off): set `review.allow_executable_gate_assets: true` in `.kittify/config.yaml`.
4. Charter-activate your pack. Now `for_review` runs your gate — behind the trust
   envelope (built-in/org-pack provenance, contained, timed out) — with **no
   change to spec-kitty code**.

## What a consumer with nothing declared sees
A calm, non-blocking notice: *"automated pre-review scope not configured for this
repository."* No spec-kitty-internal module names. The transition proceeds. (#2534 resolved.)

## Fail-open, always
A misconfigured/crashed/unconfinable gate never blocks a transition — only a
valid `regression(blocking)` verdict blocks. (C-002.)

## Observe what's active
```
spec-kitty agent tasks status …            # shows active gates for the transition,
                                            # their declaring doctrine, and why each ran/didn't (FR-018)
```
