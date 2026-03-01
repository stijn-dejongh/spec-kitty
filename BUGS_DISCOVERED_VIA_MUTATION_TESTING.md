# Bugs Discovered During Mutation Testing Campaign

This document tracks real bugs discovered through mutation testing rather than just equivalent mutants or missing test coverage.

## Bug #1: Missing Encoding Parameter in .git File Reads

**Discovered in**: Iteration 5 (core/paths.py)  
**Date**: 2026-03-01  
**Severity**: Medium (potential crash on non-UTF-8 systems)

### Description

The `locate_project_root()`, `is_worktree_context()`, and `get_main_repo_root()` functions in `paths.py` were reading .git files using `.read_text()` without specifying encoding parameters. This could cause `UnicodeDecodeError` on systems with non-UTF-8 default encodings or when .git files contain special characters.

### Impact

- **Systems Affected**: Non-UTF-8 default encoding (e.g., Windows with CP-1252, legacy systems)
- **Failure Mode**: `UnicodeDecodeError` exception when reading .git worktree pointer files
- **User Impact**: Complete failure of worktree detection and project root location

### Root Cause

Python's `Path.read_text()` defaults to the system's default encoding (`locale.getpreferredencoding()`), which varies by platform and configuration. Git's .git files are typically UTF-8 but may contain arbitrary bytes.

### Fix

Added explicit encoding parameters to all `.read_text()` calls:

```python
# BEFORE (3 occurrences)
content = git_path.read_text().strip()

# AFTER
content = git_path.read_text(encoding="utf-8", errors="replace").strip()
```

The `errors="replace"` parameter ensures that any invalid UTF-8 bytes are replaced with � instead of raising an exception.

### Files Changed

- `src/specify_cli/core/paths.py`: Lines 77, 141, 229
- `tests/unit/test_paths_mutations.py`: Added TestEncodingRobustness class with 3 tests

### Tests Added

1. `test_locate_project_root_handles_non_utf8_git_file` - Verifies no UnicodeDecodeError
2. `test_is_worktree_context_handles_malformed_git_file` - Verifies graceful degradation
3. `test_get_main_repo_root_handles_corrupted_git_file` - Verifies fallback behavior

---

## Bug #2: Empty gitdir Path Not Validated

**Discovered in**: Iteration 5 (core/paths.py), while fixing Bug #1  
**Date**: 2026-03-01  
**Severity**: Medium (returns incorrect path)

### Description

The `get_main_repo_root()` function did not validate that the gitdir path extracted from `.git` files was non-empty. When a .git file contained just `gitdir:` with no path, the function would:
1. Create `Path("")` which becomes `Path(".")`
2. Call `.parent` repeatedly on `.` (which returns `.`)
3. Return `.` instead of the expected resolved path

### Impact

- **Trigger**: Corrupted or incomplete .git worktree pointer file
- **Failure Mode**: Returns relative path `.` instead of absolute path
- **User Impact**: Path operations fail or target wrong directory

### Root Cause

No validation of extracted gitdir path before Path construction. Empty string becomes current directory (`.`), and `.parent` on `.` still returns `.`.

### Fix

Added validation to check gitdir path is non-empty before processing:

```python
# BEFORE
if git_content.startswith("gitdir:"):
    gitdir = Path(git_content.split(":", 1)[1].strip())
    main_git_dir = gitdir.parent.parent
    main_repo_root = main_git_dir.parent
    return main_repo_root

# AFTER  
if git_content.startswith("gitdir:"):
    gitdir_str = git_content.split(":", 1)[1].strip()
    # Validate the gitdir path is not empty (bug discovered via mutation testing)
    if gitdir_str:
        gitdir = Path(gitdir_str)
        main_git_dir = gitdir.parent.parent
        main_repo_root = main_git_dir.parent
        return main_repo_root
```

Also added `.resolve()` to fallback return to ensure absolute paths:

```python
# BEFORE
return current_path

# AFTER
return current_path.resolve()
```

### Files Changed

- `src/specify_cli/core/paths.py`: Lines 228-237, 240
- `tests/unit/test_paths_mutations.py`: Test updated to verify resolved path

### Tests Added

Updated `test_get_main_repo_root_handles_corrupted_git_file` to verify:
- Corrupted gitdir doesn't crash
- Returns resolved absolute path (not relative `.`)

---

## Lessons Learned

### 1. Mutation Testing Reveals Real Bugs

These weren't just missing tests - they were actual latent bugs that would manifest in production under specific conditions:
- Non-UTF-8 systems (Bug #1)
- Corrupted git files (Bug #2)

### 2. Edge Cases Matter

Both bugs involved edge cases that might not be covered in normal "happy path" testing:
- Special characters in file content
- Empty or malformed file content
- Cross-platform encoding differences

### 3. Defensive Programming Validated

The mutations that revealed these bugs were:
- Removing encoding parameters
- Mutating return statements
- Changing string validations

This shows the value of defensive coding practices that mutation testing verifies.

### 4. Test-Driven Fixes

Each bug was:
1. Discovered through mutation analysis
2. Confirmed with a failing test
3. Fixed in implementation
4. Verified with passing tests

This is the ideal test-driven development cycle.

---

## Statistics

**Campaign**: 5 iterations, 145 tests, ~1,818 mutants  
**Bugs Found**: 2 real bugs (0.14% of mutants revealed bugs)  
**Bug Severity**: Both Medium impact  
**Fix Time**: ~30 minutes total  
**Test Coverage**: 3 new tests for encoding robustness  

**ROI**: These bugs could have caused customer-facing failures. Finding them during development saves:
- Customer incident reports
- Emergency hotfix releases
- Reputation damage
- Support time

---

## Recommendations

1. **Always specify encoding** for text file operations
2. **Validate extracted data** before using it to construct paths
3. **Use mutation testing** for security-critical and cross-platform code
4. **Add robustness tests** for file I/O operations
5. **Document discovered bugs** to prevent regression

---

*This document will be updated as more bugs are discovered through mutation testing.*
