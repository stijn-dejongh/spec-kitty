# Curation Backlog

Artifacts intentionally tracked for doctrine curation follow-up.

## Current Backlog

- `directive/DIRECTIVE_032`
  - Status: drafted
  - Reason: needed to preserve deterministic private dependency handling, CI safety, and release portability

- `directive/DIRECTIVE_033`
  - Status: drafted
  - Reason: needed to preserve the requirement that docs, migration notes, and ADRs stay aligned with behavior

- `tactic/cross-repo-pin-and-verify`
  - Status: drafted
  - Reason: needed for the reusable cross-repo dependency update flow

- `tactic/docs-sync-check`
  - Status: drafted
  - Reason: needed to operationalize documentation-maintenance guidance

- `styleguide/documentation-maintenance`
  - Status: drafted
  - Reason: needed to preserve durable documentation update expectations and branch-aware doc scoping

- `procedure/maintain-private-git-dependency`
  - Status: drafted
  - Reason: needed to preserve the deterministic private dependency update and validation workflow

## Completed In This Pass

- Promoted `DIRECTIVE_003` to shipped
- Promoted `DIRECTIVE_010` to shipped
- Promoted `DIRECTIVE_018` to shipped
- Promoted `DIRECTIVE_028` to shipped
- Promoted `DIRECTIVE_029` to shipped
- Promoted `DIRECTIVE_030` to shipped
- Promoted `tactic/quality-gate-verification` to shipped
- Promoted `toolguide/efficient-local-tooling` to shipped
- Promoted `toolguide/git-agent-commit-signing` to shipped
- Verified `tests/doctrine/test_procedure_consistency.py` passes after promotion

## Next Action

Take the drafted branch-strategy, private-dependency, and documentation-maintenance artifacts through HiC review, then promote the accepted subset as the next constitution-parity batch.
