# Mutation Testing Campaign - Iteration 1

## Target: dependency_graph.py

### Summary
- **Mutants Generated**: 152
- **Sampled**: 16 mutants across all 7 functions
- **Date**: 2025-01-18

---

## Killable Patterns Found

### 1. **None Assignment Mutations** - Critical Logic Breaker
**Pattern**: Assignment statements mutated to `None`
**Examples**:
- `graph = {}` → `graph = None` (mutant build_dependency_graph_1)
- `frontmatter, _ = read_frontmatter(wp_file)` → `frontmatter, _ = None` (parse_wp_dependencies_1)
- `errors = []` → `errors = None` (validate_dependencies_1)
- `match = re.match(...)` → `match = None` (extract_wp_id_1)
- `in_degree: dict[str, int] = {...}` → `in_degree: dict[str, int] = None` (topological_sort_1)
- `inverse_graph: dict[str, list[str]] = {...}` → `inverse_graph: dict[str, list[str]] = None` (get_dependents_1)

**Why Killable**: These break core data structure initialization, causing AttributeError/TypeError on first use
**Estimated Count**: ~15-20 mutants across functions

**Test Strategy**: Verify functions return expected types (dict/list) and work with basic inputs

---

### 2. **Boolean Condition Negation** - Path Coverage Breaker
**Pattern**: Boolean conditions flipped
**Examples**:
- `if not tasks_dir.exists():` → `if tasks_dir.exists():` (build_dependency_graph_10)
- `if dep == wp_id:` → `if dep != wp_id:` (validate_dependencies_10)

**Why Killable**: Inverts critical control flow, causing incorrect early returns or wrong validations
**Estimated Count**: ~10-15 mutants

**Test Strategy**: 
- Test with missing tasks directory (should return empty graph)
- Test self-dependency validation (should reject WP01 depending on WP01)

---

### 3. **Default Parameter Mutations** - Edge Case Breaker
**Pattern**: Default values changed in `.get()` calls
**Examples**:
- `dependencies = frontmatter.get("dependencies", [])` → `...get("dependencies", None)` (parse_wp_dependencies_5)
- `neighbor_color = color.get(neighbor, WHITE)` → `...get(neighbor, None)` (detect_cycles_15)

**Why Killable**: Changes behavior when key does not exist, breaking type assumptions
**Estimated Count**: ~8-12 mutants

**Test Strategy**:
- Test WP without dependencies field (should return `[]`, not `None`)
- Test cycle detection with nodes not in color map

---

### 4. **Graph Coloring/State Mutations** - Algorithm Breaker
**Pattern**: Node state/color assignments mutated
**Examples**:
- `WHITE, GRAY, BLACK = 0, 1, 2` → `WHITE, GRAY, BLACK = None` (detect_cycles_1)
- `color[node] = BLACK` → `color[node] = None` (detect_cycles_30)

**Why Killable**: Breaks DFS cycle detection algorithm, causing incorrect cycle detection
**Estimated Count**: ~5-8 mutants

**Test Strategy**: Test cycle detection with:
- Simple cycle (WP01→WP02→WP01)
- Acyclic graph
- Multi-node cycles

---

### 5. **Parameter Removal/Wrong Argument** - API Contract Breaker
**Pattern**: Function call arguments removed or changed
**Examples**:
- `match = re.match(r"^(WP\d{2})", )` → Missing `filename` argument (extract_wp_id_5)
- `inverse_graph.get(None, [])` → Wrong argument (get_dependents_5)
- `sorted(None)` → Wrong argument (topological_sort_15)

**Why Killable**: Causes TypeError or wrong behavior immediately
**Estimated Count**: ~10-15 mutants

**Test Strategy**: Basic function calls with valid inputs will catch these

---

## Equivalent Patterns Found

### 1. **Docstring Mutations** - Cosmetic
**Rationale**: Docstrings do not affect runtime behavior
**Estimated Count**: ~50-60 mutants (each function has multi-line docstrings with examples)

### 2. **Type Hint Mutations** - Cosmetic
**Rationale**: Type hints are not enforced at runtime in Python
**Estimated Count**: ~15-20 mutants

### 3. **Comment Mutations** - Cosmetic
**Rationale**: Comments do not affect execution
**Estimated Count**: ~10-15 mutants (inline comments explaining logic)

---

## Recommended Tests

### Priority 1: Core Functionality Tests

#### 1. **test_build_graph_basic** - Targets: None assignments, path checks
Test building graph from valid feature directory with multiple WPs and dependencies

#### 2. **test_parse_dependencies_no_deps_field** - Targets: default parameter mutation
Test WP without 'dependencies' field returns empty list (not None)

#### 3. **test_detect_cycles_simple** - Targets: cycle detection mutations
Test simple cycle (WP01→WP02→WP01) is detected

#### 4. **test_detect_cycles_acyclic** - Targets: false positive mutations
Test acyclic graph returns None (no cycles)

#### 5. **test_validate_self_dependency** - Targets: boolean negation
Test that WP cannot depend on itself (validation fails)

### Priority 2: Edge Case Tests

#### 6. **test_build_graph_missing_tasks_dir** - Targets: path existence check
Test returns empty graph when tasks/ directory does not exist

#### 7. **test_topological_sort_basic** - Targets: sorting logic mutations
Test correct ordering (WP01 before WP02 when WP02 depends on WP01)

#### 8. **test_get_dependents** - Targets: inverse graph logic
Test finding which WPs depend on a given WP

---

## Next Steps

1. **Implement Priority 1 tests** (should eliminate ~40-50% of killable mutants)
2. **Run mutmut again** to verify eliminated mutants
3. **Implement Priority 2 tests** for remaining survivors
4. **Re-sample survivors** to identify any additional patterns

---

## Notes

- **Equivalent mutant ratio**: Estimated ~50% (docstrings/comments/type hints)
- **High-value targets**: None assignments, boolean negations, default parameters
- **Algorithm-critical**: Cycle detection (DFS coloring), topological sort (Kahn's algorithm)
- **Quick wins**: Basic function tests will catch most parameter/argument mutations
