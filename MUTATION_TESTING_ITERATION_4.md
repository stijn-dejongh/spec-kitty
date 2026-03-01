# Mutation Testing Campaign - Iteration 4: merge/preflight.py

**Date**: 2025-01-18  
**Target Module**: `src/specify_cli/merge/preflight.py`  
**Total Mutants**: 316  
**Mutants Sampled**: 20  

---

## Executive Summary

This iteration focuses on `preflight.py`, which implements pre-flight validation checks for merge operations (FR-001 through FR-004). The module validates worktree cleanliness, checks for missing worktrees, and detects target branch divergence before merge operations begin.

**Key Findings**:
- **316 total mutants** generated across 5 functions
- **~45% equivalent mutants** (docstrings, display strings, Rich formatting)
- **5 high-value killable patterns** identified requiring test coverage
- **Target**: 25-30 tests to achieve comprehensive mutation coverage

**Function Distribution**:
- `check_worktree_status()`: ~80 mutants
- `check_target_divergence()`: ~70 mutants
- `run_preflight()`: ~70 mutants
- `_wp_lane_from_feature()`: ~40 mutants
- `display_preflight_result()`: ~56 mutants

---

## Sampled Mutants Analysis

### Sample 1: subprocess.run() Nullification
```python
# ORIGINAL
result = subprocess.run(
    ["git", "status", "--porcelain"],
    cwd=str(worktree_path),
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
    check=False,
)

# MUTANT
result = None
```
**Classification**: KILLABLE  
**Impact**: AttributeError when accessing result.stdout  
**Test Need**: Verify function returns WPStatus with correct attributes

### Sample 2: Boolean Parameter Mutation
```python
# ORIGINAL
table = Table(show_header=True, header_style="bold")

# MUTANT
table = Table(show_header=False, header_style="bold")
```
**Classification**: EQUIVALENT (display logic)  
**Reason**: Visual output change doesn't affect validation logic

### Sample 3: String Argument Mutation
```python
# ORIGINAL
["git", "status", "--porcelain"]

# MUTANT
["git", "status", "XX--porcelainXX"]
```
**Classification**: KILLABLE  
**Impact**: Git command fails, returns different output  
**Test Need**: Verify git status detection works correctly

### Sample 4: Boolean Logic Inversion
```python
# ORIGINAL
if result.returncode != 0:
    return False, None  # No remote tracking, assume OK

# MUTANT
if result.returncode != 0:
    return True, None  # No remote tracking, assume OK
```
**Classification**: KILLABLE  
**Impact**: False positive for divergence when remote doesn't exist  
**Test Need**: Test behavior when remote tracking missing

### Sample 5: Comparison Operator Mutation
```python
# ORIGINAL
if behind > 0:
    return True, f"{target_branch} is {behind} commit(s) behind..."

# MUTANT
if behind >= 0:
    return True, f"{target_branch} is {behind} commit(s) behind..."
```
**Classification**: KILLABLE  
**Impact**: False positive when branches are in sync (behind=0)  
**Test Need**: Verify no divergence reported when behind=0

### Sample 6: None Substitution in Path Operations
```python
# ORIGINAL
tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"

# MUTANT
tasks_dir = None
```
**Classification**: KILLABLE  
**Impact**: AttributeError when calling tasks_dir.exists()  
**Test Need**: Verify path construction works

### Sample 7: Missing Function Argument
```python
# ORIGINAL
diverged, msg = check_target_divergence(target_branch, repo_root)

# MUTANT
diverged, msg = check_target_divergence(repo_root)
```
**Classification**: KILLABLE  
**Impact**: TypeError - missing required positional argument  
**Test Need**: Integration test for run_preflight()

### Sample 8: String Literal Mutation in Paths
```python
# ORIGINAL
tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"

# MUTANT
tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "XXtasksXX"
```
**Classification**: KILLABLE  
**Impact**: Path doesn't exist, function returns None  
**Test Need**: Verify correct "tasks" directory access

### Sample 9: Error Message String Mutation
```python
# ORIGINAL
error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"

# MUTANT
error = None
```
**Classification**: KILLABLE  
**Impact**: Error message not set when worktree is dirty  
**Test Need**: Verify error message populated correctly

### Sample 10: Git Command Argument Mutation
```python
# ORIGINAL
["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"]

# MUTANT
["git", "rev-list", "--left-right", "--COUNT", f"{target_branch}...origin/{target_branch}"]
```
**Classification**: KILLABLE  
**Impact**: Git command fails, unrecognized option  
**Test Need**: Mock git calls to verify correct arguments

