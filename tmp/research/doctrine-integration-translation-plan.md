# Translating the Doctrine Integration Proposal into Spec-Kitty Features

**Date:** 2026-02-14
**Purpose:** Map the architectural analysis from `quickstart_agent-augmented-development/work/kitty/` into actionable spec-kitty features using the native spec-driven workflow.

---

## Source Material Summary

The external analysis proposes unifying **Spec Kitty** (workflow orchestrator) with an **Agentic Doctrine** framework (behavioral governance). The key finding: the two systems are complementary -- SK manages *what* gets done; Doctrine manages *how* agents behave. Integration approach: Spec Kitty remains primary, Doctrine plugs in as optional governance.

### What the Proposal Wants to Add to Spec Kitty

| Capability | Current SK Coverage | Proposal |
|---|:---:|---|
| Governance lifecycle hooks | 0% | `GovernancePlugin` ABC with `validate_pre_{plan,implement,review,accept}()` |
| Event bridge / telemetry | ~5% | `EventBridge` ABC, JSONL append-only log, SQLite materialized views |
| Pluggable model routing | 0% | `RoutingProvider` ABC with fallback chains, cost-aware selection |
| Agent profile enrichment | Flat config keys | Bridge from flat keys to rich role/capability profiles |
| Budget enforcement | 0% | Cost tracking per agent/model, warn/block at thresholds |
| Constitution-config sync | N/A | Bidirectional sync between narrative Constitution and machine `.doctrine-config/` |
| Structured error reporting | ~5% | CI/CD error extraction for agent consumption |

### The 6 Proposed Phases

| Phase | Summary | Effort |
|---|---|---|
| 0 | Analysis (complete -- the source material itself) | Done |
| 1 | Telemetry & Observability Library | M (3-4 weeks) |
| 2 | Governance Plugin Extension | L (4-6 weeks) |
| 3 | Model Routing & Agent Bridge | L (5-6 weeks) |
| 4 | Real-Time Dashboard & Query Service | M |
| 5 | Error Reporting & CI Integration | M |
| 6 | Documentation, Migration & Release | S |

---

## Translation Strategy: Phases to Spec-Kitty Features

Each proposal phase maps to **one spec-kitty feature** (a `kitty-specs/NNN-*` directory). Each feature goes through the full spec-kitty lifecycle: `/spec-kitty.specify` -> `/spec-kitty.plan` -> `/spec-kitty.tasks` -> implement -> review -> merge.

### Recommended Feature Breakdown

The proposal's 6 phases are large. Some should be split further to keep work packages manageable (each WP should be implementable in a focused session). Here is the recommended mapping:

| SK Feature # | Name | Maps to Proposal Phase | Rationale |
|---|---|---|---|
| **040** | `event-bridge-and-telemetry-foundation` | Phase 1 (core) | EventBridge ABC + JSONL event log + event schema. This is the foundational infrastructure everything else depends on. |
| **041** | `telemetry-store-and-cost-tracking` | Phase 1 (store) | SQLite materialized views, cost tracker, query interface. Depends on 040. |
| **042** | `governance-plugin-interface` | Phase 2 (interface) | `GovernancePlugin` ABC, `ValidationResult`, lifecycle hook callsites in orchestrator. Pure interface + integration points -- no Doctrine-specific logic yet. |
| **043** | `doctrine-governance-provider` | Phase 2 (implementation) | `DoctrineGovernancePlugin` implementation: doctrine loader, precedence resolver, policy checker. Depends on 042. |
| **044** | `constitution-doctrine-config-sync` | Phase 2 (constitution) | Bidirectional sync between Constitution narrative and `.doctrine-config/` YAML. Depends on 043. |
| **045** | `routing-provider-interface` | Phase 3 (interface) | `RoutingProvider` ABC, `RoutingDecision`, `DefaultRoutingProvider` (reads existing agent config). |
| **046** | `doctrine-routing-and-agent-bridge` | Phase 3 (implementation) | `DoctrineRoutingProvider`, agent profile parser, capability-based routing. Depends on 045 + 043. |
| **047** | `cost-aware-routing-and-budget` | Phase 3 (budget) | Cost-optimized routing, budget enforcer, model catalog. Depends on 041 + 046. |
| **048** | `realtime-dashboard-extension` | Phase 4 | Extend existing dashboard with telemetry views, cost metrics, SocketIO. Depends on 041. |
| **049** | `ci-error-reporting` | Phase 5 | CI/CD error extraction, agent-friendly parsing. Depends on 040. |
| **050** | `doctrine-integration-docs-and-migration` | Phase 6 | User guides, `spec-kitty init --doctrine`, migration tooling. Depends on all above. |

