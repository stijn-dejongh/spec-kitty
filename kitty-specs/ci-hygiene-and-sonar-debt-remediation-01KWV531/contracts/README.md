# Contracts — CI Hygiene & Sonar Debt Remediation

This mission has no HTTP/GraphQL API surface. "Contracts" here are the
internal interface/shape agreements each implementation concern must honor,
so WPs can be built and reviewed independently.

- [contract-path-resolution.md](contract-path-resolution.md) — IC-02's
  canonical `compat-planner.json` path-resolution helper contract.
- [census-ratchet-split.md](census-ratchet-split.md) — IC-01's structural
  vs. LOC-ratchet split contract for the CI-topology census.
- [backlog-slice-ticket.md](backlog-slice-ticket.md) — IC-07's GitHub-issue
  shape contract for every filed backlog-slice ticket.
