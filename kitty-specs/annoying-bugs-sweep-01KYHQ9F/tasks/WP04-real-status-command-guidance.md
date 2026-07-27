---
work_package_id: WP04
title: Real status command guidance
dependencies: []
requirement_refs:
- C-003
- C-004
- FR-012
planning_base_branch: fix/annoying-bugs-sweep
merge_target_branch: fix/annoying-bugs-sweep
branch_strategy: Planning artifacts for this mission were generated on fix/annoying-bugs-sweep. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into fix/annoying-bugs-sweep unless the human explicitly redirects the landing branch.
subtasks:
- T018
- T019
- T020
- T021
- T022
phase: Phase 2 - Agent guidance
history:
- at: '2026-07-27T13:34:24Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: curator-carla
authoritative_surface: src/doctrine/styleguides/
create_intent:
- tests/architectural/test_status_command_guidance.py
execution_mode: code_change
model: gpt-5.6-terra
owned_files:
- src/doctrine/styleguides/built-in/plain-language.styleguide.yaml
- docs/api/environment-variables.md
- docs/api/upgrade-lifecycle.md
- docs/architecture/launch-readiness-future.md
- docs/guides/install-and-upgrade.md
- tests/architectural/test_status_command_guidance.py
role: curator
tags: []
tracker_refs:
- '#2983'
---

# Work Package Prompt: WP04 - Real status command guidance

## ⚡ Do This First: Load Agent Profile

Use `/ad-hoc-profile-load`, resolve `curator-carla` with
`spec-kitty agent profile show curator-carla`, and load
`spec-kitty charter context --action implement --json`.

- **Profile**: `curator-carla`
- **Role**: `curator`
- **Agent/tool**: `codex`

## Objective

Remove concrete examples of the nonexistent top-level `spec-kitty status` command from the
canonical styleguide and four scoped published documentation pages, replacing each with the real
command that matches its local intent.

## Constraints

- Do not add a top-level `status` command.
- Do not edit `docs/changelog/CHANGELOG.md` or archived `kitty-specs/**`.
- Do not blindly replace every string with `spec-kitty agent tasks status`; upgrade checks,
  environment behavior, and WP status are different domains.
- Preserve generic prose that means “a status command” rather than a literal invocation.

## Branch Strategy

- **Planning base**: `fix/annoying-bugs-sweep`
- **Merge target**: `fix/annoying-bugs-sweep`
- Execute in the workspace allocated by finalization.

## Subtasks

### T018 - Classify occurrences

For each scoped occurrence, identify the intended owning command from the live Typer tree and
`--help`. Record the classification in the test parametrization or a concise code comment where it
prevents future blind substitution.

### T019 - Correct the styleguide

Change the `good_example` to the real WP status command while preserving the plain-language lesson.
Keep the canonical source YAML valid and avoid generated copies.

### T020 - Correct published docs

Update only:

- `docs/api/environment-variables.md`
- `docs/api/upgrade-lifecycle.md`
- `docs/architecture/launch-readiness-future.md`
- `docs/guides/install-and-upgrade.md`

Use current command help as the authority. Preserve surrounding semantics, option spelling, and
environment examples.

### T021 - Regression guard

Add a non-vacuous architectural test over the exact scoped source set. It should assert each
concrete command parses against the live CLI or a canonical command inventory, not merely ban one
string. Assert the file denominator so deletion cannot green the test.

### T022 - Gates

```bash
PWHEADLESS=1 pytest tests/architectural/test_status_command_guidance.py -q
PWHEADLESS=1 pytest tests/architectural/test_docs_cli_reference_parity.py -q
PWHEADLESS=1 pytest tests/architectural/test_no_legacy_terminology.py -q
```

Validate YAML and Markdown formatting with the repository's existing focused checks.

## Definition Of Done

- Every scoped concrete example names a real, intent-correct command.
- The canonical styleguide remains valid.
- Changelog and archived mission history are untouched.
- A non-vacuous test prevents recurrence.

## Reviewer Guidance

Review each replacement in context. Reject uniform substitution, historical rewrites, or a test
that merely asserts the forbidden string disappeared without validating the replacement.