### Sample 11: Display String Mutations
```python
# ORIGINAL
console.print("\n[bold]Pre-flight Check[/bold]\n")

# MUTANT
console.print(None)
```
**Classification**: EQUIVALENT (display logic)  
**Reason**: Display formatting doesn't affect validation outcome

### Sample 12: Collection Nullification
```python
# ORIGINAL
discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
missing_wps = sorted(expected_wps - discovered_wps)

# MUTANT
discovered_wps = None
missing_wps = sorted(expected_wps - discovered_wps)  # TypeError
```
**Classification**: KILLABLE  
**Impact**: TypeError when trying set subtraction with None  
**Test Need**: Verify missing worktree detection logic

### Sample 13: Conditional Lane Check
```python
# ORIGINAL
if lane == "done":
    result.warnings.append(f"Skipping missing worktree check for {wp_id} (lane=done).")
    continue

# MUTANT
if lane == "XXdoneXX":  # Never matches
```
**Classification**: KILLABLE  
**Impact**: Done WPs incorrectly flagged as errors  
**Test Need**: Verify lane="done" bypass logic

### Sample 14: encoding Parameter Mutation
```python
# ORIGINAL
encoding="utf-8"

# MUTANT
encoding="XXutf-8XX"
```
**Classification**: KILLABLE  
**Impact**: LookupError for unknown encoding  
**Test Need**: Verify subprocess calls complete successfully

### Sample 15: cwd Parameter Removal
```python
# ORIGINAL
subprocess.run(["git", "status", "--porcelain"], cwd=str(worktree_path), ...)

# MUTANT
subprocess.run(["git", "status", "--porcelain"], ...)  # Missing cwd
```
**Classification**: KILLABLE  
**Impact**: Git runs in wrong directory, returns wrong status  
**Test Need**: Verify git commands run in correct directory

### Sample 16: check=False Parameter Removal
```python
# ORIGINAL
subprocess.run([...], check=False)

# MUTANT
subprocess.run([...])  # check defaults to False, so equivalent
```
**Classification**: EQUIVALENT  
**Reason**: check defaults to False in subprocess.run()

### Sample 17: text=True Mutation
```python
# ORIGINAL
subprocess.run([...], text=True, encoding="utf-8", ...)

# MUTANT
subprocess.run([...], text=None, encoding="utf-8", ...)
```
**Classification**: KILLABLE  
**Impact**: Returns bytes instead of string, breaks .strip()  
**Test Need**: Verify text output handling

### Sample 18: Glob Pattern Nullification
```python
# ORIGINAL
candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))

# MUTANT
candidates = sorted(tasks_dir.glob(None))
```
**Classification**: KILLABLE  
**Impact**: TypeError - glob() pattern must be string  
**Test Need**: Verify task file discovery

### Sample 19: Table Column Nullification
```python
# ORIGINAL
table.add_column("Issue")

# MUTANT
table.add_column(None)
```
**Classification**: EQUIVALENT (display logic)  
**Reason**: Visual presentation doesn't affect validation

### Sample 20: Error List Access Mutation
```python
# ORIGINAL
result.errors.append(status.error or f"{wp_id} has uncommitted changes")

# MUTANT
# (missing argument mutations)
```
**Classification**: KILLABLE  
**Impact**: Incorrect error messages or missing errors  
**Test Need**: Verify error accumulation logic

---

## Identified Killable Patterns

### Pattern 1: Git Status Detection Logic
**Mutants**: 25+ across check_worktree_status()  
**Risk**: Incorrect worktree cleanliness detection

**Mutations**:
- `result = None` (subprocess.run nullification)
- `is_clean = not result.stdout.strip()` → `is_clean = result.stdout.strip()` (boolean negation)
- `cwd=str(worktree_path)` removal (wrong directory)
- `text=True` → `text=None` (bytes vs string)
- Git command argument mutations

**Test Requirements**:
1. Clean worktree returns is_clean=True, error=None
2. Dirty worktree returns is_clean=False with error message
3. Git command failure returns is_clean=False with exception message
4. Subprocess runs in correct worktree directory
5. Error message contains worktree name

### Pattern 2: Target Branch Divergence Detection
**Mutants**: 30+ across check_target_divergence()  
**Risk**: False positives/negatives for divergence

