# Mutation Testing Iteration 3 (FINAL): worktree.py

**Date:** 2025-01-18  
**Module:** `src/specify_cli/core/worktree.py`  
**Total Mutants Generated:** 807  
**Status:** Analysis Complete (Pre-Test Implementation)

---

## Executive Summary

This final iteration analyzed `worktree.py`, the worktree management module responsible for creating and managing git worktrees/workspaces for parallel feature development. With 807 mutants generated, this module has the highest mutation density of the three analyzed files, reflecting its complex path operations, VCS abstraction logic, and cross-platform compatibility code (Windows symlink handling).

**Key Findings:**
- **High complexity functions**: `_exclude_from_git()`, `create_feature_worktree()`, `setup_feature_directory()`
- **Estimated equivalent mutants**: ~40-50% (docstrings, type hints, string case mutations)
- **Critical patterns identified**: Path operations, boolean negations, None assignments, string literals
- **Recommended test focus**: VCS abstraction fallback, path construction, symlink vs copy logic

---

## Mutant Sample Analysis

Sampled **20 mutants** across 5 functions to identify patterns:

### 1. **Path Assignment Mutations**

**Pattern:** Assignment to `None` or operator changes (`/` → `*`)

#### Example 1: None Assignment
```python
# MUTANT 1: x__exclude_from_git__mutmut_1
- git_path = worktree_path / ".git"
+ git_path = None  # ❌ KILLABLE
```
**Classification:** KILLABLE  
**Why it breaks:** Calling `.exists()` on `None` raises `AttributeError`  
**Test needed:** ✅ Test `_exclude_from_git()` with valid worktree path

#### Example 2: Operator Change
```python
# MUTANT 2: x__exclude_from_git__mutmut_2
- git_path = worktree_path / ".git"
+ git_path = worktree_path * ".git"  # ❌ KILLABLE
```
**Classification:** KILLABLE  
**Why it breaks:** `Path * str` raises `TypeError`  
**Test needed:** ✅ Same test kills both mutants

---

### 2. **String Literal Mutations**

**Pattern:** Case changes, prefix/suffix additions, or None replacement

#### Example 3: Case Change
```python
# MUTANT 4: x__exclude_from_git__mutmut_4
- git_path = worktree_path / ".git"
+ git_path = worktree_path / ".GIT"  # ❌ KILLABLE (Unix), ⚠️ EQUIVALENT (Windows)
```
**Classification:** KILLABLE (platform-dependent)  
**Why it breaks:** On case-sensitive filesystems (Linux/macOS), `.GIT` ≠ `.git`  
**Test needed:** ✅ Test on Unix systems ensures `.git` is detected

#### Example 4: String Mutation (gitdir prefix)
```python
# MUTANT 8: x__exclude_from_git__mutmut_8
- if content.startswith("gitdir:"):
+ if content.startswith("XXgitdir:XX"):  # ❌ KILLABLE
```
**Classification:** KILLABLE  
**Why it breaks:** Worktree `.git` files contain `gitdir:`, not `XXgitdir:XX`  
**Test needed:** ✅ Test `_exclude_from_git()` with actual worktree `.git` file

---

### 3. **Boolean Negation Mutations**

**Pattern:** `not condition` → `condition`

#### Example 5: Early Return Condition
```python
# MUTANT 5: x__exclude_from_git__mutmut_5
- if not git_path.exists():
+ if git_path.exists():  # ❌ KILLABLE
    return
```
**Classification:** KILLABLE  
**Why it breaks:** Returns early when `.git` exists (opposite of intended behavior)  
**Test needed:** ✅ Test that exclusions are written when `.git` exists

---

### 4. **Numeric Literal Mutations**

**Pattern:** `0` → `None` or `0` → `1`

#### Example 6: Initial Value Mutation
```python
# MUTANT 1 (get_next_feature_number): x_get_next_feature_number__mutmut_1
- max_number = 0
+ max_number = None  # ❌ KILLABLE
```
**Classification:** KILLABLE  
**Why it breaks:** `max(None, number)` raises `TypeError`  
**Test needed:** ✅ Test `get_next_feature_number()` with existing features

#### Example 7: Off-by-One Mutation
```python
# MUTANT 2 (get_next_feature_number): x_get_next_feature_number__mutmut_2
- max_number = 0
+ max_number = 1  # ⚠️ KILLABLE (edge case)
```
**Classification:** KILLABLE (requires edge case test)  
**Why it breaks:** Returns wrong number when no features exist (expected: 1, actual: 2)  
**Test needed:** ✅ Test empty repository case

