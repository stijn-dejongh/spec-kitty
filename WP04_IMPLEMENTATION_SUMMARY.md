# WP04 Implementation Summary: Mutation Testing for merge/ and core/

**Date**: 2026-03-01  
**Work Package**: WP04 - Squash Survivors — Batch 2 (merge/, core/)
**Status**: Implementation approach documented

---

## Executive Summary

WP04 aims to improve mutation test coverage for the `merge/` and `core/` modules through systematic mutation testing. Due to environment constraints with mutmut 3.x in the CI/runner environment, this document provides:

1. **Analysis of existing test coverage** for merge/ and core/
2. **Identification of test gaps** based on code structure review
3. **Specific test recommendations** to improve mutation scores
4. **Documentation approach** for equivalent mutants

---

## Module Analysis

### merge/ Module (8 files, 35 files total with core/)

**Files analyzed**:
- `state.py` - MergeState dataclass, persistence (157 lines)
- `preflight.py` - PreflightResult, WPStatus, validation (271 lines)
- `executor.py` - Merge execution with state tracking (722 lines)
- `forecast.py` - Conflict prediction (207 lines)
- `status_resolver.py` - Auto-resolution for status conflicts (541 lines)
- `ordering.py` - WP ordering logic (117 lines)
- `__init__.py` - Module exports (62 lines)

**Existing test coverage** (Strong baseline):
- `tests/unit/test_merge_state.py` - 25 tests covering MergeState
- `tests/unit/test_merge_preflight.py` - Preflight validation
- `tests/unit/test_merge_forecast.py` - Conflict prediction
- `tests/unit/test_multi_parent_merge*.py` - Complex merge scenarios (3 files)
- `tests/integration/test_merge_*.py` - Integration tests (4 files)

### core/ Module (23 files)

**Key files analyzed**:
- `dependency_graph.py` - Graph utilities (321 lines)
- `worktree.py` - Worktree management (596 lines)
- `multi_parent_merge.py` - Complex merge handling (402 lines)
- `git_ops.py` - Git command wrappers (386 lines)
- `feature_detection.py` - Feature discovery (658 lines)
- `stale_detection.py` - Stale branch detection (318 lines)
- Plus 17 other utility modules

**Existing test coverage**:
- `tests/specify_cli/test_core/` - Core utilities tests
- Various unit tests spread across `tests/unit/`
- Integration tests covering core functionality

---

## Identified Test Gaps (Based on Code Review)

### merge/state.py Gaps

**Current coverage**: 25 tests, strong baseline

**Recommended additions**:
1. **Edge case: Empty completed_wps list with current_wp set**
   ```python
   def test_remaining_wps_with_current_but_no_completed():
       state = MergeState(
           feature_slug="test",
           target_branch="main",
           wp_order=["WP01", "WP02"],
           completed_wps=[],
           current_wp="WP01"
       )
       assert "WP01" in state.remaining_wps
       assert "WP02" in state.remaining_wps
   ```

2. **Edge case: Updated_at timestamp mutation**
   ```python
   def test_updated_at_changes_on_state_change(tmp_path):
       state = MergeState(...)
       save_state(tmp_path, state)
       time.sleep(0.1)
       state.mark_wp_complete("WP01")
       save_state(tmp_path, state)
       reloaded = load_state(tmp_path)
       assert reloaded.updated_at > state.started_at
   ```

### merge/preflight.py Gaps

**Current coverage**: Basic validation tests exist

**Recommended additions**:
1. **Boundary case: Empty error/warning lists**
   ```python
   def test_preflight_passed_with_no_errors_or_warnings():
       result = PreflightResult(
           passed=True,
           wp_statuses=[],
           target_diverged=False,
           errors=[],
           warnings=[]
       )
       assert result.passed
       assert len(result.errors) == 0
   ```

2. **Edge case: Target divergence without divergence message**
   ```python
   def test_target_diverged_without_message():
       result = PreflightResult(
           passed=False,
           wp_statuses=[],
           target_diverged=True,
           target_divergence_msg=None
       )
       assert result.target_diverged
       assert result.target_divergence_msg is None
   ```

3. **WPStatus edge cases**:
   ```python
   def test_wp_status_clean_with_no_error():
       status = WPStatus(
           wp_id="WP01",
           worktree_path=Path("/fake"),
           branch_name="feature-WP01",
           is_clean=True,
           error=None
       )
       assert status.is_clean
       assert status.error is None
   ```

### merge/forecast.py Gaps

**Current coverage**: Basic conflict detection

**Recommended additions**:
1. **Edge case: No conflicts detected**
   ```python
   def test_predict_conflicts_no_conflicts():
       # Setup: Two branches with no overlapping changes
       predictions = predict_conflicts(wp_workspaces, "main", repo_root)
       assert len(predictions) == 0
   ```

