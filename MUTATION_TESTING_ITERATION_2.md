# Mutation Testing Campaign - Iteration 2

## Target: git_ops.py

### Summary
- **Mutants Generated**: 434
- **Sampled**: 17 mutants across all 9 functions
- **Date**: 2025-03-01

---

## Killable Patterns Found

### 1. **None Assignment Mutations** - Critical Logic Breaker
**Pattern**: Assignment statements mutated to `None`
**Examples**:
- `target = (path or Path.cwd()).resolve()` → `target = None` (is_git_repo_1)
- `repo_path = (path or Path.cwd()).resolve()` → `repo_path = None` (get_current_branch_1)
- `result = subprocess.run(...)` → `result = None` (has_tracking_branch_1, resolve_primary_branch_1)
- `exclude_file = repo_path / ".git" / "info" / "exclude"` → `exclude_file = None` (exclude_from_git_index_1)
- `meta_file = repo_path / "kitty-specs" / feature_slug / "meta.json"` → `meta_file = None` (resolve_target_branch_10)
- `target = fallback` → `target = None` (resolve_target_branch_20)

**Why Killable**: These break core data structure initialization, causing AttributeError/TypeError on first use (e.g., `None.is_dir()`, `None.returncode`)

**Estimated Count**: ~60-80 mutants across functions

**Test Strategy**: 
- Verify functions handle None path arguments correctly (defaults to current dir)
- Test subprocess calls with mocks to ensure result is not None
- Test file path construction works correctly

---

### 2. **Boolean Condition Negation** - Path Coverage Breaker
**Pattern**: Boolean conditions flipped
**Examples**:
- `console if console is not None` → `console if console is None` (_resolve_console_1)
- `respect_current: bool = True` → `respect_current: bool = False` (resolve_target_branch_1)
- Various boolean checks in subprocess result handling

**Why Killable**: Inverts critical control flow, causing:
- Wrong branch taken (return None when should return Console)
- Wrong behavior flag (auto-checkout instead of staying on current branch)
- Incorrect error handling

**Estimated Count**: ~20-30 mutants

**Test Strategy**: 
- Test console resolution with None console (should create new one)
- Test console resolution with provided console (should return it)
- Test respect_current flag behavior (branches differ case)
- Test subprocess return code checking (== 0 vs != 0)

---

### 3. **Subprocess Argument Mutations** - Command Breaker
**Pattern**: subprocess.run() arguments removed or changed to None
**Examples**:
- `subprocess.run(cmd, ...)` → `subprocess.run(None, ...)` (run_command_5)
- `capture_output=capture` → removed (run_command_15)
- `cwd=repo_path` → `cwd=None` (get_current_branch_10)
- `cwd=str(cwd) if cwd else None` → removed (run_command_20)

**Why Killable**: Breaks git command execution:
- None command causes TypeError
- Missing capture_output means stdout/stderr not captured
- Wrong cwd means git commands run in wrong directory

**Estimated Count**: ~40-50 mutants

**Test Strategy**:
- Test run_command with actual commands and capture=True
- Test git operations with specific cwd paths
- Test command execution with different subprocess options
- Verify captured output is not empty when expected

---

### 4. **String Literal Mutations** - Git Command Breaker
**Pattern**: String constants changed (XX prefix/suffix)
**Examples**:
- `remote_name: str = "origin"` → `remote_name: str = "XXoriginXX"` (has_remote_1)
- `"git", "symbolic-ref"` → `"git", "XXsymbolic-refXX"` (resolve_primary_branch_20)
- `"kitty-specs"` → `"KITTY-SPECS"` (resolve_target_branch_15)
- `"exclude"` → `"EXCLUDE"` (exclude_from_git_index_10)

**Why Killable**: Changes git command arguments or file paths:
- Wrong remote name ("XXoriginXX" instead of "origin")
- Invalid git subcommand ("XXsymbolic-refXX")
- Wrong case-sensitive path components

**Estimated Count**: ~25-35 mutants

**Test Strategy**:
- Test has_remote with default "origin" remote
- Test resolve_primary_branch with symbolic-ref command
- Test path construction for meta.json and exclude files
- Test common branch names (main, master, develop)

---

### 5. **Default Parameter Mutations** - Edge Case Breaker
**Pattern**: Default values changed in function signatures
**Examples**:
- `quiet: bool = False` → `quiet: bool = True` (init_git_repo_1)
- `respect_current: bool = True` → `respect_current: bool = False` (resolve_target_branch_1)
- `remote_name: str = "origin"` → `remote_name: str = "XXoriginXX"` (has_remote_1)

**Why Killable**: Changes default behavior:
- Suppresses output when should be shown
- Auto-checkout when should stay on current branch
- Checks wrong remote by default

**Estimated Count**: ~15-20 mutants

**Test Strategy**:
- Test functions with default parameters (no explicit args)
- Verify quiet=False shows console output
- Verify respect_current=True stays on current branch
- Verify remote_name="origin" is default

---

## Equivalent Patterns Found

### 1. **Docstring Mutations** - Cosmetic
**Rationale**: Docstrings do not affect runtime behavior
**Estimated Count**: ~120-150 mutants (each function has extensive docstrings with examples)

