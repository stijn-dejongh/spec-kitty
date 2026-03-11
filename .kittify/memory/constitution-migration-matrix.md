# Constitution Migration Matrix

Initial execution output for the procedure `migrate-project-guidance-to-spec-kitty-constitution`.

Goal: achieve functional parity between the legacy project constitution and the
doctrine-backed Spec Kitty constitution flow.

## Source

- Legacy source: `.kittify/constitution/constitution.md`
- Target runtime: doctrine-backed constitution compilation and constitution context loading

## Classification Rules

- `directive`: mandatory rule, gate, or policy
- `tactic`: reusable execution method or step pattern that explains how to satisfy a directive
- `procedure`: multi-step operational workflow
- `styleguide`: conventions for code/docs/architecture
- `toolguide`: tool-specific instructions
- `paradigm`: high-level posture or architectural framing

## Initial Mapping

| Legacy Section | Functional Content | Target Doctrine Artifact(s) | Activation Path | Status |
|---|---|---|---|---|
| Developer Tooling Preferences | Prefer efficient local tools for common operations, including `rg` for search and better platform-specific defaults | `directive/efficient-local-tooling` + `toolguide/efficient-local-tooling` | software-dev defaults | shipped (`DIRECTIVE_028` + `efficient-local-tooling`) |
| Testing Requirements | pytest, mypy strict, integration + unit tests, high coverage bar | `directive/test-and-typecheck-quality-gate` + `tactic/quality-gate-verification` | software-dev defaults | shipped (`DIRECTIVE_030` + `quality-gate-verification`) |
| Performance and Scale | CLI responsiveness, dashboard scale, efficient git operations | `directive/cli-performance-and-scale-guardrails` | software-dev defaults | candidate |
| Deployment and Constraints | cross-platform support, Python baseline, Git requirement, release distribution expectation | `directive/runtime-and-distribution-constraints` | software-dev defaults | candidate |
| Private Dependency Pattern | how to update, pin, and release private `spec-kitty-events` dependency | `directive/private-dependency-governance` + `tactic/cross-repo-pin-and-verify` + `procedure/maintain-private-git-dependency` | software-dev defaults | drafted (`DIRECTIVE_032` + `cross-repo-pin-and-verify` + `maintain-private-git-dependency`) |
| CI/CD Authentication | deploy key handling for private dependency access | `procedure/private-repo-ci-authentication` | referenced from dependency-management directive | candidate |
| PyPI Release Process | vendoring / release workflow around private dependency | `tactic/vendor-private-runtime-for-release` + `procedure/release-with-private-runtime-dependency` | referenced from dependency-management directive | candidate |
| Testing Integration Changes | two-repo branch choreography and pinning discipline | `tactic/cross-repo-pin-and-verify` + `procedure/test-cross-repo-integration-change` | referenced from dependency-management directive | drafted (first tactic drafted) |
| Architecture: Private Dependency Pattern | private dependency model is an architectural rule, not advice | `directive/private-dependency-governance` | software-dev defaults | candidate |
| 1.x vs 2.x Branch Strategy | feature work targets 2.x; 1.x is maintenance only | `directive/deferred-migration-policy` | software-dev defaults | candidate |
| Pull Request Requirements | approval and CI requirements before merge | `directive/pull-request-quality-gate` + `tactic/pre-merge-verification` | software-dev defaults | candidate |
| Code Review Checklist | review expectations for tests, types, docs, security | `tactic/review-checklist-execution` + `styleguide/review-checklist` | referenced from pull-request-quality-gate directive | candidate |
| LLM/Agent Git Commits | agents must use unsigned commits | `directive/agent-commit-signing-policy` + `toolguide/git-agent-commit-signing` | software-dev defaults | shipped (`DIRECTIVE_029` + `git-agent-commit-signing`) |
| Documentation Standards | help text, public API docs, migration docs, ADR capture | `directive/documentation-maintenance-requirement` + `tactic/docs-sync-check` + `styleguide/documentation-maintenance` | software-dev defaults | drafted (`DIRECTIVE_033` + `docs-sync-check` + `documentation-maintenance`) |
| Governance Amendment Process | how constitutional changes are proposed and reviewed | `procedure/governance-amendment-review` | referenced from governance directive | candidate |
| Compliance Validation / Exception Handling | review responsibility and exception handling | `directive/governance-compliance-and-exceptions` | software-dev defaults | candidate |
| Attribution / License | informational metadata, not agent-execution behavior | keep outside compiled governance | n/a | intentionally out of scope |

## Immediate Curation Dependencies

Cleared in this pass:

- `DIRECTIVE_003` Decision Documentation Requirement
- `DIRECTIVE_010` Specification Fidelity Requirement
- `DIRECTIVE_018` Doctrine Versioning Requirement

## Recommended Next Extraction Order

1. Review and promote the drafted branch-strategy, private-dependency, and documentation-maintenance artifacts
2. Add `procedure/private-repo-ci-authentication`
3. Add `tactic/vendor-private-runtime-for-release`
4. Add `procedure/release-with-private-runtime-dependency`
5. Add `procedure/test-cross-repo-integration-change`
6. Add `directive/deferred-migration-policy`
7. Wire defaults/profile activation and regenerate constitution for parity checks
