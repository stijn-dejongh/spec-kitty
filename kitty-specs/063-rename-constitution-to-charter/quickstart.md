# Quickstart: Rename Constitution to Charter

## Verification Commands

After each stage, run these to verify progress:

```bash
# Check for remaining constitution references in Python source (excluding migrations)
grep -ri "constitution" src/ --include="*.py" | grep -v upgrade/migrations | grep -v __pycache__ | wc -l

# Check for remaining constitution references in templates/YAML (excluding historical)
grep -ri "constitution" src/ --include="*.yaml" --include="*.md" | grep -v _reference | grep -v curation | wc -l

# Run test suite
rtk test pytest tests/ --timeout=120

# Run static analysis
ruff check src/
mypy src/ --ignore-missing-imports
```

## Stage Execution Order

```
1. git mv src/doctrine/constitution/ src/doctrine/charter/
   → update imports → test → commit

2. git mv src/constitution/ src/charter/
   → rename classes/functions → update imports → test → commit

3. git mv src/specify_cli/constitution/ src/specify_cli/charter/
   → rename classes/functions → update imports → test → commit

4. git mv src/specify_cli/cli/commands/constitution.py src/specify_cli/cli/commands/charter.py
   → update CLI registration → add deprecation alias → test → commit

5. git mv command templates + skills
   → update content references → test → commit

6. Update glossary + docs
   → text replacement → verify → commit

7. Write user-project migration
   → test migration → commit

8. git mv src/doctrine/paradigms/test-first.paradigm.yaml src/doctrine/paradigms/shipped/
   → rename create-feature → create-mission
   → rename tests/constitution/ → tests/charter/
   → final sweep → commit
```

## Acceptance Gates

After Stage 8, confirm:

- [ ] `grep -ri "constitution" src/ --include="*.py" | grep -v upgrade/migrations | grep -v __pycache__` → zero hits
- [ ] `grep -ri "constitution" src/ --include="*.yaml" --include="*.md" | grep -v _reference | grep -v curation` → zero hits on active templates
- [ ] `spec-kitty charter --help` → works
- [ ] `spec-kitty constitution --help` → works + deprecation warning
- [ ] `spec-kitty agent mission create-mission --help` → works
- [ ] Full test suite passes
- [ ] `test-first` paradigm is discoverable