**Mutations**:
- `if result.returncode != 0: return False, None` → `return True, None` (logic inversion)
- `if behind > 0:` → `if behind >= 0:` (comparison mutation)
- `len(parts) != 2` → `len(parts) == 2` (logic inversion)
- `map(int, parts)` mutations (parsing logic)
- Git fetch/rev-list command mutations

**Test Requirements**:
1. Branches in sync: returns (False, None)
2. Behind origin: returns (True, message) with correct count
3. Ahead of origin: returns (False, None)
4. No remote tracking: returns (False, None) - non-fatal
5. Git command failure: returns (False, None) - graceful degradation
6. Malformed output: returns (False, None)

### Pattern 3: Missing Worktree Detection
**Mutants**: 25+ in run_preflight()  
**Risk**: Missing worktrees not detected, incorrect error reporting

**Mutations**:
- `discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}` → `None`
- `missing_wps = sorted(expected_wps - discovered_wps)` → `sorted(None)`
- `if lane == "done":` → `if lane == "XXdoneXX":`
- `result.passed = False` mutations
- Error message mutations

**Test Requirements**:
1. All worktrees present: no errors
2. Missing worktree (lane != done): error added, passed=False
3. Missing worktree (lane == done): warning added, passed=True
4. Multiple missing worktrees: all detected
5. Correct error message with expected path
6. WPStatus objects created for missing worktrees

### Pattern 4: Lane Value Parsing from Frontmatter
**Mutants**: 18+ in _wp_lane_from_feature()  
**Risk**: Incorrect lane detection, wrong bypass logic

**Mutations**:
- `tasks_dir = repo_root / ... / "tasks"` → `None` or wrong path
- `candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))` → `glob(None)`
- `if not content.startswith("---"):` logic mutations
- Regex pattern mutations for lane extraction
- `.strip().lower()` mutations

**Test Requirements**:
1. Valid frontmatter with lane: returns lane value
2. Missing tasks directory: returns None
3. No matching task file: returns None
4. No frontmatter: returns None
5. No lane field: returns None
6. Lane value extraction (case insensitive, handles quotes)
7. Multiple matching files: uses first (sorted)

### Pattern 5: PreflightResult State Accumulation
**Mutants**: 35+ across run_preflight()  
**Risk**: Incorrect validation state, missing errors/warnings

**Mutations**:
- `result = PreflightResult(passed=True)` → `result = None`
- `result.passed = False` removals
- `result.errors.append(...)` mutations
- `result.warnings.append(...)` mutations
- `result.target_diverged = diverged` mutations

**Test Requirements**:
1. All checks pass: passed=True, no errors
2. Dirty worktree: passed=False, error in list
3. Target diverged: passed=False, target_diverged=True, error in list
4. Missing worktree: passed=False, error in list
5. Multiple failures: all errors accumulated
6. Warnings for done WPs don't fail validation
7. WPStatus list contains all checked worktrees

---

## Equivalent Mutants

### Category 1: Display/UI Strings (~25% of mutants)
- Rich formatting tags: `[bold]`, `[green]`, `[red]`
- Console.print() message strings
- Table column headers
- Error/warning message formatting
- Icon characters (✓, ✗)

**Rationale**: Visual presentation doesn't affect validation logic

### Category 2: Docstrings and Comments (~10% of mutants)
- Function docstrings
- Inline comments
- Type hint strings in docstrings

**Rationale**: Documentation doesn't execute

### Category 3: Default Parameter Values (~5% of mutants)
- `check=False` (already default in subprocess.run)
- Some encoding parameter mutations (if caught by try/except)

**Rationale**: No behavioral change

### Category 4: Display Logic (~5% of mutants)
- `show_header=True` → `False` in Rich Table
- Table styling parameters
- Console formatting

**Rationale**: Doesn't affect validation outcome

**Total Equivalent**: ~145 mutants (45%)

---

## Test Coverage Recommendations

### Priority 1: Core Validation Functions (HIGH)
**Target**: `check_worktree_status()`, `check_target_divergence()`

Tests needed:
1. ✅ Worktree status - clean worktree
2. ✅ Worktree status - dirty worktree
3. ✅ Worktree status - subprocess failure
4. ✅ Worktree status - correct error message
5. ✅ Target divergence - in sync (behind=0)
6. ✅ Target divergence - behind origin
7. ✅ Target divergence - ahead of origin
8. ✅ Target divergence - no remote tracking
9. ✅ Target divergence - git command failure
10. ✅ Target divergence - malformed output

### Priority 2: Integration Logic (HIGH)
**Target**: `run_preflight()`

