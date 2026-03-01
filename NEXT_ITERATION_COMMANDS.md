# Mutation Testing - Next Iteration Commands

## Quick Reference

### Run Iteration 1 Tests (once implemented)
```bash
cd /home/runner/work/spec-kitty/spec-kitty
pytest tests/unit/test_dependency_graph_mutations.py -v
```

### Re-run Mutation Testing (check progress)
```bash
cd /home/runner/work/spec-kitty/spec-kitty
mutmut run  # Uses existing .mutmut-cache, will check all 152 mutants
```

### Show Mutation Results
```bash
mutmut results  # List all mutants and their status (killed/survived/timeout)
mutmut results --status killed  # Show only killed mutants
mutmut results --status survived  # Show survivors for iteration 2
```

### Sample Survivors
```bash
# Show first 5 survivors
mutmut results --status survived | head -5

# Show specific survivor details
mutmut show "specify_cli.core.dependency_graph.x_function__mutmut_42"
```

## Iteration Workflow

1. **Implement Tests** (Priority 1)
   - Edit `tests/unit/test_dependency_graph_mutations.py`
   - Replace `pass` statements with actual test logic
   - Focus on 8 priority tests first

2. **Verify Tests Pass**
   ```bash
   pytest tests/unit/test_dependency_graph_mutations.py -v
   ```

3. **Run Mutation Testing**
   ```bash
   mutmut run
   # This will test all 152 mutants against your tests
   # Expect ~20-30 minutes runtime
   ```

4. **Analyze Results**
   ```bash
   mutmut results | grep -E "(killed|survived|timeout)" | wc -l
   # Count survivors for next iteration
   ```

5. **Sample Survivors** (Iteration 2)
   ```bash
   # Get list of survivor IDs
   mutmut results --status survived > survivors.txt
   
   # Sample 10-15 survivors to identify new patterns
   for id in $(head -15 survivors.txt); do
       mutmut show "$id"
   done
   ```

## Expected Outcomes

### After Iteration 1 (Priority 1 tests)
- **Target**: Kill 40-50% of killable mutants (~20-25 mutants)
- **Survivors**: ~75-80 mutants remaining (including ~50% equivalents)

### Iteration 2 Goals
- Sample 10-15 survivors
- Identify new killable patterns
- Add 5-10 more targeted tests
- Target: Kill another 20-30% of remaining killable mutants

## Troubleshooting

### If mutmut run fails with import errors
```bash
# Ensure dependencies installed in mutants directory
cd mutants/
pip install -e ..
cd ..
mutmut run
```

### If tests are too slow
```bash
# Run with pytest-xdist for parallelization
pip install pytest-xdist
pytest -n auto tests/unit/test_dependency_graph_mutations.py
```

### To reset and start fresh
```bash
rm -rf .mutmut-cache mutants/
mutmut run  # Regenerates everything
```

## Notes

- Mutmut caches results in `.mutmut-cache` (SQLite database)
- Each run only tests changed mutants (incremental)
- Use `mutmut export-cicd-stats` for detailed metrics
- Equivalent mutants (~50%) will always survive - this is expected

## Files to Track

- `MUTATION_TESTING_ITERATION_1.md` - Current iteration findings
- `MUTATION_TESTING_ITERATION_2.md` - Next iteration findings (create after step 5)
- `.mutmut-cache` - Mutation test results (git-ignored)
- `mutants/` - Temporary mutant code (git-ignored)
