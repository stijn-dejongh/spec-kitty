# Tracer — Tooling Friction

Mission: `mission-resolver-port-01KX1C05` · #2173 Phase-2 MissionResolver port.
Seeded at planning with **known friction to watch** (from in-lineage retrospectives). **Append every real
friction hit during implement; assess at close and file the durable ones to #2017 / the relevant epic.**

## Watch-list carried in from prior missions (single-authority-resolution-gates, read-surface-ssot, coord-primary-partition-lock)

- **F1 — Arch marker gate is vacuous under `.worktrees/`.** A green marker run inside an execution
  worktree proves nothing; verify arch gates from the **primary checkout** (NFR-002). Confirmed friction
  in the read-surface mission.
- **F2 — Draining one call-site can drop TWO counters at once** (its own allowlist entry AND a
  `primary_feature_dir_for_mission` call inside a removed cascade). Always run the FULL arch suite +
  repo-wide floor-constant grep, not a scoped `pytest -k`.
- **F3 — Floor constants are duplicated across gate files.** `CANONICALIZER_FLOOR==44` /
  `ROUTED_CANONICALIZER_FLOOR==39` are independently pinned in BOTH
  `test_resolution_authority_gates.py` and `test_coord_read_residuals_closeout.py`. A drain must update
  every twin; grep the constant name repo-wide before assuming one file owns it.
- **F4 — `kitty-specs/` tracer edits on a lane branch commit silently, then BLOCK `move-task`.** Write
  these tracer files from the **primary checkout**, not inside a lane worktree.
- **F5 — Census/allowlist entries are token-authoritative; `line:` is non-authoritative.** Pin gate
  allowlists on tokens/symbols, never line numbers (they drift on merge).
- **F6 — `spec-commit` on a protected/coord topology** materializes the coordination worktree and lands
  on the coordination branch. This mission is `topology: coord` (coordination branch
  `kitty/mission-mission-resolver-port-01KX1C05`) — expect spec/plan commits to route there.
- **F7 — CI-only shards.** Some gates (terminology, integration/git) run only in CI's
  `integration-tests-core-misc` job. Run `tests/architectural/` locally before pushing doctrine/prose
  (the #2447 doc tail touches shipped doctrine).

## Friction encountered during implement
_(append dated entries here)_
