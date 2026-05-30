# Contract: Org-Charter `extends:` Union Resolution

**Mission**: `charter-doctrine-mission-type-configuration-01KSWJVX`
**Addresses**: FR-001, FR-002, FR-003
**Status**: Proposed

---

## Resolution Model

`org-charter.yaml` supports an optional `extends: <pack-name>` key. When present, the overlay
pack is merged on top of the named base pack. Without `extends:`, all listed packs continue
to union as before (backward-compatible flat union).

| Field | Resolution rule |
|---|---|
| `required_directives` | **Union**: overlay adds; base values always preserved. Removal raises `OrgCharterExtensionError`. |
| `required_toolguides` | **Union**: same as `required_directives`. |
| `interview_defaults` | **Per-key replacement**: overlay value wins for each key; unmentioned keys inherit from base. |
| `schema_version` | Must match between base and overlay; mismatch raises a structured error with both version values. |

---

## Invariants

1. `extends:` is backward-compatible. A pack without the field behaves identically to today.
2. A base pack named in `extends:` must be present in the loaded pack set; otherwise
   `OrgCharterExtensionError` is raised with the chain that led to the failure.
3. Circular `extends:` chains raise `OrgCharterCycleError` with the full cycle path.
4. Directives and toolguides are union-only — an overlay pack can never remove a directive
   declared in a base pack (C-002).
5. `interview_defaults` keys are overwritten, not union-merged (C-002 exemption).

---

## Behavioral Contracts (Given/When/Then)

### Contract A — Union of directives across base and overlay

```
Given: base pack "corp-baseline" with
         required_directives: [SWIFT_CSP, GDPR_HANDLING]
         interview_defaults: {verbosity: concise, language: english}
         schema_version: 1
  and: overlay pack "team-alpha" with
         extends: corp-baseline
         required_directives: [DIR-035]
         interview_defaults: {verbosity: verbose}
         schema_version: 1
  and: both packs are present in the loaded pack set
When:  charter resolves the merged org-charter governance
Then:  required_directives = {SWIFT_CSP, GDPR_HANDLING, DIR-035}
       interview_defaults   = {verbosity: verbose, language: english}
       (overlay verbosity wins; language inherits from base)
```

### Contract B — Missing base pack raises OrgCharterExtensionError

```
Given: overlay pack "team-alpha" with extends: corp-baseline
  and: "corp-baseline" is NOT present in the loaded pack set
When:  charter attempts to resolve the org-charter governance
Then:  OrgCharterExtensionError is raised
       the error message includes the chain: ["team-alpha → corp-baseline"]
       no governance is applied to the session
```

### Contract C — Circular extends chain raises OrgCharterCycleError

```
Given: pack "alpha" with extends: beta
  and: pack "beta"  with extends: alpha
  and: both packs are present in the loaded pack set
When:  charter attempts to resolve the org-charter governance
Then:  OrgCharterCycleError is raised
       the error message includes the full cycle: ["alpha → beta → alpha"]
       no governance is applied to the session
```

### Contract D — No extends (flat union, backward-compatible)

```
Given: pack "corp-baseline" with required_directives: [SWIFT_CSP]
  and: pack "team-alpha"    with required_directives: [DIR-035]
  and: neither pack declares extends:
When:  charter resolves the org-charter governance
Then:  required_directives = {SWIFT_CSP, DIR-035}
       behaviour is identical to the pre-extends flat-union implementation
```

### Contract E — schema_version mismatch raises structured error

```
Given: base pack "corp-baseline"  with schema_version: 1
  and: overlay pack "team-alpha"  with schema_version: 2
         extends: corp-baseline
When:  charter attempts to resolve the org-charter governance
Then:  a structured schema-version-mismatch error is raised
       the error includes both version values: base=1, overlay=2
       no governance is applied to the session
```
