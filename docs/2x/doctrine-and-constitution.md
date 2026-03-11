# 2.x Doctrine and Constitution

## Doctrine Artifact Model

2.x doctrine artifacts are repository-native and typed:

1. Directives: `src/doctrine/directives/*.directive.yaml`
2. Tactics: `src/doctrine/tactics/*.tactic.yaml`
3. Styleguides: `src/doctrine/styleguides/**/*.styleguide.yaml`
4. Toolguides: `src/doctrine/toolguides/*.toolguide.yaml`
5. Schemas: `src/doctrine/schemas/*.schema.yaml`
6. Mission assets/templates: `src/doctrine/missions/**`

Artifact integrity is enforced by:

1. `tests/doctrine/test_schema_validation.py`
2. `tests/doctrine/test_artifact_compliance.py`
3. `tests/doctrine/test_tactic_compliance.py`

## Constitution Lifecycle in 2.x

The constitution flow is command-driven. The interview step is **required** — `generate` will
exit non-zero with an actionable error if `answers.yaml` is absent.

1. `spec-kitty constitution interview` — Capture project answers (paradigms, directives, tools)
2. `spec-kitty constitution generate --from-interview` — Compile bundle from answers + shipped doctrine
3. `spec-kitty constitution context --action <specify|plan|implement|review>` — Load governance context
4. `spec-kitty constitution status` — Check sync state
5. `spec-kitty constitution sync` — Re-extract YAML config files from `constitution.md`

**Validation behaviour:**

- Shipped doctrine catalog is validated at compile time; unrecognised IDs are reported as diagnostics
  but do not abort generation.
- Project-local support files (declared in `answers.yaml`) are accepted without catalog-ID validation.
  They supplement shipped doctrine and appear in `references.yaml` as `kind: local_support`.
- Local support files that overlap a shipped concept emit an additive conflict warning; both entries
  are kept.
- `governance.yaml`, `directives.yaml`, and `metadata.yaml` are emitted by `constitution sync`.
  `agents.yaml` is **not** emitted.

**Context bootstrap behaviour:**

- First call to `constitution context --action <action>` returns full governance context (depth 2).
- Subsequent calls for the same action return compact context (depth 1) by default.
- Bootstrap state is persisted in `.kittify/constitution/context-state.json`.
- An explicit `--depth` flag overrides the bootstrap auto-selection.

Primary implementation:

1. `src/specify_cli/cli/commands/constitution.py`
2. `src/specify_cli/constitution/compiler.py`
3. `src/specify_cli/constitution/context.py`

## 2.x Constitution Paths

Current bundle location:

1. `.kittify/constitution/constitution.md`
2. `.kittify/constitution/interview/answers.yaml`
3. `.kittify/constitution/references.yaml`
4. `.kittify/constitution/context-state.json` — first-load bootstrap tracking

Legacy compatibility is still handled for projects with older layout, but 2.x documentation treats `.kittify/constitution/` as canonical.

> **Note:** The `library/` subdirectory used in earlier builds has been removed.
> Shipped doctrine content is fetched at runtime from the packaged `src/doctrine/` tree;
> project-local support files are referenced via paths recorded in `references.yaml`.

## Runtime Template Resolution

When resolving templates and mission assets, 2.x uses ordered precedence:

1. Project override
2. Project legacy location
3. User-global mission-specific location
4. User-global location
5. Packaged doctrine mission defaults

Implementation references:

1. `src/specify_cli/runtime/resolver.py`
2. `src/specify_cli/runtime/home.py`
