# Feature Specification: Mutmut Mutation Testing CI Integration

**Feature Branch**: `047-mutmut-mutation-testing-ci`
**Created**: 2026-03-01
**Status**: Draft
**Mission**: software-dev

## Overview

Introduce mutation testing to the Spec Kitty project using `mutmut`. Mutation
testing goes beyond line-coverage by verifying that the test suite actually
detects bugs — if mutating a line of production code does not cause at least
one test to fail, the test suite has a coverage gap for that line.

The feature adds mutmut to the project's test toolchain and wires it into CI as
a slow, parallel job so it does not slow down PR feedback loops.

## User Scenarios & Testing

### User Story 1 — Developer runs mutation testing locally (Priority: P1)

A developer wants to run mutation testing against a specific module to check
whether their new tests actually detect all the bugs they are fixing.

**Why this priority**: The primary value is the local developer workflow.
CI integration is secondary but exposes team-level trends.

**Independent Test**: Run `mutmut run` locally against a single module; verify
that the output shows surviving and killed mutants without any external
dependencies.

**Acceptance Scenarios**:

1. **Given** the dev dependency is installed, **When** the developer runs
   `mutmut run`, **Then** mutmut analyses `src/specify_cli/` and prints a
   summary of killed, surviving, and timeout mutants.
2. **Given** a mutant survives, **When** the developer runs `mutmut results`,
   **Then** the output identifies the exact file and line of the surviving
   mutant.

---

### User Story 2 — CI reports mutation score on every push (Priority: P2)

When a maintainer pushes to the repository (or triggers a manual dispatch), the
CI pipeline runs mutation testing in a dedicated job, produces reports, and
makes the mutation score visible without blocking the build.

**Why this priority**: Provides team-level visibility into mutation score trends
without blocking development workflow.

**Independent Test**: Push a commit; verify the `mutation-testing` CI job
appears, runs to completion, and uploads artifacts containing a mutation report.

**Acceptance Scenarios**:

1. **Given** a push event, **When** the CI pipeline runs, **Then** a
   `mutation-testing` job executes after `unit-tests` completes.
2. **Given** the `mutation-testing` job completes, **When** a maintainer views
   CI artifacts, **Then** HTML and JSON mutation reports are available under
   `out/reports/mutation/`.
3. **Given** a PR (not a push), **When** the CI pipeline runs, **Then** the
   `mutation-testing` job is skipped.

---

### User Story 3 — CI enforces a configurable mutation score floor (Priority: P3)

Once the team has established a baseline mutation score, they can raise the
floor to prevent regressions.

**Why this priority**: Foundational quality gate; initially set to 0% so it
never blocks, but the mechanism must exist for future enforcement.

**Independent Test**: Set the floor to a value above the current score; verify
the CI job exits non-zero and the error message cites the floor.

**Acceptance Scenarios**:

1. **Given** a floor of 0%, **When** any mutation score is reported, **Then**
   the job always passes.
2. **Given** a floor of 50%, **When** the mutation score is 40%, **Then** the
   job exits with a non-zero status and a descriptive error message.
3. **Given** a floor of 50%, **When** the mutation score is 55%, **Then** the
   job exits with status 0.

---

### Edge Cases

- What happens when mutmut times out on a slow test? The job should continue
  and count timed-out mutants separately, not fail the run.
- What happens when zero mutants are generated (empty source scope)? The job
  should exit 0 and emit a warning rather than divide-by-zero.
- What happens when the floor check script cannot parse the mutmut report? The
  job should fail with a clear error, not silently pass.

## Requirements

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Add mutmut dependency | As a developer, I want mutmut available as a test dependency so that I can run mutation testing locally. | High | Open |
| FR-002 | Configure mutmut scope | As a developer, I want mutmut configured to target `src/specify_cli/` with the existing pytest runner so that results are relevant and reproducible. | High | Open |
| FR-003 | Add mutation-testing CI job | As a maintainer, I want a dedicated mutation-testing CI job so that mutation scores are tracked over time. | High | Open |
| FR-004 | Trigger only on push/dispatch | As a developer, I want mutation testing to be skipped on PRs so that PR feedback loops remain fast. | High | Open |
| FR-005 | Output reports to standard location | As a maintainer, I want mutation reports written to `out/reports/mutation/` so that they are co-located with other CI quality reports. | Medium | Open |
| FR-006 | Upload reports as CI artifacts | As a maintainer, I want mutation reports uploaded as CI artifacts so that they are accessible after the job completes. | Medium | Open |
| FR-007 | Enforce configurable score floor | As a maintainer, I want a configurable mutation score floor so that the team can gradually raise the quality bar. | Medium | Open |
| FR-008 | Run after unit-tests, before SonarCloud | As a maintainer, I want mutation testing to run after unit tests succeed and feed results to SonarCloud so that the pipeline stays logically ordered. | Medium | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | No PR slowdown | Mutation testing must not add any time to PR CI runs (skipped entirely on pull_request events). | Performance | High | Open |
| NFR-002 | Reproducible local runs | Running mutmut locally produces the same configuration as CI (same source paths, same test runner). | Reliability | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | mutmut version | Must use `mutmut>=3.5.0` (3.x CLI, not 2.x). | Technical | High | Open |
| C-002 | No new test runner | Must use the existing pytest suite; no second test framework introduced. | Technical | High | Open |
| C-003 | Initial floor at 0% | The initial mutation score floor must be 0% to avoid blocking any current builds. | Business | High | Open |
| C-004 | Report path convention | Report output paths must follow the `out/reports/<category>/` convention already established in CI. | Technical | Medium | Open |

## Success Criteria

### Measurable Outcomes

- **SC-001**: Running `mutmut run` locally completes without configuration errors and produces output for `src/specify_cli/`.
- **SC-002**: A push to the repository triggers the `mutation-testing` CI job within the existing `ci-quality.yml` workflow.
- **SC-003**: HTML and JSON mutation reports appear as downloadable CI artifacts after every push run.
- **SC-004**: Setting the mutation score floor above the actual score causes the CI job to exit non-zero with a descriptive message.
- **SC-005**: PRs never trigger the mutation-testing job (verified by `if:` condition on the job).

## Assumptions

1. mutmut 3.x produces parseable output for score extraction; implementation adapts to the 3.x API if it differs from 2.x.
2. The existing pytest suite runs without external service dependencies in mutation CI runs.
3. Mutation runs may take up to 60 minutes per push; CI timeout for this job is set accordingly.
4. Excluding `tests/`, `.venv/`, and generated files from the mutation scope is a reasonable default configured in `pyproject.toml`.

## Out of Scope

- Incremental mutation testing (only mutating changed lines) — future enhancement.
- Per-file or per-module score floors — a single project-level floor is sufficient.
- Automatic floor ratcheting — the floor is manually adjusted by maintainers.
