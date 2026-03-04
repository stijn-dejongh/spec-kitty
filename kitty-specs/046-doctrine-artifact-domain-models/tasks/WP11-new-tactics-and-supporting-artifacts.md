---
work_package_id: WP11
title: New Tactics & Supporting Artifacts
lane: planned
dependencies:
- WP01
- WP02
- WP03
- WP04
- WP07
- WP08
- WP09
subtasks:
- T064
- T065
- T066
- T067
- T068
phase: Phase 2 - Content
assignee: ''
agent: ''
shell_pid: ''
review_status: ''
reviewed_by: ''
history:
- timestamp: '2026-02-26T04:36:22Z'
  lane: planned
  agent: system
  shell_pid: ''
  action: Prompt generated via /spec-kitty.tasks
---

# Work Package Prompt: WP11 – New Tactics & Supporting Artifacts

## ⚠️ IMPORTANT: Review Feedback Status

- **Has review feedback?**: Check the `review_status` field above.

---

## Review Feedback

*[This section is empty initially.]*

---

## Objectives & Success Criteria

- Audit all enriched and new directives for `tactic-refs` that point to non-existent tactics
- Create new tactic YAML files for every unresolved reference
- Create new styleguide/toolguide YAML files if referenced by directives or tactics
- Every `tactic-ref` in every shipped directive resolves to a tactic file in `shipped/`
- All new artifacts validate against their respective schemas
- Only create artifacts that are actually referenced — no speculative creation

## Context & Constraints

- **Depends on WP02-04**: Repositories must exist for validation
- **Depends on WP07-09**: Enriched directives must be finalized to know which refs are needed
- **Reference material**: `src/doctrine/doctrine_ref/tactics/` for tactic content
- **Minimum viable tactic**: `schema-version`, `id`, `name`, `steps` (at least 1 step)

## Subtasks & Detailed Guidance

### Subtask T064 – Audit directives for unresolved tactic_refs

- **Purpose**: Build a complete list of tactic IDs referenced but not yet existing.
- **Steps**:
  1. Load all shipped directives via `DirectiveRepository().list_all()`
  2. Collect all unique `tactic_refs` values across all directives
  3. For each tactic ref, check if `TacticRepository().get(ref)` returns a result
  4. Build list of unresolved refs (tactic ID + which directive(s) reference it)
  5. Document the audit results as a comment in the implementation
  6. Also check `TacticReference` objects in shipped tactics — any references to non-existent artifacts?
- **Files**: No file changes — this is an audit step
- **Notes**: The output of this audit drives T065-T067. If no unresolved refs exist, T065-T067 may be no-ops.

### Subtask T065 – Create new tactic YAML files

- **Purpose**: Create tactic files for every unresolved tactic-ref.
- **Steps**:
  1. For each unresolved tactic ref from T064:
     - Check `src/doctrine/doctrine_ref/tactics/` for reference content
     - Create `src/doctrine/tactics/shipped/{tactic-id}.tactic.yaml`
     - Follow existing tactic schema structure:
       ```yaml
       schema-version: "1.0"
       id: {tactic-id}
       name: "{Human Readable Name}"
       purpose: |
         Description of what this tactic achieves.
       steps:
         - title: "Step 1 Name"
           description: |
             Detailed description of step 1.
         - title: "Step 2 Name"
           description: |
             Detailed description of step 2.
       ```
     - Minimum 2-3 steps per tactic (meaningful, not filler)
  2. Validate each new tactic against `tactic.schema.yaml`
  3. Verify `TacticRepository().get(tactic_id)` returns the new tactic
- **Files**: `src/doctrine/tactics/shipped/*.tactic.yaml` (new files, count depends on audit)
- **Parallel?**: Yes — each tactic file is independent
- **Notes**: Likely new tactics include those referenced by the new directives (020-026). Check the enriched directives (WP07-08) too for newly wired tactic-refs.

### Subtask T066 – Create new styleguide YAML files

- **Purpose**: Create styleguide files if any directives or tactics reference non-existent styleguides.
- **Steps**:
  1. Check all `TacticReference` objects where `type == "styleguide"`
  2. Verify each referenced styleguide exists in `StyleguideRepository`
  3. Create any missing styleguide files in `src/doctrine/styleguides/shipped/`
  4. Follow existing styleguide schema structure
  5. Validate against `styleguide.schema.yaml`
- **Files**: `src/doctrine/styleguides/shipped/*.styleguide.yaml` (new files if needed)
- **Notes**: May be a no-op if all styleguide references already resolve

### Subtask T067 – Create new toolguide YAML files

- **Purpose**: Create toolguide files if any references point to non-existent toolguides.
- **Steps**: Same pattern as T066 but for toolguides
- **Files**: `src/doctrine/toolguides/shipped/*.toolguide.yaml` (new files if needed)
- **Notes**: May be a no-op

### Subtask T068 – Validate all new artifacts against schemas

- **Purpose**: Final validation pass for all artifacts created in this WP.
- **Steps**:
  1. Load all new tactics via `TacticRepository` — verify no load errors
  2. Load all new styleguides/toolguides — verify no load errors
  3. Validate each against its schema using the validation utility
  4. Re-run the consistency check from T064 — all tactic-refs should now resolve
  5. Run `pytest tests/doctrine/test_consistency.py` — must pass
- **Files**: No new files — validation only
- **Notes**: This is the gate check — if consistency tests fail, new artifacts are incomplete

## Test Strategy

```bash
# Validate new artifacts load correctly
pytest tests/doctrine/ -v -k "consistency"

# Verify all tactic-refs resolve
python -c "
from doctrine.service import DoctrineService
s = DoctrineService()
unresolved = []
for d in s.directives.list_all():
    for ref in d.tactic_refs:
        if not s.tactics.get(ref):
            unresolved.append((d.id, ref))
if unresolved:
    print('UNRESOLVED:', unresolved)
else:
    print('All tactic-refs resolve!')
"
```

## Risks & Mitigations

- **doctrine_ref tactics may be incomplete**: Some tactic references from enriched directives may not have corresponding doctrine_ref material — create minimal but meaningful tactic content
- **Cascade of missing artifacts**: One missing tactic may reference another missing styleguide — audit deeply before creating

## Review Guidance

- Verify every previously-unresolved tactic-ref now resolves
- Verify new tactics have meaningful content (not placeholder/filler)
- Verify no speculative artifacts created (only those actually referenced)
- Verify `test_consistency.py` passes

## Activity Log

- 2026-02-26T04:36:22Z – system – lane=planned – Prompt created.

---

### Implementation Command

Depends on WP02-04 and WP07-09:
```bash
spec-kitty implement WP11 --base WP07
```
Then merge other dependencies:
```bash
cd .worktrees/046-doctrine-artifact-domain-models-WP11/
git merge <WP08-branch>
git merge <WP09-branch>
git merge <WP02-branch>
git merge <WP03-branch>
git merge <WP04-branch>
```
