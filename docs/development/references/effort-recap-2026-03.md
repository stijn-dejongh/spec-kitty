# Development Effort Recap — 2026-03

> Historical reference. See `docs/development/architecture_recomposition_tracker.md`
> for the active recomposition tracker and current next steps.

## Purpose

This recap replaces a larger set of point-in-time development notes with a
single working summary of the effort completed on this branch through
2026-03-30. It captures the decisions, findings, and open follow-up areas that
shaped the current implementation direction.

## What the work established

### Architecture and package direction

- Doctrine asset migration is the intended direction: shipped mission assets and
  templates move out of `specify_cli` and into `doctrine`, while `specify_cli`
  remains the CLI/runtime layer.
- `kernel`, `constitution`, and `doctrine` were treated as layered packages:
  `kernel` as the zero-dependency floor, `constitution` as governance/config
  compilation, and `doctrine` as the shipped governance asset layer.
- Centralized path handling was started with `ProjectMissionPaths`, with a clear
  next step to extend the same discipline to constitution paths, `kitty-specs/`,
  and global runtime locations.
- The mission-oriented rename direction is deliberate. The product language is
  moving away from `feature` terminology for active systems.

### Runtime, template, and workflow alignment

- Template resolution needs an explicit authoritative package tier. The desired
  steady state is that package-default mission templates resolve from doctrine
  assets rather than legacy `specify_cli/missions` copies.
- `spec-kitty next` still has acknowledged mapping gaps for the `plan` and
  `documentation` missions. Those gaps were intentionally tracked rather than
  hidden.
- Quality-check and mission compatibility work focused on making command
  surfaces, workflow transitions, and runtime decisions more deterministic.

### Quality and verification findings

- Architectural review concluded the doctrine migration aligns with the target
  architecture, but the implementation-mapping docs lag the code and need
  updates.
- A broader code review found several real defects and a large backlog of type,
  complexity, and error-handling issues. The key lesson was that the branch
  carried meaningful technical debt alongside the larger structural work.
- PR #305 verification showed the targeted doctrine, kernel, CLI rename, and
  orchestrator surfaces were broadly correct, but unresolved pre-existing test
  failures still needed explicit treatment before merge.
- Mutation-testing work did not just produce findings; it also clarified a more
  selective tactic for where mutation coverage is worthwhile versus noisy.

### CI, release, and operational guardrails

- CI linting policy was intentionally moved to a cutoff-based informational mode
  for commitlint and markdownlint, while tests, typing, security, and Python
  linting remained blocking.
- Coverage reporting was expanded so SonarCloud can aggregate outputs across the
  parallel test jobs instead of only seeing a narrow subset of the suite.
- SSH deploy-key setup for the private `spec-kitty-events` dependency was
  documented as an operational requirement for CI/CD.

## Source notes absorbed into this recap

This recap folds in the substance of the following deleted development notes:

- `code-review-2026-03-25.md`
- `constitution-path-resolution-gaps.md`
- `doctrine-migration-architecture-review.md`
- `linting-cutoff-policy.md`
- `mission-next-compatibility.md`
- `model-first-schema-generation.md`
- `mutation-testing-findings.md`
- `mutation-testing-tactic.yaml`
- `pr305-review-resolution-plan.md`
- `quality_check_structure.md`
- `ssh-deploy-keys.md`
- `test-execution-report-pr305.md`
- `test-plan-pr305.md`
- `tracking/next-mission-mappings/*`

## Follow-up themes that remain active

1. Finish the path-centralization story so constitution, mission, and global
   runtime paths are resolved through typed path services instead of ad hoc
   string assembly.
2. Align the runtime resolver, shipped templates, and documentation around
   doctrine as the canonical package asset source.
3. Close the known `next`-mapping gaps for `plan` and `documentation` missions.
4. Burn down the higher-severity test, typing, and architectural drift issues
   before treating the broader branch as merge-ready.
