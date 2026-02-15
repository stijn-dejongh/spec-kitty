# tmp/ — Working Documents

> **Purpose**: Staging area for collaborative design and system evolution.
>
> Contents here are **versioned** to enable collaboration and portability
> across branches and contributors. They are **intended to be removed**
> once their ideas have been incorporated into the main codebase
> (e.g., as missions, templates, migrations, or documentation).

## Current Contents

| Directory | Source | Purpose | Target |
|-----------|--------|---------|--------|
| `doctrine/` | [Doctrine stack](https://github.com/robertDouglass/quickstart_agent-augmented-development) | Reference material for design mission development | `src/specify_cli/missions/design/` |
| `doctrine-missions/` | Internal analysis | Design mission fit analysis and notes | `src/specify_cli/missions/design/` |
| `design-mission/templates/` | Derived from Doctrine + gist artifacts | Template prototypes for the design mission | `src/specify_cli/missions/design/templates/` |

## Rules

1. **Do not build production code here** — this is for research, prototyping, and reference
2. **Do reference from here** — agents and contributors should read `tmp/` during design work
3. **Do remove when done** — once content is incorporated, delete the source from `tmp/`
4. **Do commit** — this directory is versioned for collaboration, not gitignored