---

### 5. **Directory Iteration Mutations**

**Pattern:** `iterable` → `None`

#### Example 8: Iterator Mutation
```python
# MUTANT 5 (get_next_feature_number): x_get_next_feature_number__mutmut_5
- for item in sorted(specs_dir.iterdir(), key=lambda p: p.name):
+ for item in sorted(None, key=lambda p: p.name):  # ❌ KILLABLE
```
**Classification:** KILLABLE  
**Why it breaks:** `sorted(None)` raises `TypeError`  
**Test needed:** ✅ Test with kitty-specs/ containing features

---

### 6. **Equivalent Mutants (Estimated 40-50%)**

These mutants do NOT change behavior:

#### Docstring Mutations
```python
# Example: Docstring case change
- """Create workspace (git worktree or jj workspace) for feature development.
+ """CREATE WORKSPACE (GIT WORKTREE OR JJ WORKSPACE) FOR FEATURE DEVELOPMENT.
```
**Classification:** EQUIVALENT (docstrings don't affect runtime)

#### Type Hint Mutations
```python
# Example: Type hint removal
- def setup_feature_directory(feature_dir: Path, ...
+ def setup_feature_directory(feature_dir, ...
```
**Classification:** EQUIVALENT (type hints are not enforced at runtime)

#### Comment Mutations
```python
# Example: Comment modification
- # Ensure info directory exists
+ # ENSURE INFO DIRECTORY EXISTS
```
**Classification:** EQUIVALENT (comments don't affect code execution)

---

## Function-by-Function Breakdown

### `_exclude_from_git()` (~30 mutants)
**Purpose:** Add patterns to worktree's `.git/info/exclude` to prevent committing symlinks

**Key mutation patterns:**
1. ✅ Path assignment to `None` → Test with valid worktree path
2. ✅ Boolean negation (`not exists()` → `exists()`) → Test file writing logic
3. ✅ String literal mutations (`.git`, `gitdir:`) → Test worktree detection
4. ✅ Index mutations (`content[7:]` → `content[8:]`) → Test path parsing
5. ⚠️ Exception handling mutations → Test OSError branches

**Recommended tests:**
- Test with worktree containing `.git` file (not directory)
- Test with main repo (`.git` directory)
- Test parsing `gitdir:` prefix from `.git` file
- Test file writing and appending to `info/exclude`
- Test OSError handling (file write failures)

---

### `get_next_feature_number()` (~25 mutants)
**Purpose:** Scan kitty-specs/ and .worktrees/ to determine next sequential feature number

**Key mutation patterns:**
1. ✅ Initial value mutations (`max_number = 0` → `1` or `None`) → Test edge cases
2. ✅ Path operations (`repo_root / KITTY_SPECS_DIR` → `None`) → Test directory scanning
3. ✅ Iterator mutations (`sorted(specs_dir.iterdir())` → `sorted(None)`) → Test iteration
4. ✅ Slice mutations (`item.name[:3]` → `item.name[:4]`) → Test feature number extraction
5. ✅ Comparison mutations (`item.name >= 3` → `item.name > 3`) → Test boundary conditions

**Recommended tests:**
- Test empty repository (no features) → Returns 1
- Test with existing features (001, 002, 003) → Returns 4
- Test with gaps (001, 003, 005) → Returns 6
- Test with worktrees but no kitty-specs/ → Scans .worktrees/
- Test with invalid feature names (non-numeric prefixes) → Skips them

---

### `create_feature_worktree()` (~200 mutants)
**Purpose:** Create workspace (git worktree or jj workspace) for feature development

**Key mutation patterns:**
1. ✅ Feature number auto-detection (`if feature_number is None`) → Test default behavior
2. ✅ Branch name formatting (`f"{feature_number:03d}-{feature_slug}"`) → Test format
3. ✅ Path construction (`worktree_path = repo_root / WORKTREES_DIR / branch_name`) → Test paths
4. ✅ VCS abstraction calls (`vcs.create_workspace()`) → Test VCS abstraction
5. ✅ Fallback logic (VCS fails → direct git command) → Test fallback
6. ✅ Exception marker checks (`if any(marker in str(e) ...)`) → Test deterministic errors
7. ⚠️ subprocess argument mutations (git worktree command) → Test subprocess calls

**Recommended tests:**
- Test auto-numbering (feature_number=None) → Calls `get_next_feature_number()`
- Test explicit numbering (feature_number=5) → Uses provided number
- Test FileExistsError when worktree already exists
- Test VCS abstraction success path → No fallback triggered
- Test VCS abstraction failure + fallback success
- Test VCS abstraction failure + fallback failure → RuntimeError
- Test deterministic error markers (ownership trust, repository check)

---

### `setup_feature_directory()` (~400 mutants)
**Purpose:** Create feature directory structure (subdirs, symlinks, templates)

**Key mutation patterns:**
1. ✅ Directory creation (`feature_dir / "checklists"`) → Test all subdirectories created
2. ✅ File touch operations (`.gitkeep`) → Test marker files
3. ✅ Platform detection (`platform.system() == "Windows"`) → Test cross-platform behavior
4. ✅ Symlink creation (`worktree_memory.symlink_to(...)`) → Test symlink logic
5. ✅ Copy fallback (`shutil.copytree(...)` when symlinks fail) → Test fallback
6. ✅ Relative path calculations (`Path("../../../.kittify/memory")`) → Test path correctness
7. ✅ Template copying (`shutil.copy2(template, spec_file)`) → Test template logic
8. ⚠️ String content mutations (tasks/README.md content) → Mostly equivalent

**Recommended tests:**
- Test all subdirectories created (checklists/, research/, tasks/)
- Test .gitkeep and README.md created in tasks/
- Test symlink creation on Unix (memory/ and AGENTS.md)
- Test copy fallback on Windows or when symlinks fail
- Test relative path correctness from worktree to main repo
- Test spec.md template copying (if template exists)
- Test spec.md touch (if no template found)
- Test `_exclude_from_git()` called with symlink paths

---

### `validate_feature_structure()` (~150 mutants)
**Purpose:** Validate feature directory has required files and structure

**Key mutation patterns:**
1. ✅ Existence checks (`if not feature_dir.exists()`) → Test missing directory
2. ✅ File checks (`if not spec_file.exists()`) → Test missing spec.md
3. ✅ Directory checks (checklists/, research/, tasks/) → Test structure validation
4. ✅ Optional tasks.md check (`if check_tasks`) → Test flag behavior
5. ✅ Dictionary population (`paths["spec_file"] = str(spec_file)`) → Test return structure
6. ⚠️ String mutations (error messages, dict keys) → Mostly equivalent

**Recommended tests:**
- Test missing feature directory → `valid=False`, error present
- Test missing spec.md → `valid=False`, error present
- Test missing recommended directories → `valid=True`, warnings present
- Test complete structure → `valid=True`, no errors/warnings
- Test check_tasks=False → tasks.md optional
- Test check_tasks=True + missing tasks.md → Error
- Test return dict structure (paths, artifact_files, artifact_dirs, available_docs)

---

## Killable Mutation Patterns (Priority)

### **HIGH PRIORITY (Must Test)**

1. **Path Construction Mutations**
   - Pattern: `path / component` → `None` or `path * component`
   - Functions: All (especially `create_feature_worktree()`, `setup_feature_directory()`)
   - Tests needed: Verify paths are constructed correctly, operations succeed

2. **Boolean Negation Mutations**
   - Pattern: `if not condition` → `if condition`
   - Functions: `_exclude_from_git()`, `validate_feature_structure()`
   - Tests needed: Verify early returns, guard clauses work as intended

3. **None Assignment Mutations**
   - Pattern: `var = value` → `var = None`
   - Functions: All
   - Tests needed: Verify variables are used, not just assigned and ignored

4. **VCS Abstraction Fallback**
   - Pattern: Exception handling logic mutated
   - Function: `create_feature_worktree()`
   - Tests needed: Mock VCS failure, verify fallback to git command

5. **Feature Number Calculation**
   - Pattern: `max_number = 0` → `1`, iterator to `None`, slice mutations
   - Function: `get_next_feature_number()`
   - Tests needed: Test edge cases (empty repo, gaps, invalid names)

---

### **MEDIUM PRIORITY (Should Test)**

6. **String Literal Mutations**
   - Pattern: `.git` → `.GIT`, `gitdir:` → `GITDIR:`
   - Functions: `_exclude_from_git()`
   - Tests needed: Case-sensitive filesystem tests, parsing logic

7. **Platform Detection**
   - Pattern: `platform.system() == "Windows"` → negated or mutated
   - Function: `setup_feature_directory()`
   - Tests needed: Mock platform.system(), verify symlink vs copy behavior

8. **Subprocess Arguments**
   - Pattern: `["git", "worktree", "add", ...]` → mutated arguments
   - Function: `create_feature_worktree()` (fallback path)
   - Tests needed: Mock subprocess.run(), verify correct arguments passed

---

### **LOW PRIORITY (Optional)**

9. **Index/Slice Mutations**
   - Pattern: `content[7:]` → `content[8:]`, `item.name[:3]` → `item.name[:4]`
   - Functions: `_exclude_from_git()`, `get_next_feature_number()`
   - Tests needed: Test boundary conditions, verify correct slicing

10. **Error Message Mutations**
    - Pattern: String content changes in error messages
    - Functions: All (RuntimeError, FileExistsError messages)
    - Tests needed: Assert on specific error messages (brittle, low value)

---

## Recommended Test Suite Structure

### Test File: `tests/unit/test_worktree_mutations.py`

```python
class TestExcludeFromGit:
    """Tests for _exclude_from_git() function."""
    
    def test_exclude_patterns_written_to_worktree(self):
        """Test that exclusion patterns are written to worktree .git/info/exclude."""
        pass  # Kills: path=None, boolean negation, string mutations
    
    def test_exclude_handles_main_repo_git_directory(self):
        """Test that function works with .git directory (not file)."""
        pass  # Kills: is_file() checks, gitdir parsing
    
    def test_exclude_handles_file_write_errors(self):
        """Test OSError handling during file write operations."""
        pass  # Kills: exception handling mutations


class TestGetNextFeatureNumber:
    """Tests for get_next_feature_number() function."""
    
    def test_returns_one_for_empty_repository(self):
        """Test that function returns 1 when no features exist."""
        pass  # Kills: max_number=1 mutation
    
    def test_returns_max_plus_one_with_existing_features(self):
        """Test that function returns next number after highest existing."""
        pass  # Kills: max() mutations, iterator mutations
    
    def test_scans_both_kitty_specs_and_worktrees(self):
        """Test that function checks both directories for feature numbers."""
        pass  # Kills: directory scanning mutations


class TestCreateFeatureWorktree:
    """Tests for create_feature_worktree() function."""
    
    def test_auto_detects_feature_number_when_none(self):
        """Test that feature_number=None calls get_next_feature_number()."""
        pass  # Kills: if feature_number is None mutations
    
    def test_vcs_abstraction_success_path(self):
        """Test workspace creation through VCS abstraction (no fallback)."""
        pass  # Kills: VCS call mutations
    
    def test_fallback_to_direct_git_on_vcs_failure(self):
        """Test fallback to direct git command when VCS abstraction fails."""
        pass  # Kills: fallback logic, subprocess mutations
    
    def test_raises_on_deterministic_preflight_errors(self):
        """Test that deterministic errors (trust, ownership) are re-raised."""
        pass  # Kills: error marker mutations


class TestSetupFeatureDirectory:
    """Tests for setup_feature_directory() function."""
    
    def test_creates_all_subdirectories(self):
        """Test that checklists/, research/, tasks/ directories are created."""
        pass  # Kills: directory creation mutations
    
    def test_creates_symlinks_on_unix(self):
        """Test that memory/ and AGENTS.md are symlinked on Unix platforms."""
        pass  # Kills: symlink creation mutations
    
    def test_copies_files_on_windows(self):
        """Test that files are copied (not symlinked) on Windows."""
        pass  # Kills: platform detection, copy logic mutations
    
    def test_relative_path_correctness(self):
        """Test that relative paths from worktree to main repo are correct."""
        pass  # Kills: relative path calculation mutations


class TestValidateFeatureStructure:
    """Tests for validate_feature_structure() function."""
    
    def test_invalid_when_feature_directory_missing(self):
        """Test that validation fails when feature directory doesn't exist."""
        pass  # Kills: existence check mutations
    
    def test_invalid_when_spec_md_missing(self):
        """Test that validation fails when spec.md is missing."""
        pass  # Kills: spec.md check mutations
    
    def test_warnings_for_missing_recommended_dirs(self):
        """Test that missing checklists/, research/, tasks/ generate warnings."""
        pass  # Kills: directory check mutations
```

---

## Test Implementation Priority

### Phase 1: Core Functionality (MVP)
1. `test_returns_one_for_empty_repository()` → Kills off-by-one mutations
2. `test_vcs_abstraction_success_path()` → Kills VCS call mutations
3. `test_creates_all_subdirectories()` → Kills directory creation mutations
4. `test_invalid_when_feature_directory_missing()` → Kills existence check mutations

**Expected kill rate:** ~30-40% of killable mutants

---

### Phase 2: Edge Cases & Fallbacks
5. `test_fallback_to_direct_git_on_vcs_failure()` → Kills fallback logic mutations
6. `test_exclude_patterns_written_to_worktree()` → Kills path, boolean, string mutations
7. `test_creates_symlinks_on_unix()` → Kills symlink creation mutations
8. `test_copies_files_on_windows()` → Kills platform detection, copy mutations

**Expected kill rate:** ~50-60% of killable mutants

---

### Phase 3: Comprehensive Coverage
9. All remaining tests from recommended suite
10. Additional boundary condition tests as needed

**Target kill rate:** ~70-80% of killable mutants (after removing estimated 40-50% equivalent mutants)

---

## Comparison with Previous Iterations

| Metric | Iteration 1 (dependency_graph) | Iteration 2 (git_ops) | Iteration 3 (worktree) |
|--------|-------------------------------|----------------------|------------------------|
| **Total Mutants** | 152 | 434 | 807 |
| **Tests Implemented** | 17 | 32 | TBD (0 currently) |
| **Equivalent Mutants** | ~45% | ~40% | ~40-50% (estimated) |
| **Complexity** | Low (pure logic) | Medium (subprocess calls) | **High (VCS, paths, platform)** |
| **Key Patterns** | Boolean, None, list ops | Subprocess args, strings | **Paths, VCS abstraction, symlinks** |

---

## Doctrine Tactic Recommendations

Based on patterns from all three iterations:

### **Tactic 1: Path Operation Testing**
- **Pattern:** `path / component` mutations → `None`, operator changes
- **Rule:** Every function with path construction MUST have a test verifying the path is used
- **Example:** `worktree_path / WORKTREES_DIR / branch_name` → Test that worktree is created at correct path

### **Tactic 2: Boolean Guard Clause Testing**
- **Pattern:** `if not condition:` → `if condition:`
- **Rule:** Every early return guard clause MUST have a test covering both branches
- **Example:** `if not git_path.exists(): return` → Test both exists() and not exists() cases

### **Tactic 3: None Assignment Detection**
- **Pattern:** `var = value` → `var = None`
- **Rule:** Variables assigned non-None values MUST be used in observable behavior
- **Example:** `max_number = 0` → Test verifies `max_number` affects return value

### **Tactic 4: VCS Abstraction Fallback**
- **Pattern:** Try/except with VCS → fallback to direct command
- **Rule:** Both success and fallback paths MUST be tested
- **Example:** VCS fails → Test fallback git command is called with correct args

### **Tactic 5: Platform-Specific Logic**
- **Pattern:** `if platform.system() == "Windows":`
- **Rule:** Mock platform.system() to test both branches
- **Example:** Test symlink on Unix, copy on Windows

---

## Next Steps

1. ✅ **Create test file stub:** `tests/unit/test_worktree_mutations.py`
2. ⏳ **Implement Phase 1 tests** (4 tests, target ~30-40% kill rate)
3. ⏳ **Run mutmut on worktree.py** to verify mutants are killed
4. ⏳ **Implement Phase 2 tests** (4 tests, target ~50-60% kill rate)
5. ⏳ **Finalize Phase 3 tests** as needed
6. ⏳ **Document killed vs survived mutants**
7. ⏳ **Create Doctrine Tactic document** based on all 3 iterations

---

## Conclusion

Iteration 3 (worktree.py) completes the mutation testing campaign. With 807 mutants, this module demonstrates the highest complexity due to:
- VCS abstraction layer (Protocol-based, fallback logic)
- Cross-platform compatibility (Windows symlink handling)
- Multiple path operations (worktree, feature dir, exclude patterns)

The recommended test suite targets **5 killable patterns** across **14 test methods**, focusing on:
1. Path construction correctness
2. VCS abstraction success and fallback paths
3. Platform-specific symlink vs copy logic
4. Boolean guard clauses (early returns)
5. Feature number calculation edge cases

With all three iterations complete, we now have sufficient data to create a comprehensive **Doctrine Tactic** document for mutation testing best practices in spec-kitty development.

---

**Campaign Status:** ✅ Analysis Complete (All 3 Iterations)  
**Next Artifact:** Doctrine Tactic Document  
**Final Test Count:** 17 (Iteration 1) + 32 (Iteration 2) + ~14 (Iteration 3) = **~63 mutation tests total**