### 2. **Type Hint Mutations** - Cosmetic
**Rationale**: Type hints are not enforced at runtime in Python
**Examples**:
- `Console | None` → various mutations
- `Path | None` → various mutations
- `Sequence[str] | str` → various mutations
**Estimated Count**: ~30-40 mutants

### 3. **Comment Mutations** - Cosmetic
**Rationale**: Comments do not affect execution
**Examples**:
- `# Primary: git branch --show-current (Git 2.22+)`
- `# Method 1: Get from origin's HEAD`
- `# Returns 0 with output like "origin/main" if tracking exists`
**Estimated Count**: ~20-30 mutants

### 4. **Parameter Name Mutations in Docstrings** - Cosmetic
**Rationale**: Parameter names in docstrings don't affect code execution
**Estimated Count**: ~15-20 mutants

---

## Recommended Tests

### Priority 1: Core Functionality Tests

#### 1. **test_run_command_basic** - Targets: None assignments, subprocess args
Test run_command with simple git command (git --version) and verify returncode, stdout captured

#### 2. **test_is_git_repo_valid** - Targets: None assignment, path resolution
Test is_git_repo with a valid git repo returns True, path resolution works

#### 3. **test_get_current_branch_basic** - Targets: None assignment, cwd parameter
Test get_current_branch returns branch name, subprocess called with correct cwd

#### 4. **test_has_remote_origin** - Targets: string literal mutation, default param
Test has_remote returns True for "origin" remote in a repo with remote configured

#### 5. **test_resolve_primary_branch_from_origin** - Targets: subprocess result, string mutation
Test resolve_primary_branch detects "main" from origin/HEAD symbolic ref

### Priority 2: Boolean Logic Tests

#### 6. **test_resolve_console_with_none** - Targets: boolean negation
Test _resolve_console(None) creates new Console instance (not returns None)

#### 7. **test_resolve_console_with_console** - Targets: boolean negation
Test _resolve_console(console) returns the provided console (not creates new one)

#### 8. **test_resolve_target_branch_respect_current_true** - Targets: boolean default, logic
Test resolve_target_branch with branches differing, respect_current=True → stays on current

#### 9. **test_resolve_target_branch_respect_current_false** - Targets: boolean default
Test resolve_target_branch with branches differing, respect_current=False → action="checkout_target"

### Priority 3: Subprocess Error Handling

#### 10. **test_run_command_with_capture** - Targets: capture_output parameter
Test run_command with capture=True returns non-empty stdout/stderr

#### 11. **test_run_command_with_cwd** - Targets: cwd parameter mutation
Test run_command with explicit cwd executes in correct directory

#### 12. **test_has_tracking_branch_with_tracking** - Targets: subprocess result None
Test has_tracking_branch returns True when branch has upstream tracking

#### 13. **test_has_tracking_branch_without_tracking** - Targets: return code check
Test has_tracking_branch returns False when no upstream tracking configured

### Priority 4: File Path and JSON Operations

#### 14. **test_exclude_from_git_index_basic** - Targets: Path construction, None assignment
Test exclude_from_git_index creates .git/info/exclude path correctly, writes patterns

#### 15. **test_resolve_target_branch_reads_meta_json** - Targets: Path construction, JSON parsing
Test resolve_target_branch reads target_branch from meta.json when it exists

#### 16. **test_init_git_repo_quiet_false** - Targets: default param, console output
Test init_git_repo with quiet=False prints console output (mocked)

---

## Git Ops Specific Patterns

### 1. **Subprocess Mocking Strategy**
- Mock `subprocess.run` to return controlled results
- Verify arguments passed (cmd, cwd, capture_output)
- Return mocked CompletedProcess with returncode, stdout, stderr

### 2. **Path Testing Strategy**
- Use pytest tmp_path fixtures for real file operations
- Initialize git repos in temp directories for integration tests
- Test path resolution (None → Path.cwd(), Path provided → used)

### 3. **Error Handling Testing**
- Test CalledProcessError handling in run_command
- Test FileNotFoundError handling (git command not found)
- Test OSError handling in file operations

### 4. **Console Mocking**
- Mock Rich Console for output verification
- Test quiet=True suppresses output
- Test quiet=False shows console prints

---

## Next Steps

1. **Implement Priority 1 tests** (should eliminate ~40-50% of killable mutants)
2. **Run mutmut again** to verify eliminated mutants
3. **Implement Priority 2-4 tests** for remaining survivors
4. **Add integration tests** with real git repos in tmp_path
5. **Re-sample survivors** to identify any additional patterns

---

## Notes

- **Equivalent mutant ratio**: Estimated ~40% (docstrings/comments/type hints)
- **High-value targets**: None assignments, subprocess arguments, boolean negations
- **Git-specific risks**: Wrong cwd, missing capture_output, wrong git commands
- **Testing approach**: Mix of mocked subprocess + real git repos in tmp_path
- **Quick wins**: Basic function tests with valid inputs will catch most subprocess mutations
- **Complex cases**: Branch resolution logic, fallback mechanisms, error handling paths