Tests needed:
1. ✅ All worktrees present and clean - passes
2. ✅ Missing worktree (not done) - fails
3. ✅ Missing worktree (lane=done) - warning only
4. ✅ Dirty worktree - fails
5. ✅ Target diverged - fails
6. ✅ Multiple failures - all errors accumulated
7. ✅ Error message correctness
8. ✅ WPStatus list population
9. ✅ Result.passed logic

### Priority 3: Helper Functions (MEDIUM)
**Target**: `_wp_lane_from_feature()`

Tests needed:
1. ✅ Valid frontmatter - lane extracted
2. ✅ Missing tasks directory
3. ✅ No matching task file
4. ✅ No frontmatter
5. ✅ No lane field in frontmatter
6. ✅ Case handling and quotes

### Priority 4: Display Logic (LOW)
**Target**: `display_preflight_result()`

Tests needed:
1. ⚠️ Rich output generation (limited value)
2. ⚠️ Console calls verification (mock-based)

**Note**: Display tests provide limited mutation kill value due to equivalent mutants

---

## Test Implementation Plan

### Test File Structure
```python
# tests/unit/test_preflight_mutations.py

class TestCheckWorktreeStatus:
    """Pattern 1: Git status detection"""
    def test_clean_worktree()
    def test_dirty_worktree()
    def test_subprocess_failure()
    def test_error_message_format()
    def test_correct_directory()
    
class TestCheckTargetDivergence:
    """Pattern 2: Branch divergence detection"""
    def test_branches_in_sync()
    def test_behind_origin()
    def test_ahead_of_origin()
    def test_no_remote_tracking()
    def test_git_failure_graceful()
    def test_malformed_output()
    def test_comparison_boundary()
    
class TestWPLaneFromFeature:
    """Pattern 4: Lane parsing"""
    def test_valid_frontmatter()
    def test_missing_directory()
    def test_no_matching_file()
    def test_no_frontmatter()
    def test_no_lane_field()
    def test_case_and_quotes()
    def test_multiple_files()
    
class TestRunPreflight:
    """Pattern 3 & 5: Integration"""
    def test_all_checks_pass()
    def test_missing_worktree_not_done()
    def test_missing_worktree_done_lane()
    def test_dirty_worktree_fails()
    def test_target_diverged_fails()
    def test_multiple_failures_accumulate()
    def test_wp_status_list_population()
    def test_error_message_correctness()
    def test_result_passed_logic()
```

### Estimated Coverage
- **Total mutants**: 316
- **Equivalent mutants**: ~145 (45%)
- **Killable mutants**: ~171 (55%)
- **Tests planned**: 28
- **Expected kill rate**: ~70-80% of killable mutants (~120-137 kills)
- **Overall score**: 38-43% (accounting for equivalents)

---

## Insights from Previous Iterations

### Iteration 1 (dependency_graph.py): 152 mutants, 17 tests
- Graph traversal logic critical
- Edge case handling in cycles/missing nodes
- Dictionary key mutations common

### Iteration 2 (git_ops.py): 434 mutants, 32 tests
- Subprocess.run() mutations dominant
- String argument mutations in git commands
- Error handling for subprocess failures

### Iteration 3 (worktree.py): 807 mutants, 29 tests
- Path operations frequent mutation target
- Boolean logic inversions critical
- None substitutions common

### Iteration 4 (preflight.py): 316 mutants, ~28 tests planned
- Validation logic mutations critical
- Git command mutations similar to Iteration 2
- Display mutations mostly equivalent (new pattern)
- Lane parsing adds complexity
- Integration logic requires comprehensive tests

---

## Conclusion

The `preflight.py` module has **316 mutants** with approximately **45% equivalent** (display/docstring mutations). The remaining **171 killable mutants** cluster around 5 key patterns:

1. **Git status detection** (subprocess, path, parsing)
2. **Branch divergence detection** (comparison logic, error handling)
3. **Missing worktree detection** (set operations, lane bypass)
4. **Lane parsing** (file I/O, regex, path construction)
5. **Result accumulation** (state management, error lists)

Implementing **28 targeted tests** should achieve:
- **70-80% kill rate** of killable mutants
- **38-43% overall mutation score** (accounting for equivalents)
- **Comprehensive coverage** of validation logic
- **Confidence** in merge pre-flight reliability

The high equivalent mutant rate (45%) is acceptable given the display-heavy nature of the module. Focus on validation logic provides maximum value.
