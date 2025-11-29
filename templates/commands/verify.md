---
description: "Verify refactoring success and behavior preservation"
---

# /refactor.verify Command

**Purpose**: Verify that the refactoring is complete, behavior is preserved, and goals are met.

## Input

Uses all existing refactoring documents. Optional parameters:
- Specific verification focus
- Additional checks to perform

Example: `$ARGUMENTS`

## Prerequisites

Before running this command:
- [ ] `/refactor.execute` has completed all tasks
- [ ] All tests pass
- [ ] Code is in stable state

## Workflow

### Step 1: Test Verification

1. **Run full test suite**
   ```bash
   # Run all tests
   pytest  # or appropriate test command
   ```

2. **Verify no regressions**
   - All pre-existing tests pass
   - No new failures
   - No flaky tests

3. **Check coverage**
   - Coverage maintained or improved
   - No new uncovered critical paths

### Step 2: Behavior Comparison

1. **Compare with baseline**
   - Document behavior before/after
   - Verify external behavior unchanged
   - Check edge cases

2. **Integration verification**
   - Dependent code still works
   - APIs behave as expected
   - No broken contracts

### Step 3: Code Quality Metrics

Measure improvement:

1. **Complexity metrics**
   - Cyclomatic complexity before/after
   - Method length before/after
   - Class size before/after

2. **Coupling metrics**
   - Dependencies before/after
   - Coupling level before/after

3. **Cohesion metrics**
   - Single responsibility adherence
   - Module cohesion

### Step 4: Goal Verification

Check success criteria from strategy:

| Criterion | Target | Actual | Status |
|-----------|--------|--------|--------|
| [SC-001] | [target] | [actual] | ✓/✗ |
| [SC-002] | [target] | [actual] | ✓/✗ |

### Step 5: Documentation Verification

1. **Code documentation**
   - Docstrings updated
   - Comments reflect new structure
   - Type hints accurate

2. **External documentation**
   - README updated (if needed)
   - API docs updated (if needed)
   - Design docs updated

### Step 6: Generate Report

Create verification summary:

1. **Test results**
   - All tests passed: Yes/No
   - Coverage: X%
   - Regressions: None/List

2. **Quality improvements**
   - Complexity: Reduced by X%
   - Lines of code: Changed from X to Y
   - Coupling: Improved/Same/Worse

3. **Goals met**
   - Success criteria status
   - Any criteria not met

4. **Recommendations**
   - Follow-up actions
   - Future improvements
   - Known limitations

## Output

Generate verification document at:
`.refactor/refactorings/[###-refactor-name]/verification.md`

The output includes:
- Test verification results
- Behavior comparison
- Code quality metrics (before/after)
- Goal verification status
- Documentation status
- Overall assessment
- Recommendations

## Verification Checklist

### Functional Verification

- [ ] All existing tests pass
- [ ] No regression in functionality
- [ ] Edge cases handled correctly
- [ ] Integration points work

### Structural Verification

- [ ] Code structure matches target state
- [ ] Patterns correctly applied
- [ ] No leftover scaffolding
- [ ] Clean separation of concerns

### Quality Verification

- [ ] Complexity reduced or maintained
- [ ] Coupling reduced or maintained
- [ ] Test coverage maintained or improved
- [ ] Code is more readable

### Documentation Verification

- [ ] Code comments updated
- [ ] API documentation updated
- [ ] Design documentation updated
- [ ] README updated (if needed)

## Post-Verification Actions

1. **If verification passes**:
   - Create pull request
   - Request code review
   - Merge when approved

2. **If verification fails**:
   - Identify failures
   - Determine if fixable
   - Fix issues and re-verify
   - Or rollback if unfixable

## Next Steps

After verification passes:
1. Create pull request with verification report
2. Request code review
3. Merge and deploy
4. Monitor for issues
5. Close refactoring documentation

## Constitution Final Check

- [x] Analysis completed (Principle I)
- [x] Behavior preserved (Principle II)
- [x] Incremental approach used (Principle III)
- [x] Tests ensured safety (Principle IV)
- [x] Strategy guided execution (Principle V)
- [x] Backward compatibility maintained (Principle VI)
- [x] Simplicity achieved (Principle VII)
- [x] Documentation updated (Principle VIII)
