# Maven Review Checks

Automated checks a reviewer should run — or verify the implementer has run — before approving Java code changes. Each tool catches a different category of defect; no single tool replaces the others.

## Build and Test

### mvn verify

Full lifecycle: compile, unit tests (Surefire), integration tests (Failsafe), packaging, and all bound quality plugins.

```bash
mvn verify
```

**What it catches:** compilation errors, failing unit and integration tests, packaging failures.
**Review signal:** if `verify` does not pass cleanly, no further review is warranted.

### mvn test

Unit tests only (Surefire). Use during development to run fast feedback loops.

```bash
mvn test
# Run a single test class:
mvn test -Dtest=OrderServiceTest
# Run a single method:
mvn test -Dtest=OrderServiceTest#processOrder_singleItem_returnsInvoiceWithId
```

**What it catches:** failing unit tests.

## Code Style

### Checkstyle

Enforces formatting and naming conventions against a configured ruleset (Google style or project-specific).

```bash
mvn checkstyle:check
```

**What it catches:** line length violations, naming convention deviations, import ordering, Javadoc presence on public APIs.
**Review signal:** style violations indicate the implementer skipped the quality gate.

### Spotless (if configured)

Enforces consistent code formatting using google-java-format.

```bash
mvn spotless:check
# Auto-fix:
mvn spotless:apply
```

**What it catches:** inconsistent indentation, brace placement, blank lines.

## Static Analysis

### SpotBugs

Bytecode-level static analysis detecting common bug patterns.

```bash
mvn spotbugs:check
```

**What it catches:** null dereferences, resource leaks, incorrect use of equals/hashCode, thread safety issues, bad practice patterns.
**Key categories:** `CORRECTNESS`, `BAD_PRACTICE`, `PERFORMANCE`, `MT_CORRECTNESS`.

### PMD

Source-level static analysis for code quality and complexity.

```bash
mvn pmd:check
```

**What it catches:** excessive complexity (cyclomatic), unused variables and imports, empty catch blocks, duplicate code (CPD), naming violations.

## Test Coverage

### JaCoCo

Measures instruction and branch coverage; fails the build if coverage falls below configured thresholds.

```bash
mvn verify   # JaCoCo report generated under target/site/jacoco/
# View summary:
open target/site/jacoco/index.html
```

**Thresholds:** check `<configuration>` in pom.xml; typical minimum is 80% instruction coverage on changed modules.
**What it catches:** uncovered branches, dead code, undertested public APIs.

## Dependency Analysis

### OWASP Dependency Check

Scans dependencies for known CVEs.

```bash
mvn org.owasp:dependency-check-maven:check
```

**What it catches:** dependencies with published CVEs. Flag any HIGH or CRITICAL findings to the architect before merging.

### Maven Enforcer

Validates build environment and dependency rules (no duplicate dependencies, required Java version, banned dependencies).

```bash
mvn enforcer:enforce
```

## Architecture Testing

### ArchUnit

Runs as a regular JUnit 5 test suite. Enforces structural rules about package dependencies, naming conventions, class visibility, and layer boundaries — violations fail the build just like any other test failure.

```bash
mvn test  # ArchUnit rules execute as part of the test phase
```

**What it catches:** package dependency cycles, classes in the wrong layer accessing forbidden packages, naming convention deviations (e.g., classes in `repository` package that do not implement a `Repository` interface), public constructors on classes that must use factories.

**Example rules:**
```java
@Test
void services_should_not_access_controllers() {
    noClasses().that().resideInAPackage("..service..")
        .should().accessClassesThat().resideInAPackage("..controller..")
        .check(importedClasses);
}

@Test
void repository_classes_should_implement_repository_interface() {
    classes().that().resideInAPackage("..repository..")
        .and().areNotInterfaces()
        .should().implement(Repository.class)
        .check(importedClasses);
}
```

**Review signal:** ArchUnit failures indicate architectural drift — new code violating layer boundaries or naming contracts established by the team.

## Summary Checklist

| Check | Command | Gate |
|-------|---------|------|
| Build + all tests | `mvn verify` | green build |
| Style | `mvn checkstyle:check` | zero violations |
| Bytecode analysis | `mvn spotbugs:check` | zero bugs |
| Source analysis | `mvn pmd:check` | zero violations |
| Coverage | `mvn verify` + JaCoCo | meets configured threshold |
| Architecture rules | `mvn test` (ArchUnit suite) | zero architectural violations |
| CVEs | `mvn dependency-check:check` | no HIGH/CRITICAL unresolved |
