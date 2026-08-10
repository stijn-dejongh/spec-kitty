# Mission Specification: Single-Authority Tracker-Egress Verdict

**Mission Branch**: `feat/egress-single-authority`
**Created**: 2026-08-10
**Status**: Draft
**Input**: Retire the tracker-egress two-authority diagnostics split (#3287); remove the redundant per-verdict consent lookup (#3291-item2).

## User Scenarios & Testing *(mandatory)*

The tracker egress gate decides whether a project's mission/engagement identifiers may leave the machine. It already **enforces** that decision from one authority (`project_egress_refusal`). But it re-derives the human-readable *reason* for a refusal — and the remedy shown to the operator — from a **second, independent** consent lookup (`egress_verdict._classify_channel1`). Two evaluations of the same consent chain can drift, and the second one repeats work (a full checkout-routing / git-identity resolution) on every gated verdict. This mission collapses the two into one.

### User Story 1 - The refusal reason comes from the deciding authority (Priority: P1)

A maintainer of the confidentiality seam wants the "why refused" and its remedy to come from the *same* evaluation that decided refuse-vs-permit, so what an operator is told can never disagree with what the gate enforced.

**Why this priority**: This is the mission's core value and its correctness guarantee — a diagnostic that can contradict enforcement is the defect #3287 names.

**Independent Test**: Compute the verdict for a project in each Channel-1 state and assert the reported `channel1_state`/remedy is derived from the enforcing resolver's return, with no second consent lookup on the path.

**Acceptance Scenarios**:

1. **Given** a project with no resolvable identity (`not_consentable`), **When** the egress verdict is computed, **Then** the reported state and remedy (run `spec-kitty init` first) are derived from the single enforcing evaluation, not a second lookup.
2. **Given** a project whose Channel 1 permits, **When** the verdict is computed, **Then** no refusal-diagnostic derivation runs and the reported state is `granted`.
3. **Given** the sync internals cannot be imported (degraded), **When** the verdict is computed, **Then** it fails closed to a refusal and never raises.

### User Story 2 - A gated sync resolves consent once (Priority: P2)

An operator running a gated tracker sync wants the gate to resolve their project's consent a single time, so the command does not spawn a second, redundant batch of git-identity subprocesses.

**Why this priority**: Removes measurable dead work (#3291-item2) — it falls out of Story 1's single-authority change, so it ships together but is not the correctness driver.

**Independent Test**: Count checkout-routing resolutions (or the git subprocesses they issue) during one gated verdict; assert exactly one, down from two.

**Acceptance Scenarios**:

1. **Given** a gated tracker sync on a hosted binding, **When** the verdict is computed, **Then** checkout routing / git identity is resolved exactly once.

### Edge Cases

- Degraded resolver (sync internals unimportable): the verdict fails closed to a refusal, reports an undetermined/no-record state, and never raises (NFR-003).
- Permitting path: the enforced permit is byte-for-byte unchanged; no diagnostic re-derivation executes.
- Hosted destination: the Channel-1 refusal message must remain byte-identical to the shipped string (NFR-002).
- Concurrent consent mutation: with one evaluation there is no window in which enforcement and the reported reason can disagree.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Decision-carrying resolver return | As the seam owner, I want the egress-consent resolver to return a value that distinguishes a grant from the three refusal states (`no_record`, `recorded_refusal`, `not_consentable`), so the verdict's Channel-1 diagnostics come from the enforcing evaluation. | High | Open |
| FR-002 | Delete the second evaluation | As the seam owner, I want `egress_verdict._classify_channel1` and its independent routing/consent resolution removed, with `channel1_state` sourced from the resolver's return. | High | Open |
| FR-003 | Preserve per-state remedies | As an operator, I want the refusal remedy for each of the three states preserved (including the `not_consentable` "run `spec-kitty init` first" remedy), now sourced from the single evaluation. | High | Open |
| FR-004 | `sync doctor` parity | As an operator, I want `spec-kitty sync doctor` to render the same per-destination refusal state and remedy, now read from the single authority. | Medium | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Enforcement unchanged | For every combination of Channel-1 state × Channel-2 value × destination, the enforced outcome (`refused` and `refusing_channels`) is identical before and after — 0 differences across the full matrix. | Security | High | Open |
| NFR-002 | Hosted byte-identity | The `HOSTED_SERVICE` Channel-1 refusal message remains byte-identical to the shipped string (FR-016 preserved) — 0-byte diff. | Compatibility | High | Open |
| NFR-003 | Never raises | The verdict never raises; on a degraded/unimportable resolver it fails closed to a refusal. | Reliability | High | Open |
| NFR-004 | One consent lookup | A gated verdict resolves checkout routing / git identity exactly once (from two), verified by a resolution/subprocess count. | Efficiency | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Seam must not widen | The contract change adds no path by which egress is permitted where it was previously refused (C-004 invariant); the change is refusal-diagnostics only. | Technical | High | Open |
| C-002 | Delete, not migrate | `_classify_channel1` and its two non-authoritativeness pins are deleted, per the module's documented retirement condition — not carried forward. | Technical | Medium | Open |
| C-003 | Re-point, don't drop, the enforcement pin | The existing `TestReportingSplitNeverFlipsEnforcement` guarantee is re-pointed to the single-authority shape, never deleted. | Technical | Medium | Open |

### Key Entities

- **Egress consent decision**: the resolver's return value — a grant, or one of the three named refusal states — replacing the current bare boolean.
- **Channel-1 state**: the reported diagnostic (`granted` / `no_record` / `recorded_refusal` / `not_consentable` / undetermined), now derived from the decision above rather than a second lookup.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Across the full matrix (3 Channel-1 states × the Channel-2 value set × 2 destinations), the enforced refuse/permit outcome and `refusing_channels` are identical before and after — 0 differences.
- **SC-002**: The `HOSTED_SERVICE` Channel-1 refusal message is byte-identical to the pre-change output (0-byte diff).
- **SC-003**: A gated tracker sync verdict performs exactly one checkout-routing resolution (down from two) — the second git-identity subprocess batch is gone.
- **SC-004**: `egress_verdict._classify_channel1` and its two non-authoritativeness pins no longer exist in the codebase, and the egress-consent boundary guards remain green.