### Dependency Graph

```
040 (EventBridge)
 |
 +---> 041 (Telemetry Store) ---> 047 (Budget) ---> 048 (Dashboard)
 |                                     ^
 +---> 042 (Governance Interface)      |
 |      |                              |
 |      +---> 043 (Doctrine Provider)  |
 |      |      |                       |
 |      |      +---> 044 (Constitution Sync)
 |      |                              |
 +---> 045 (Routing Interface)         |
        |                              |
        +---> 046 (Doctrine Routing) --+

 040 ---> 049 (CI Error Reporting)

 All ---> 050 (Docs & Migration)
```

### Parallelization Opportunities

These can run in parallel once their dependencies are met:

- **Wave 1:** 040 (EventBridge) -- no dependencies
- **Wave 2:** 041 (Telemetry Store) + 042 (Governance Interface) + 045 (Routing Interface) -- all depend only on 040
- **Wave 3:** 043 (Doctrine Provider) + 046 (Doctrine Routing) + 049 (CI Error Reporting)
- **Wave 4:** 044 (Constitution Sync) + 047 (Budget)
- **Wave 5:** 048 (Dashboard)
- **Wave 6:** 050 (Docs & Migration)

---

## How to Execute This Using Spec-Kitty's Native Workflow

### Step 1: Create Features in Dependency Order

For each feature, run the full planning pipeline **in main**:

```bash
# Feature 040 - EventBridge foundation
/spec-kitty.specify
# Answer discovery interview describing the EventBridge + event schema
# Input: reference the ARCHITECTURE_SPEC.md interfaces (EventBridge ABC, event dataclasses)

/spec-kitty.plan
# Technical design: where the code lives, which SK modules change

/spec-kitty.tasks
# Break into WPs: e.g., WP01=event schema, WP02=EventBridge ABC, WP03=JSONL writer, WP04=tests

spec-kitty agent feature finalize-tasks
# Validates dependencies, commits to main
```

### Step 2: Implement Work Packages

```bash
# Start WP01 (creates worktree)
spec-kitty implement WP01

# When WP01 is done, start dependent WPs
spec-kitty implement WP02 --base WP01

# Independent WPs can run in parallel
spec-kitty implement WP03 --base WP01 &
spec-kitty implement WP04 --base WP01 &
```

### Step 3: Review and Merge

```bash
spec-kitty agent workflow review WP01
spec-kitty agent workflow review WP02
# ... etc

# When all WPs pass review:
spec-kitty merge --feature 040-event-bridge-and-telemetry-foundation
```

### Step 4: Repeat for Next Feature

Move to feature 041, 042, etc. Features in the same wave can be specified in parallel.

---

## Key Decisions to Make Before Starting

### Decision 1: Scope Boundary

The proposal was written from the perspective of a *separate* Doctrine repository consuming Spec Kitty as a dependency. Since we're working *inside* the Spec Kitty fork, the approach shifts:

- **Option A (Recommended):** Build extension points directly into Spec Kitty core (GovernancePlugin, RoutingProvider, EventBridge as ABCs in `src/specify_cli/`). This is cleaner and avoids the "external plugin" indirection.
- **Option B:** Build as a separate package (`specify-cli-doctrine`) that imports from `specify_cli`. More modular but adds packaging complexity.

**Recommendation:** Option A for the interfaces (ABCs, dataclasses, hook callsites). Option B only for Doctrine-specific implementations if upstream acceptance is a concern.

### Decision 2: Where to Place New Code

Proposed layout within `src/specify_cli/`:

