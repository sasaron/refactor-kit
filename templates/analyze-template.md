# Refactoring Analysis: [TARGET NAME]

**Target**: `[path/to/target/code]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## Executive Summary

<!--
  Brief overview of the analysis findings.
  What is the target code? What are the main issues identified?
  What is the overall risk level for refactoring?
-->

[Summary of findings]

## Code Structure Analysis

### Overview

<!--
  High-level description of the target code:
  - Purpose and responsibility
  - Size metrics (lines, classes, methods)
  - Age and change frequency
-->

| Metric | Value |
|--------|-------|
| Lines of Code | [NUMBER] |
| Classes/Modules | [NUMBER] |
| Methods/Functions | [NUMBER] |
| Cyclomatic Complexity (avg) | [NUMBER] |
| Last Modified | [DATE] |
| Change Frequency | [high/medium/low] |

### Structure Map

<!--
  Visual or textual representation of code structure.
  Include main components and their relationships.
-->

```text
[Component diagram or text representation]
```

## Dependency Analysis

### Internal Dependencies

<!--
  What does this code depend on within the project?
-->

| Dependency | Type | Coupling Level |
|------------|------|----------------|
| [Module A] | [direct/indirect] | [high/medium/low] |
| [Module B] | [direct/indirect] | [high/medium/low] |

### External Dependencies

<!--
  What external libraries or services does this code depend on?
-->

| Dependency | Version | Purpose |
|------------|---------|---------|
| [Library A] | [version] | [purpose] |

### Dependents

<!--
  What code depends on this target? (Impact of changes)
-->

| Dependent | Type | Impact Risk |
|-----------|------|-------------|
| [Module X] | [public API/internal] | [high/medium/low] |

## Code Smell Analysis

### Identified Issues

<!--
  List code smells with severity and location.
  Reference: https://refactoring.guru/refactoring/smells
-->

| ID | Code Smell | Severity | Location | Description |
|----|------------|----------|----------|-------------|
| CS-001 | [smell name] | [critical/major/minor] | [file:line] | [description] |
| CS-002 | [smell name] | [critical/major/minor] | [file:line] | [description] |

### Smell Categories

- **Bloaters**: [list any Long Method, Large Class, etc.]
- **Object-Orientation Abusers**: [list any violations]
- **Change Preventers**: [list any Divergent Change, Shotgun Surgery, etc.]
- **Dispensables**: [list any Dead Code, Speculative Generality, etc.]
- **Couplers**: [list any Feature Envy, Inappropriate Intimacy, etc.]

## Test Coverage Assessment

### Current Coverage

| Metric | Value | Status |
|--------|-------|--------|
| Line Coverage | [%] | [adequate/inadequate] |
| Branch Coverage | [%] | [adequate/inadequate] |
| Test Count | [number] | |
| Test Quality | [high/medium/low] | |

### Coverage Gaps

<!--
  Where is coverage missing or weak?
-->

| Area | Coverage | Risk |
|------|----------|------|
| [area/feature] | [%] | [high/medium/low] |

### Test Characteristics

- [ ] Tests run fast (<30 seconds)
- [ ] Tests are reliable (no flaky tests)
- [ ] Tests are independent (no order dependency)
- [ ] Tests are maintainable (clear, focused)

## Risk Assessment

### Overall Risk Level: [HIGH/MEDIUM/LOW]

### Risk Factors

| Factor | Level | Mitigation |
|--------|-------|------------|
| Complexity | [high/medium/low] | [mitigation strategy] |
| Test Coverage | [high/medium/low] | [mitigation strategy] |
| Dependencies | [high/medium/low] | [mitigation strategy] |
| Churn Rate | [high/medium/low] | [mitigation strategy] |
| Team Familiarity | [high/medium/low] | [mitigation strategy] |

### Safety Assessment

- [ ] Adequate test coverage exists
- [ ] Code is well-understood
- [ ] Dependencies are manageable
- [ ] Rollback is possible

## Refactoring Opportunities

### High Priority

<!--
  Refactorings that would have the most impact
-->

| Opportunity | Pattern | Impact | Effort | Priority |
|-------------|---------|--------|--------|----------|
| [description] | [Extract Method/Class/etc.] | [high/medium/low] | [high/medium/low] | P1 |

### Medium Priority

| Opportunity | Pattern | Impact | Effort | Priority |
|-------------|---------|--------|--------|----------|
| [description] | [pattern] | [impact] | [effort] | P2 |

### Low Priority

| Opportunity | Pattern | Impact | Effort | Priority |
|-------------|---------|--------|--------|----------|
| [description] | [pattern] | [impact] | [effort] | P3 |

## Recommendations

### Immediate Actions

1. [First action to take]
2. [Second action]

### Prerequisites for Refactoring

- [ ] [Prerequisite 1, e.g., increase test coverage]
- [ ] [Prerequisite 2, e.g., document current behavior]

### Suggested Approach

[Description of recommended refactoring approach based on analysis]

## Next Steps

Use `/refactor.strategy` to define the refactoring strategy based on this analysis.
