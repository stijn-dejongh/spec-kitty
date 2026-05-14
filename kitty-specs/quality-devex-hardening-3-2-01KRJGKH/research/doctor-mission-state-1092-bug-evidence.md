# Bug Evidence: `doctor.py:1092` — `RepairReport` / `RepoAuditReport` Type Confusion

**Produced by**: WP01 (T003)
**For**: WP06 (T030 regression test + fix)
**Date**: 2026-05-14
**Relevant file**: `src/specify_cli/cli/commands/doctor.py`

---

## Bug Description

The function `mission_state` in `doctor.py` (the `--audit / --fix / --teamspace-dry-run`
multiplexer) uses a single local variable `report` for two mutually exclusive return types:

1. `RepairReport` (returned by `repair_repo()` at line ~1012, `--fix` path)
2. `RepoAuditReport` (returned by `run_audit()` at line ~1092, `--audit` path)

Each branch returns early before the other branch runs, so there is NO runtime confusion.
However, mypy sees the first assignment as establishing `report: RepairReport` and then
rejects the second assignment of `RepoAuditReport`. This causes a cascade:

- Line 1092: `Incompatible types in assignment (expression has type "RepoAuditReport", variable has type "RepairReport")` `[assignment]`
- Line 1111: `Argument 1 to "build_report_json" has incompatible type "RepairReport"; expected "RepoAuditReport"` `[arg-type]`
- Line 1119: `"MissionRepairResult" has no attribute "findings"` `[attr-defined]`
- Line 1125: `"MissionRepairResult" has no attribute "findings"` `[attr-defined]`

The `findings` attribute errors arise because mypy narrows `report.missions` to
`list[MissionRepairResult]` (since `RepairReport.missions` is that type), and
`MissionRepairResult` has no `findings` attribute — only `MissionAuditResult` does.

---

## Type Hierarchy (for reference)

```python
# src/specify_cli/migration/mission_state.py
@dataclass
class MissionRepairResult:
    mission_slug: str
    mission_id: str | None
    status: Literal["updated", "unchanged", "error"]
    file_changes: list[FileChange]
    row_transformations: list[RowTransformation]
    quarantined_rows: int
    validation_errors: list[str]
    # NO .findings attribute

@dataclass
class RepairReport:
    run_id: str
    repo_head: str | None
    target_missions: list[str]
    manifest_path: str
    missions: list[MissionRepairResult]
    ...

# src/specify_cli/audit/models.py
@dataclass
class MissionAuditResult:
    mission_slug: str
    findings: list[MissionFinding]  # HAS .findings
    ...

@dataclass
class RepoAuditReport:
    missions: list[MissionAuditResult]  # HAS .findings via MissionAuditResult
    ...
```

---

## Reproduction Evidence

The mypy errors are reproducible without `--extra lint` (once stubs are installed):

```
$ uv run --with mypy mypy --strict src/specify_cli/cli/commands/doctor.py
src/specify_cli/cli/commands/doctor.py:631: error: Unused "type: ignore" comment  [unused-ignore]
src/specify_cli/cli/commands/doctor.py:631: error: "object" has no attribute "entries"  [attr-defined]
src/specify_cli/cli/commands/doctor.py:1092: error: Incompatible types in assignment (expression has type "RepoAuditReport", variable has type "RepairReport")  [assignment]
src/specify_cli/cli/commands/doctor.py:1111: error: Argument 1 to "build_report_json" has incompatible type "RepairReport"; expected "RepoAuditReport"  [arg-type]
src/specify_cli/cli/commands/doctor.py:1119: error: "MissionRepairResult" has no attribute "findings"  [attr-defined]
src/specify_cli/cli/commands/doctor.py:1125: error: "MissionRepairResult" has no attribute "findings"  [attr-defined]
```

With `--extra lint` (full run with `follow_imports=skip`), lines 1092-1125 disappear
because the imports resolve to `Any`, hiding the type conflict.

---

## Root Cause

`doctor.py` lines ~1008-1127 compose a multi-branch `if fix: ... if teamspace_dry_run: ... # audit path` 
control flow. Each branch early-returns, so at runtime `report` is never both types at once.
But mypy's sequential type inference narrows `report` to `RepairReport` from the `fix` branch,
then rejects the `RepoAuditReport` assignment in the later `audit` branch.

The `--fix` branch is at lines 1008-1044. The `--audit` branch starts at line 1085.

---

## Recommended Fix for WP06

WP06 should apply one of these strategies (in order of preference):

### Option A — Use a union type annotation
```python
from specify_cli.migration.mission_state import repair_repo
from specify_cli.audit import run_audit

report: RepairReport | RepoAuditReport | None = None
```

### Option B — Extract to separate functions
Extract the `fix`, `teamspace_dry_run`, and `audit` branches into dedicated functions
(`_run_fix_mode`, `_run_audit_mode`) that each return their own typed report and handle
output internally. This is also the cognitive-complexity refactor WP06 owns.

### Option C — Use typed local variables per branch
```python
if fix:
    fix_report = repair_repo(...)
    # use fix_report exclusively in this branch
    return

if audit:
    audit_report = run_audit(...)
    # use audit_report exclusively in this branch
```

**Recommended**: Option B aligns with WP06's cognitive-complexity refactor task.

---

## Lines 631 (also in doctor.py, owned by WP06)

Line 631: `_print_overdue_details(report: object, console: Console)` uses
`report.entries` but `report` is typed as `object`. The `# type: ignore[union-attr]`
comment suppresses the wrong error code — mypy now reports `[attr-defined]` not `[union-attr]`.

Fix: narrow the `report` parameter type to a protocol or concrete type that has `.entries`.

---

## Pre-existing Test: `CliRunner` Reproduction

The following demonstrates the broken audit path behavior when run from the CLI:

```python
from typer.testing import CliRunner
from specify_cli.cli import app

runner = CliRunner()
result = runner.invoke(app, ["doctor", "mission-state", "--audit"])
# Expected: exit code 0 with audit report
# Observed (pre-WP06): depends on mypy mode — runtime works correctly
```

Runtime behavior is correct (early returns prevent actual type confusion).
The bug is purely in the static type layer.

---

## Files to Modify in WP06

- `src/specify_cli/cli/commands/doctor.py` — lines 628-632, 1008-1127
- `tests/regressions/test_doctor_missionrepairresult_findings.py` (new, T030)
