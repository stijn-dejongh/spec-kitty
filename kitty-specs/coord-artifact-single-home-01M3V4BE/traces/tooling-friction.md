# Tooling friction: coord-artifact-single-home-01M3V4BE

Running log of tooling friction. One entry per event, 1-3 sentences, dated when it happens.

## Initial context

This Mission works on the coordination write path: `spec-kitty agent mission create`, the status and decision writers, the commit router (`coordination/commit_router.py`), `accept`, `finalize-tasks`, `spec-commit`, `doctor decisions`, `doctor coordination` and `decision verify`. Expect friction around the read-side EMPTY fallback, which masks where a write really lands, and around receipts that name the wrong branch.

## Entries

- 2026-10-01: `spec-kitty charter context` writes its encoding-provenance log to a CWD-relative `.kittify/encoding-provenance/global.jsonl` (`src/charter/activation/_io.py:286`); a squad delegate run from the mission dir left a stray `kitty-specs/<m>/.kittify/` — removed by hand.
- 2026-10-01: PR #5495 merged mid-triage and closed #5479–#5483; triage edited closed issues — re-verify issue state before writes.
- 2026-10-01: `spec-kitty charter context --action plan --json` run from `/tmp` fails with "Unable to locate repository root"; it must run from the repository root checkout (which then writes the provenance log there, where it is gitignored).
- 2026-10-01: NFR-001 bench script first ran with `./bench.sh $cfg` in zsh; zsh does not word-split an unquoted variable, so `$2` was unbound. Pass arguments explicitly.
- 2026-10-01: the installed `spec-kitty` is an editable install of a sibling checkout (`fork/spec-kitty`, at `ecb5dd914a`), not this repository; its `--json` output reports `spec_kitty_version: 4.0.0rc3` while `--version` prints `4.0.0rc5`.