```
src/specify_cli/
  extensions/                 # NEW: Extension point ABCs
    governance.py             # GovernancePlugin ABC, ValidationResult
    routing.py                # RoutingProvider ABC, RoutingDecision
    events.py                 # EventBridge ABC, event dataclasses
  telemetry/                  # NEW: Telemetry implementation
    event_log.py              # JSONL writer
    event_store.py            # SQLite materialized views
    cost_tracker.py           # Cost aggregation
    query.py                  # Query API
  governance/                 # NEW: Governance implementations
    doctrine_plugin.py        # DoctrineGovernancePlugin
    precedence.py             # Precedence resolver
    loader.py                 # Doctrine artifact loader
  routing/                    # NEW: Routing implementations
    default_provider.py       # DefaultRoutingProvider
    doctrine_provider.py      # DoctrineRoutingProvider
    model_catalog.py          # Model registry
```

### Decision 3: Backward Compatibility Strategy

The proposal is clear: **Doctrine must be optional.** Implementation approach:

- All governance/routing hooks check `if plugin is not None` before calling
- Config flag: `governance: { enabled: false }` in `.kittify/config.yaml`
- CLI flag: `--skip-governance` for fast iteration
- No new mandatory dependencies

### Decision 4: Start with Which Feature?

**Recommendation:** Start with **040 (EventBridge)** because:
1. It's the foundation everything else builds on
2. It's relatively self-contained (ABCs + JSONL writer)
3. It doesn't require Doctrine artifacts to exist
4. It provides immediate value (event logging for existing lane transitions)

---

## Mapping Source Material to Spec Inputs

When running `/spec-kitty.specify` for each feature, use the following source documents as input to the discovery interview:

| Feature | Primary Source | Key Sections |
|---|---|---|
| 040 | `ARCHITECTURE_SPEC.md` | EventBridge Interface (Section 3), Event dataclasses |
| 041 | `EXECUTION_ROADMAP.md` | Phase 1 deliverables (TelemetryStore, cost_tracker, query_interface) |
| 042 | `ARCHITECTURE_SPEC.md` | GovernancePlugin Interface (Section 1), ValidationResult |
| 043 | `EXECUTION_ROADMAP.md` | Phase 2 deliverables (doctrine_loader, policy_checker, precedence_resolver) |
| 044 | `ARCHITECTURE_SPEC.md` | Q3a (Constitution vs .doctrine-config convergence) |
| 045 | `ARCHITECTURE_SPEC.md` | RoutingProvider Interface (Section 2), RoutingDecision |
| 046 | `EXECUTION_ROADMAP.md` | Phase 3 deliverables (agent profile bridge, capability routing) |
| 047 | `EXECUTION_ROADMAP.md` | Phase 3 (BudgetEnforcer, cost-aware routing) |
| 048 | `EXECUTION_ROADMAP.md` | Phase 4 (dashboard extension) |
| 049 | `EXECUTION_ROADMAP.md` | Phase 5 (CI error extraction) |
| 050 | `EXECUTION_ROADMAP.md` | Phase 6 (documentation, migration, `--doctrine` flag) |

---

## Estimated Timeline (Using Spec-Kitty Workflow)

Assuming serial execution with parallel WPs within each feature:

| Wave | Features | Est. Duration | Cumulative |
|---|---|---|---|
| 1 | 040 (EventBridge) | 1-2 weeks | 2 weeks |
| 2 | 041 + 042 + 045 (parallel) | 2-3 weeks | 5 weeks |
| 3 | 043 + 046 + 049 (parallel) | 2-3 weeks | 8 weeks |
| 4 | 044 + 047 (parallel) | 1-2 weeks | 10 weeks |
| 5 | 048 (Dashboard) | 1-2 weeks | 12 weeks |
| 6 | 050 (Docs & Migration) | 1 week | 13 weeks |

**Total: ~13 weeks** (aligns with the proposal's 12-14 week optimized estimate).

---

## Next Concrete Action

```bash
# 1. Navigate to spec-kitty
cd /media/stijnd/DATA/development/projects/forks/spec-kitty

# 2. Start the first feature specification
/spec-kitty.specify
# Topic: "EventBridge and telemetry foundation for Spec Kitty"
# Reference: ARCHITECTURE_SPEC.md EventBridge interface + event dataclasses
# Goal: Add structured event emission to SK's orchestrator lifecycle
```

This creates `kitty-specs/040-event-bridge-and-telemetry-foundation/spec.md` and kicks off the native workflow.
