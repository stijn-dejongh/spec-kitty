# Contract — CI-Topology Census Structural/LOC-Ratchet Split

> Mission: `ci-hygiene-and-sonar-debt-remediation-01KWV531`
> Closes: FR-001, FR-002 | Data model: [../data-model.md §1-2](../data-model.md#1-worklistcensusentry-structural-only-post-ic-01)
> Depends on: `tests/architectural/_baselines.yaml`'s existing `BaselinesFile`
> schema (documented in
> `kitty-specs/slice-f-multi-context-extensibility-01KRX5C8/contracts/ratchet-baseline-format.md`
> — reused unchanged, not re-specified here).

## Contract

`tests/architectural/test_ci_topology_worklist.py::test_census_worklist_matches_live_derivation`
splits into two independent assertions:

### 1. Structural equality (unchanged failure semantics)

```python
structural_fields = ("dir", "cone_roots", "target_group", "target_shard")
assert [
    {k: entry[k] for k in structural_fields} for entry in census["worklist"]
] == [
    {k: entry[k] for k in structural_fields} for entry in gc.live_derived_worklist()
]
```

Fails immediately (no ratchet) on any change — this is the routing-
completeness invariant NFR-001 requires to keep working exactly as today.

### 2. LOC ratchet (new — routes through the existing shared mechanism)

Each tracked directory's live LOC is compared against its
`_baselines.yaml` entry under a new `test_ci_topology_worklist` key via the
**existing, unmodified** `test_ratchet_baselines.py` meta-test — this
mission adds entries to `_baselines.yaml`, it does not add new ratchet
*logic*.

```yaml
# tests/architectural/_baselines.yaml (new section)
test_ci_topology_worklist:
  session_presence_loc: 1229
  bulk_edit_loc: <live value at fix time>
  # ... one entry per tracked worklist directory
```

Growth above the recorded baseline fails; shrinkage warns only — identical
semantics to every other gated module in this file.

## Non-goals

- This contract does **not** change `test_census_mapped_dirs_matches_live_derivation`
  or `test_census_arch_blind_groups_matches_live_derivation` — both stay
  exact-equality, unmodified, since they assert structural/set-membership
  facts that only change on genuine routing changes (confirmed during the
  post-spec validation squad's campsite-cleaning pass).
- This contract does **not** change `_gate_coverage.py::live_derived_worklist()`'s
  routing-assignment *logic* (which dirs get which shard/group) — only how
  its LOC field is checked downstream.

## Verification

- Red-first: temporarily add ~20 lines to a tracked worklist directory with
  no other change, confirm the OLD assertion fails and the NEW split
  assertion does not fail on the structural half and correctly ratchet-fails
  or warns on the LOC half depending on direction.
- Full `tests/architectural/` suite green after the split, with the same or
  greater invariant count as before (NFR-001).
