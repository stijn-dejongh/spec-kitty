# Quickstart: verifying the role-aware review-claim gate

## The bug (before)
On the move-task path, a distinct reviewer profile claiming a WP for review is refused:
`WP already claimed for review by <implementer>`.

## Verify the fix

```bash
# Full status/guard suite (parallel; daemon tests excluded)
PWHEADLESS=1 .venv/bin/python -m pytest tests/specify_cli/status tests/status tests/unit/status \
  -p no:cacheprovider -q

# The red-first repro (move-task path) — red on pre-fix commit, green after
PWHEADLESS=1 .venv/bin/python -m pytest -k review_claim_role_aware -q

# Architectural guard (NFR-001)
PWHEADLESS=1 .venv/bin/python -m pytest tests/architectural -k frontmatter -q

# Lint / types
ruff check src/specify_cli/status src/specify_cli/coordination
```

## Manual smoke (two profiles)
1. Implement a WP as profile A → submit for review (`--to for_review`).
2. Claim it for review as profile B via `move-task WP## --to in_review --agent B` → **allowed**.
3. A second reviewer C claiming the active `in_review` → refused, message names B.
4. Same reviewer B re-claiming → allowed (idempotent).

## Acceptance mapping
- SC-001 → the `-k review_claim_role_aware` repro (move-task path, red-first).
- SC-002 → the `in_review` re-claim collision test + the added parity row.
- SC-003 → the architectural guard test.
- SC-004 → full suite green with all four wrong-model files re-pointed.
- SC-005 → the #2861 compact-actor and #2960 blank-actor/blank-annotation regressions.
