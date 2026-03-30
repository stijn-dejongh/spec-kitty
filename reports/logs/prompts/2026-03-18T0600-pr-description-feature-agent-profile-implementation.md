# PR Description Prompt — feature/agent-profile-implementation → 2.x

## Context

Use this prompt to generate the pull request description for the branch
`feature/agent-profile-implementation` targeting `2.x` (upstream develop).

---

## Prompt

You are writing a GitHub pull request description for the spec-kitty project.
Target branch: 2.x (upstream develop)
Source branch: feature/agent-profile-implementation

---

### Branch commits (in order)

1. feat: doctrine artifact domain models, C4 architecture, and curation pipeline (spec 046)
   - New standalone `src/doctrine/` package with 8 artifact types: Directive, Tactic, Styleguide,
     Toolguide, Paradigm, Procedure, AgentProfile, MissionStepContract
   - Consistent repository pattern: list_all / get / save; two-source YAML loading (shipped + project)
   - Pydantic v2 frozen models; ArtifactKind StrEnum; DoctrineService aggregation facade
   - C4 architecture docs: 00_landscape, 04_implementation_mapping, initiatives/2026-03-doctrine-execution-integration

2. feat: structured agent identity and constitution-profile integration (spec 048)
   - AgentProfileRepository with weighted context-based matching (DDR-011 scoring algorithm)
   - Hierarchy traversal (get_children / get_ancestors), cycle detection, orphan validation
   - CLI surfaces: `spec-kitty agent profile` commands (list, show, init, interview)

3. feat: doctrine curation, constitution bootstrap, and MissionStepContract (spec 054)
   - Doctrine curation pipeline: curate proposed artifacts for constitution integration
   - ConstitutionInterview, compile_constitution(), build_constitution_context() bootstrap
   - MissionStepContract domain model with DelegatesTo delegation; 4 shipped step contracts
     (implement, specify, plan, review)
   - Canonical ArtifactKind enum; MissionRepository; fix MissionRepository API for command-template lookups

4. refactor(doctrine): shared utilities, SchemaUtilities, and cycle detection
   - SchemaUtilities.load_schema() in src/doctrine/shared/ replaces 6 duplicate per-type loaders
   - DoctrineArtifactLoadError + DoctrineResolutionCycleError domain exceptions replace bare excepts
   - DFS cycle detection in reference_resolver._Walker (stack + stack_set); raises DoctrineResolutionCycleError
   - 6 unit tests (direct, self-referencing, 3-node, step-level, acyclic, diamond DAG)
   - Integration test: shipped artifact set must be cycle-free at build time

5. refactor: extract constitution to standalone peer package
   - Move src/specify_cli/constitution/ → src/constitution/ as a peer package
   - Fix circular import in catalog.py (deferred lazy import of specify_cli.runtime.home)
   - Register src/constitution in pyproject.toml hatchling build targets
   - Update CI (mypy, coverage), contextive watched paths, mutmut config
   - Add src/constitution/README.md; update architecture/2.x docs and glossary

6. fix(lint): resolve ruff and markdownlint violations in new packages
   - Fix NameError bug in catalog.py (_get_package_asset_root name mismatch)
   - Replace bare except Exception blocks with specific types (YAMLError, ValidationError,
     OSError, AttributeError, KeyError)
   - Use @functools.cache, datetime.UTC alias, strict= on zip(), ternary forms
   - Disable MD060 in .markdownlint-cli2.jsonc (project-wide pre-existing table style issue)

7. refactor(boyscout): decompose complex scoring and governance extraction functions
   - repository.py: lift calculate_score to module-level _score_profile; extract 7 signal
     functions (_language_signal, _framework_signal, _file_pattern_signal, _keyword_signal,
     _exact_id_signal, _workload_penalty, _complexity_adjustment) and _filter_candidates_by_role
   - extractor.py: extract 5 _apply_* methods from _extract_governance dispatcher;
     complexity drops from 27 to ~5
   - Removes all C901 suppressions from both packages

---

### Architectural context

This branch delivers three specs from the 2.x roadmap:
- Spec 046: Doctrine Artifact Domain Models — establishes doctrine as a standalone Python package,
  the knowledge library layer in the C4 landscape
- Spec 048: Structured Agent Identity — wires agent profiles into governance and routing workflows
- Spec 054: Constitution Bootstrap — realises the ConstitutionContainer as a standalone peer package
  (src/constitution/), consuming doctrine via DoctrineService; implements the two-stage governance
  intersection (Action Index ∩ project selections) described in architecture/2.x/03_components/

The architectural goal is separating concerns between three landscape containers:
  specify_cli (control plane) → constitution (governance onboarding + context injection) → doctrine (knowledge library)

---

### Quality baseline

- Fast test suite: 3572 passed, 5 skipped
- doctrine + constitution suites: 973 passed, 1 skipped
- ruff check src/doctrine/ src/constitution/: clean
- mypy --strict src/doctrine/ src/constitution/: clean (69 source files)
- markdownlint on touched docs: clean

---

### Why a single PR (not split)

This PR intentionally bundles three specs and their associated quality work rather than splitting
into smaller PRs. The reasoning:

The branch has a strict linear dependency chain — each layer stands on the one before it:

  spec 046 (doctrine models)
    └── spec 048 (agent profiles reference ArtifactKind, DoctrineService)
          └── spec 054 (constitution imports AgentProfile; MissionStepContract extends ArtifactKind)
                └── refactoring (SchemaUtilities, cycle detection require DoctrineService + constitution)
                      └── constitution move (all callers updated in one atomic step)
                            └── lint + boyscout (clean-up against the stable final state)

Splitting at any seam produces PRs that cannot be compiled or tested in isolation. The alternative —
a chain of draft PRs merging sequentially — adds coordination overhead without reducing reviewer
cognitive load, since the feature work and its quality clean-up touch the same files and test suite.
A single PR keeps the complete picture in one place and makes the architectural intent visible end-to-end.

---

### Output format

Write a GitHub PR description with the following sections:

**Summary**
Bullet list of user-visible changes grouped by spec/feature (CHANGELOG style).
Use conventional commit categories: feat, fix, refactor. Be concise — one line per change.

**Rationale and Architectural Goals**
2–3 paragraphs. Reference the C4 landscape model (doctrine / constitution / specify_cli containers).
Reference the specs by number. Explain why the constitution package move is architecturally correct
(peer container, not sub-module).

**Key Review Focus Areas**
A numbered list of 4–6 things the reviewer should pay closest attention to, with file paths.
Focus on: correctness risks, API surface decisions, and test coverage gaps.

**Additional Improvements**
A short bulleted list of boyscout improvements made while working in the area (not spec-mandated).
Label each as the type: [bug fix], [code quality], [lint], [documentation].

**Why a single PR**
A short paragraph (3–5 sentences) explaining the dependency chain and the deliberate choice to
bundle rather than split. Use the dependency tree above as the basis.

**Test Plan**
A concise checklist the reviewer can use to verify the PR locally.
