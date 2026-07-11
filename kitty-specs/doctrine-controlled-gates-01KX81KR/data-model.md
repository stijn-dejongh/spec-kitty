# Data Model: Doctrine-Controlled Transition Gates

All models are frozen / `extra="forbid"` unless noted. Fields marked **(new schema)** land behind a versioned evolution + migration (FR-016, C-006).

## GateBinding **(new schema — on the step contract)**
The declarative unit charter activation selects.
| Field | Type | Notes |
|-------|------|-------|
| `transition` | str | the lane/action the gate fires on (e.g. `for_review`) |
| `gate_ref` | URN | `urn:gate-handler:<id>` (Path A) or `urn:asset:<id>` (Path B) |
| `mechanism` | enum `handler\|asset` | which dispatch path |
| `on_unrunnable` | enum `warn` (default) | reserved; fail-open is the only value this mission ships |
Carried on `MissionStepContractStep` and unified `MissionStep`.

## ResolvedGate (runtime, produced by the SSOT seam)
| Field | Type | Notes |
|-------|------|-------|
| `binding` | GateBinding | source binding |
| `declaring_doctrine` | str | for observability (FR-018) |
| `dispatch` | HandlerRef \| AssetRef | resolved target |
| `activation_state` | enum `active\|inactive\|refused` | why it will/won't run |

## GateVerdict (emitted by a handler/asset)
| Field | Type | Notes |
|-------|------|-------|
| `status` | enum `no_new_failures\|regression\|no_coverage\|error` | |
| `blocking` | bool | only `regression && blocking` may BLOCK (C-002) |
| `message` | str | operator-facing; MUST NOT leak internal module/paths |
| `scope_evidence` | opt str | what was checked (for observability) |

## OperatorOutcome (FR-014 — reducer output; the only thing that gates the transition)
`BLOCK` | `FAULT_WARN` | `CALM_NOTICE` | `TRUST_REFUSAL` | `PASS`. See contracts/gate-verdict-and-outcomes.md for the mapping table.

## GateHandler (Path A — shipped in spec-kitty)
| Field | Type | Notes |
|-------|------|-------|
| `id` | str | `urn:gate-handler:<id>` |
| `run(ctx) -> GateVerdict` | callable | no doctrine code; no opt-in |
| `config_keys` | list[str] | e.g. `review.fail_on_pre_review_regression`, `review.test_command` (FR-017) |

## GateAsset **(new schema — executable ASSET, Path B)**
Extends `AssetManifest` with an executable shape (keyed so non-gate assets stay inert — C-003).
| Field | Type | Notes |
|-------|------|-------|
| `id`, `mime`, `path` | (existing) | inherited from AssetManifest |
| `entrypoint` | str | module:function or script path within the asset |
| `interpreter` | enum (allowlisted) | e.g. `python`; no shell |
| `verdict_protocol` | const | must emit a GateVerdict on stdout/structured channel |

## ScopeSource (doctrine-declared strategy)
| Field | Type | Notes |
|-------|------|-------|
| `derive(changed_files) -> Scope` | callable | portable; spec-kitty's filter-group/census model is one built-in impl (FR-009) |
| built-in id | str | active only when spec-kitty's own doctrine is active (FR-012) |

## TrustEnvelope (Path-B gating; FR-007/FR-015)
| Field | Type | Notes |
|-------|------|-------|
| `provenance` | enum `built_in\|org_pack\|third_party` | **derived** from pack-load metadata, never self-declared |
| `allow_flag` | bool | `review.allow_executable_gate_assets`, default off |
| `interpreter_allowlist` | set[str] | no shell interpolation |
| `timeout_s` | int | default mirrors baseline (~300) |
| `fs_confinement` | policy | scratch/working-tree writes only |
| `network` | policy | no egress |
| `resource_limits` | policy | memory/CPU/output-size |
| `refuse_if_unconfinable` | bool=true | never run unconfined → TRUST_REFUSAL |

## Relationships
`StepContract` 1—* `GateBinding` —selected-by→ `CharterActivation` → `ResolvedGate`
→ dispatch(`GateHandler` | `GateAsset`+`TrustEnvelope`) → `GateVerdict`
→ `FR-014 reducer` → `OperatorOutcome` (the transition's only gate).
`ScopeSource` feeds a handler/asset that runs tests; absent/undeclared → `CALM_NOTICE`.