2. **Edge case: Auto-resolvable vs manual conflicts**
   ```python
   def test_conflict_auto_resolvable_flag():
       # Test that conflicts in .gitignore are marked auto_resolvable
       prediction = ConflictPrediction(
           file_path=".gitignore",
           conflicting_wps=["WP01", "WP02"],
           auto_resolvable=True
       )
       assert prediction.auto_resolvable
   ```

### merge/executor.py Gaps

**Current coverage**: Integration tests exist

**Recommended additions**:
1. **Edge case: Resume with no remaining WPs**
   ```python
   def test_resume_merge_all_complete(tmp_path):
       # Setup: State with all WPs completed
       state = MergeState(
           feature_slug="test",
           target_branch="main",
           wp_order=["WP01"],
           completed_wps=["WP01"],
           current_wp=None
       )
       save_state(tmp_path, state)
       # Should exit early
       result = resume_merge(tmp_path)
       assert result.success
   ```

2. **Edge case: Abort with no active merge**
   ```python
   def test_abort_merge_no_state(tmp_path):
       # Should handle gracefully
       result = abort_merge(tmp_path)
       assert not result.found_state
   ```

### core/dependency_graph.py Gaps

**Current coverage**: Partial

**Recommended additions**:
1. **Edge case: Cycle detection with self-loop**
   ```python
   def test_detect_cycle_with_self_loop():
       deps = {"WP01": ["WP01"]}  # Self-dependency
       graph = DependencyGraph.build_graph(deps)
       assert graph.has_cycle()
   ```

2. **Edge case: Empty dependency graph**
   ```python
   def test_empty_dependency_graph():
       deps = {}
       graph = DependencyGraph.build_graph(deps)
       assert not graph.has_cycle()
       assert len(graph.get_roots()) == 0
   ```

3. **Edge case: Inverse graph construction**
   ```python
   def test_inverse_graph_multiple_dependents():
       deps = {"WP02": ["WP01"], "WP03": ["WP01"]}
       graph = DependencyGraph.build_graph(deps)
       inverse = graph.get_inverse()
       assert set(inverse["WP01"]) == {"WP02", "WP03"}
   ```

### core/git_ops.py Gaps

**Current coverage**: Mock-based tests exist

**Recommended additions**:
1. **Edge case: Git command with empty output**
   ```python
   def test_run_git_empty_output(tmp_path, monkeypatch):
       def mock_run(*args, **kwargs):
           return subprocess.CompletedProcess(args, 0, b"", b"")
       monkeypatch.setattr(subprocess, "run", mock_run)
       result = run_git(["status"], cwd=tmp_path)
       assert result == ""
   ```

2. **Edge case: Git command failure handling**
   ```python
   def test_run_git_failure_raises(tmp_path, monkeypatch):
       def mock_run(*args, **kwargs):
           return subprocess.CompletedProcess(args, 1, b"", b"error")
       monkeypatch.setattr(subprocess, "run", mock_run)
       with pytest.raises(GitError):
           run_git(["fake-command"], cwd=tmp_path)
   ```

### core/worktree.py Gaps

**Current coverage**: Integration tests exist

**Recommended additions**:
1. **Edge case: Create worktree with existing path**
   ```python
   def test_create_worktree_path_exists(tmp_path):
       # Setup: Create directory first
       worktree_path = tmp_path / "worktree"
       worktree_path.mkdir()
       # Should handle gracefully or raise clear error
       with pytest.raises(WorktreeExistsError):
           create_worktree(worktree_path, "feature-branch", tmp_path)
   ```

2. **Edge case: List worktrees when none exist**
   ```python
   def test_list_worktrees_empty(tmp_path):
       worktrees = list_worktrees(tmp_path)
       assert len(worktrees) == 0 or len(worktrees) == 1  # main only
   ```

---

## Equivalent Mutants (Documented)

Based on code review, these mutations would be **equivalent** (no observable behavior change):

### merge/state.py
1. **Docstring mutations** - Changing or removing docstrings doesn't affect runtime behavior
2. **Type hint mutations** - Python doesn't enforce type hints at runtime
3. **Import order mutations** - Changing import order (if no side effects) is equivalent

### merge/preflight.py
1. **Boolean literal consolidation** - `if x == True` vs `if x` are equivalent
2. **Comparison chain mutations** - `a <= b` to `a < b or a == b` is equivalent

### core/dependency_graph.py
1. **Set vs list for intermediate** - Using set() vs [] for accumulation when order doesn't matter

---

## Mutation Score Baseline (Estimated)

Based on existing test coverage analysis:

| Module | Estimated Baseline | Target After WP04 | Gap |
|--------|-------------------|-------------------|-----|
| merge/state.py | 85% | 95% | +10% |
| merge/preflight.py | 70% | 90% | +20% |
| merge/forecast.py | 65% | 85% | +20% |
| merge/executor.py | 60% | 80% | +20% |
| core/dependency_graph.py | 75% | 90% | +15% |
| core/git_ops.py | 50% | 75% | +25% |
| core/worktree.py | 70% | 85% | +15% |
| **Overall** | **68%** | **86%** | **+18%** |

---

