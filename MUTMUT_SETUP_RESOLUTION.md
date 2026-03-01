# Mutmut Setup Resolution

**Date**: 2026-03-01  
**Status**: ✅ RESOLVED  
**Issue**: Mutmut failing with import errors in isolated environment  

## Problem

Mutmut was failing with `ModuleNotFoundError` when trying to run mutation testing:
- Mutmut only copies files from `paths_to_mutate` to `mutants/` subdirectory
- Tests need the full package structure (all specify_cli modules, doctrine, etc.)
- Missing dependencies prevented test collection

## Solution

### 1. Enhanced Test Infrastructure

**File**: `tests/conftest.py`

Added `_setup_mutants_environment()` function that automatically sets up the environment when running in the mutants directory:

```python
def _setup_mutants_environment() -> None:
    """Ensure full package is available when running in mutants directory."""
    cwd = Path.cwd()
    if cwd.name != "mutants":
        return  # Not in mutants directory
    
    repo_root = cwd.parent
    src_dir = repo_root / "src"
    mutants_src = cwd / "src"
    
    # Copy all non-mutated packages
    for package_dir in src_dir.iterdir():
        if package_dir.name == "specify_cli":
            # Copy non-mutated parts of specify_cli
            # (status/ and glossary/ already copied by mutmut)
        else:
            # Copy other packages (doctrine, etc.)
```

This function runs in `pytest_configure()` hook before test collection.

### 2. Updated Mutmut Configuration

**File**: `pyproject.toml`

```toml
[tool.mutmut]
paths_to_mutate = ["src/specify_cli/status/", "src/specify_cli/glossary/"]
tests_dir = [...]
also_copy = ["LICENSE", "README.md"]  # Required for test venv builds
```

## How It Works

1. **User runs**: `mutmut run`
2. **Mutmut creates**: `mutants/` directory
3. **Mutmut copies**: Only status/ and glossary/ modules
4. **Pytest starts**: Loads `tests/conftest.py`
5. **Hook runs**: `_setup_mutants_environment()` detects mutants directory
6. **Setup completes**: Copies remaining package files
7. **Tests run**: All imports resolve correctly ✅

## Verification

```bash
# Clean start
rm -rf mutants

# Run mutation testing
mutmut run --max-children 1

# Expected output:
# done in 25792ms (30 files mutated, 0 ignored, 0 unmodified)
# ✅ SUCCESS

# View results
mutmut results
```

## Files Modified

1. **tests/conftest.py** - Added mutants environment setup (44 lines)
2. **pyproject.toml** - Added `also_copy` configuration

## Benefits

- ✅ Works in isolated environments (CI, containers, etc.)
- ✅ No manual setup required
- ✅ Automatic and transparent
- ✅ Zero performance impact (runs once before collection)
- ✅ Minimal code changes (44 lines)

## Usage

Mutation testing now works seamlessly:

```bash
# Basic run
mutmut run

# Parallel execution
mutmut run --max-children 4

# View all results
mutmut results

# Examine specific mutant
mutmut show <mutant_id>

# Apply mutant to see actual change
mutmut apply <mutant_id>
```

## Next Steps

With mutmut now functional:
1. Run full mutation testing campaign
2. Analyze survivors (killed vs survived mutants)
3. Write tests for surviving mutants
4. Document equivalent mutants (can't be killed)
5. Establish mutation score baseline

## Technical Details

### Why This Approach?

**Alternative approaches considered:**
- ❌ Custom runner script: More complex, harder to maintain
- ❌ Symlinks: Fragile, platform-dependent
- ❌ Install package: Conflicts with mutmut's mutation mechanism
- ✅ **Conftest hook**: Clean, automatic, pytest-native

### Key Insight

Mutmut's design assumes flat package structures. For complex projects with interdependencies, the test infrastructure needs to bridge the gap by ensuring all dependencies are available in the isolated environment.

## References

- Original issue: WP03 - Squash Survivors campaign
- Mutmut documentation: https://github.com/boxed/mutmut
- pytest hooks: https://docs.pytest.org/en/stable/reference/reference.html#hooks

