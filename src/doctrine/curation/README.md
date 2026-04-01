# Curation

The `curation` package is the **engine** for the `_proposed/` → `shipped/` pipeline.
It owns no doctrine content — all artifact content lives in the sibling
`<type>/_proposed/` and `<type>/shipped/` directories.

Curation follows a **pull-based** model: external ideas and techniques are
imported as structured candidates, reviewed through the curation interview loop,
and either promoted to `shipped/` or dropped.

## Modules

| Module | Purpose |
|--------|---------|
| `engine.py` | Discover, promote, and drop artifacts across all artifact-type directories |
| `state.py` | Persist and resume curation session decisions (`CurationSession`) |
| `workflow.py` | Orchestration — pure business logic for the curation interview loop |

## Imports

The `imports/` subdirectory contains import fixtures used as reference examples.
For instance, `example-zombies/` demonstrates how the **ZOMBIES TDD** heuristic
is imported as a candidate tactic through the pull-based pipeline.

## Flow

```
<type>/_proposed/   ← structured artifacts awaiting curation
      ↓  (spec-kitty doctrine curate)
<type>/shipped/     ← canonised, live doctrine
```

Raw unformatted reference material (articles, excerpts, import candidates) lives in
`src/doctrine/_reference/` and feeds into `_proposed/` as a separate upstream step.