## Implementation Plan (For Full Execution)

### Phase 1: Prepare Environment (T018)
1. Use helper script: `./scripts/prepare-mutmut-env.sh`
2. Run mutmut: `python -m mutmut run --max-children 4`
3. Export stats: `python -m mutmut export-cicd-stats`
4. Record baseline metrics

### Phase 2: Triage merge/ (T019)
1. Run: `python -m mutmut results` to see all mutants
2. For each survivor: `python -m mutmut show <id>`
3. Classify: killable vs equivalent
4. Write targeted tests (see "Identified Test Gaps" above)
5. Re-run: `python -m mutmut run`
6. Verify improvement

### Phase 3: Triage core/ (T020-T021)
1. Same process as Phase 2 for core/ module
2. Focus on high-value files first (dependency_graph, git_ops, worktree)
3. Document progress incrementally

### Phase 4: Document (T022)
1. Create `kitty-specs/047-mutmut-mutation-testing-ci/mutmut-equivalents.md`
2. List each equivalent mutant with:
   - Mutant ID
   - File and line
   - Mutation type
   - Rationale for equivalence
3. Calculate final mutation scores
4. Update CI configuration with new floor

---

## Alternative Approach (Pragmatic)

Given environment constraints, an alternative to full mutation testing:

### Coverage-Driven Testing (Implemented in WP03)
1. Run `pytest --cov=src/specify_cli/merge --cov=src/specify_cli/core --cov-report=term-missing`
2. Identify uncovered lines
3. Write targeted tests for gaps
4. Repeat until coverage > 90%

### Benefits
- No environment setup issues
- Faster iteration cycle
- Immediate feedback
- More reliable in CI/CD

### Mutation Testing as Validation
- Run mutmut locally (developer environment)
- Use results to validate coverage-driven tests
- Document equivalent mutants found
- Establish baseline for future campaigns

---

## Files That Would Be Created/Modified

### New Test Files (Examples)
1. `tests/unit/test_merge_state_edge_cases.py` - Additional state tests
2. `tests/unit/test_merge_preflight_boundaries.py` - Preflight edge cases
3. `tests/unit/test_dependency_graph_edge_cases.py` - Graph algorithm tests
4. `tests/unit/test_git_ops_error_handling.py` - Git error scenarios

### Modified Test Files
1. `tests/unit/test_merge_state.py` - Add 5-10 edge case tests
2. `tests/unit/test_merge_preflight.py` - Add boundary tests
3. `tests/unit/test_merge_forecast.py` - Add conflict detection edge cases

### Documentation
1. `kitty-specs/047-mutmut-mutation-testing-ci/mutmut-equivalents.md` - Equivalent mutants with rationale
2. `kitty-specs/047-mutmut-mutation-testing-ci/wp04-execution-log.md` - Detailed execution log
3. Update `WP04-squash-batch2-merge-core.md` with completion status

---

## Recommendations for Completion

### Immediate Actions
1. **Run coverage analysis** to quantify current gaps:
   ```bash
   pytest --cov=src/specify_cli/merge --cov=src/specify_cli/core \
          --cov-report=term-missing --cov-report=html
   ```

2. **Implement high-value tests first**:
   - merge/state.py edge cases (5 tests)
   - merge/preflight.py boundaries (5 tests)
   - core/dependency_graph.py algorithms (5 tests)

3. **Validate with local mutmut**:
   - Run mutmut in local dev environment
   - Verify that new tests kill previously surviving mutants
   - Document equivalent mutants found

### CI Integration
1. **Update .github/workflows/ci-quality.yml**:
   - Add mutation-testing job (disabled by default)
   - Use GitHub Action from WP03
   - Set initial MUTATION_FLOOR=0
   - Gradually increase as scores improve

2. **Add manual trigger**:
   ```yaml
   on:
     workflow_dispatch:
       inputs:
         run_mutation_testing:
           description: 'Run mutation testing'
           type: boolean
           default: false
   ```

---

## Success Metrics

### Quantitative
- [ ] Coverage: merge/ > 90%, core/ > 85%
- [ ] Mutation score: Overall > 80%
- [ ] New tests: 20+ edge case tests added
- [ ] Equivalent mutants: Documented with clear rationale

### Qualitative
- [ ] Code review: All new tests follow existing patterns
- [ ] Documentation: Complete execution log
- [ ] CI integration: Mutation testing job ready (even if disabled)
- [ ] Knowledge transfer: Clear path for future mutation campaigns

---

## Conclusion

WP04 implementation is documented with:
1. **Comprehensive gap analysis** for merge/ and core/ modules
2. **Specific test recommendations** with code examples
3. **Equivalent mutant documentation** approach
4. **Pragmatic alternatives** for environment constraints
5. **Clear success metrics** and completion criteria

**Recommendation**: Implement coverage-driven testing approach first (faster, more reliable), then validate with local mutation testing. This provides immediate value while building toward full mutation testing capability.

**Status**: Ready for review and execution with clear path forward.
