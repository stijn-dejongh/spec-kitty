# Initiative: 2026-03 Doctrine-to-Execution Integration

This initiative captures the assessment and roadmap for wiring the doctrine
repository layer (delivered in feature 046) into the constitution resolver,
mission template system, and execution dispatch chain.

## Context

Feature 046 delivered typed Pydantic models and repository services for all
6 doctrine artifact types (directives, tactics, paradigms, styleguides,
toolguides, agent profiles). These are loadable on-demand through
`DoctrineService` but are not yet consumed by the execution pipeline.

The current execution flow resolves governance through string-based lookups
in `governance.yaml` and injects constitution summaries into agent prompts.
Agents receive directive titles but not the enriched content (procedures,
tactic_refs, scope, validation_criteria) that was added in 046.

## Current Execution Flow (As-Is)

```
CLI (spec-kitty implement WP01)
  |
  v
implement.py: create worktree and context
  |
  v
prompt_builder.py: build_prompt()
  |-- Load mission config (software-dev/mission.yaml)
  |-- Load command template (software-dev/command-templates/implement.md)
  |-- Load constitution (build_constitution_context)
  |     |-- Parse constitution.md (first load only)
  |     |-- Resolve governance (directives as strings, paradigms as strings)
  |     +-- Inject summary + references into prompt
  +-- Assemble final prompt with governance context
  |
  v
Rendered markdown prompt -> Agent (12 adapter formats)
```

**Key gap**: The constitution resolver uses `governance.yaml` with string-based
directive/paradigm references. It does not call `DoctrineService` to retrieve
the full typed artifacts with procedures, tactic steps, and cross-references.

## Target Execution Flow (To-Be)

```
CLI (spec-kitty implement WP01)
  |
  v
implement.py: create worktree and context
  |
  v
prompt_builder.py: build_prompt()
  |-- Load mission template (via MissionTemplateRepository)
  |-- Load command template (doctrine artifact, not inline markdown)
  |-- Load constitution
  |     |-- Resolve governance via DoctrineService
  |     |-- DoctrineService.directives.get(id) -> full Directive with procedures
  |     |-- Resolve tactic_refs -> full Tactic objects with steps
  |     +-- Inject enriched, actionable governance into prompt
  +-- Assemble prompt with on-demand depth loading
  |
  v
Connector interface contract -> Agent adapter (pluggable)
```

## Implementation Status

| Phase | Status | Feature |
|-------|--------|---------|
| Phase 1: Constitution Resolver + Mission Template Extraction | ✅ Complete (2026-03-10) | `054-constitution-interview-compiler-and-bootstrap` |
| Phase 2: Connector Interface Contract | Planned | TBD |
| Phase 3: Event Store Interface Abstraction | Deferred | TBD |

---


## Roadmap: Three Phases

### Phase 1: Constitution Resolver + Mission Template Extraction (single mission)

**Goal**: Wire `DoctrineService` into the constitution resolver and extract
inline mission governance into proper doctrine artifacts.

**Scope**:

1. Replace string-based directive lookups in `constitution/resolver.py` with
   `DoctrineService.directives.get(id)` calls. Inject full directive content
   (intent, procedures, tactic_refs, scope) into agent prompts.

2. Resolve `tactic_refs` transitively: when a directive references tactics,
   load the full `Tactic` objects with steps and inject them as actionable
   procedure guidance.

3. Extract inline governance from `software-dev/mission.yaml` and command
   templates into doctrine artifacts. Each workflow phase becomes a
   shipped directive or tactic. The `mission.yaml` references artifact IDs
   rather than inlining content.

4. Create `MissionTemplateRepository` (schema already exists at
   `src/doctrine/schemas/mission.schema.yaml`) following the established
   repository pattern.

**Entry point**: `src/specify_cli/constitution/resolver.py` (~50 lines),
`src/specify_cli/next/prompt_builder.py`.

6. Deploy slimmed templates to all 48 agent copies via migration `m_2_0_2`.

**Entry point**: `src/specify_cli/constitution/context.py`, `src/specify_cli/constitution/resolver.py`.

**Note on MissionTemplateRepository**: Creation deferred to a follow-on feature.
The `src/doctrine/missions` package is used directly by `context.py` for
action guidelines in this iteration.

**Prerequisite status**: Curation cycle is ongoing. Feature 054 proceeded against
the current 046 artifacts; full curation alignment was not a hard blocker for
Phase 1 mechanics.

**Completion notes** (2026-03-10): All 12 WPs merged. Remaining deployment item:
migration `m_2_0_2` for slimmed agent templates (tracked separately).
`MissionTemplateRepository` creation deferred to follow-on work. See
`2026-03-054-postmortem/README.md` for full review.

### Phase 2: Connector Interface Contract (separate mission)

**Goal**: Formalize the boundary between Orchestration and Agent Tool
Connectors so external execution engines can be plugged in.

**Scope**:

1. Define a formal `ConnectorProtocol` (Python Protocol) that agent adapters
   must implement. Current 12 markdown template adapters become the reference
   implementation.

2. Abstract prompt dispatch from the current render-to-file approach into a
   contract: `dispatch(wp_context, governance_context) -> ExecutionResult`.

3. Create adapter implementations for at least one external tool as proof
   of concept.

**External tool mapping**:

| Tool | Fits As | Role in Architecture |
|------|---------|---------------------|
| Kestra | Orchestration engine | DAG executor for WP dependency graphs. Event-sourced. Replaces in-process WP scheduling. |
| n8n | Orchestration engine (visual) | Visual DAG executor with webhook-driven agent connector triggers. |
| PromptFlow | Agent Tool Connector | Microsoft's prompt chaining structures prompt -> agent -> result with tracing. |
| Semantic Kernel | Agent Tool Connector SDK | Programmatic adapter layer. Plugins map to governance injection point. |
| LangFlow | Agent Tool Connector (visual) | Visual prompt flow builder for doctrine-enriched prompt construction. |

**Key architectural insight**: None of these replace Kitty-core (planning,
doctrine, constitution). They replace the execution machinery. Principle 2
(implementation-agnostic boundaries) means the Orchestration container's
interface contract stays the same regardless of backend.

**Integration pattern**:

```
Kitty-core (doctrine + planning)
  |
  v  [interface contract]
Orchestration (Kestra / n8n / in-process)
  |
  v  [connector contract]
Agent adapter (PromptFlow / SK / LangFlow / markdown templates)
```

### Phase 3: Event Store Interface Abstraction

**Goal**: Formalize the Event Store container boundary so alternative backends
(database, remote service) can replace the current filesystem implementation.

**Deferred**: Lower priority than Phases 1-2. The current filesystem-based
event store (JSONL + frontmatter) works for local-first operation.

## Critical Path

```
Curation cycle (interactive review of 046 artifacts)
  |
  v
Phase 1: Constitution resolver + mission template extraction
  |
  v
Phase 2: Connector interface contract
  |
  v
Phase 3: Event store abstraction (deferred)
```

Phase 1 is complete. Phase 2 is now the critical path item.

## Curation Prerequisite

Before Phase 1, all 046 doctrine artifacts must be reviewed through an
interactive curation cycle to confirm alignment with project owner intent:

- 26 enriched directives (001-026): intent, procedures, tactic_refs, scope
- 12 shipped tactics: steps, references, operational guidance
- Paradigm extensions: opposed_by tensions, tactic_refs wiring
- 7 new directives (020-026): validate these are the right concepts to formalize

**Method**: Top-to-bottom vertical slices per directive. For each directive,
review intent -> scope -> procedures -> tactic_refs (resolve to full tactics)
-> opposed_by tensions. Confirm or adjust at each layer.

## Related Artifacts

- Feature 046 spec: `kitty-specs/046-doctrine-artifact-domain-models/spec.md`
- System Landscape: `architecture/2.x/00_landscape/README.md`
- Implementation Mapping: `architecture/2.x/04_implementation_mapping/README.md`
- Current resolver: `src/specify_cli/constitution/resolver.py`
- Current prompt builder: `src/specify_cli/next/prompt_builder.py`
- Mission schema: `src/doctrine/schemas/mission.schema.yaml`
- DoctrineService: `src/doctrine/service.py`
