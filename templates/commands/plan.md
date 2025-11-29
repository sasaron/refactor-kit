---
description: "Create detailed refactoring implementation plan"
---

# /refactor.plan Command

**Purpose**: Create a detailed implementation plan for the refactoring based on strategy.

## Input

Uses existing strategy document. Optional additional instructions:
- Additional constraints
- Timeline requirements
- Team coordination needs

Example: `$ARGUMENTS`

## Prerequisites

Before running this command:
- [ ] `/refactor.analyze` has been run
- [ ] `/refactor.strategy` has been run
- [ ] Analysis and strategy documents exist

## Workflow

### Step 1: Review Strategy

1. Read the strategy document
2. Understand goals and approach
3. Review selected patterns and phases

### Step 2: Constitution Check

Verify all constitution principles are addressed:

- [ ] Analysis completed (Principle I)
- [ ] Behavior preservation ensured (Principle II)
- [ ] Incremental steps defined (Principle III)
- [ ] Test coverage adequate (Principle IV)
- [ ] Strategy defined (Principle V)
- [ ] Backward compatibility addressed (Principle VI)
- [ ] Simplest approach chosen (Principle VII)
- [ ] Documentation plan in place (Principle VIII)

### Step 3: Document Safety Baseline

Record current state:
1. Test coverage percentage
2. Build status
3. Existing test count
4. Performance baselines (if relevant)

### Step 4: Detail Each Phase

For each phase from strategy:

1. **Break into specific changes**
   - List each refactoring move
   - Identify affected files
   - Link to relevant tests

2. **Define verification steps**
   - What tests to run
   - What to manually verify
   - What metrics to check

3. **Define exit criteria**
   - What must be true to proceed
   - What can trigger rollback

### Step 5: Map Dependencies

1. Order phases correctly
2. Identify blocking dependencies
3. Note parallel opportunities

### Step 6: Define Rollback Strategy

For each phase:
1. How to undo changes
2. Difficulty level
3. Any data considerations

### Step 7: Plan Verification

1. Test strategy for each phase
2. Performance verification
3. Integration verification

### Step 8: Define Acceptance Criteria

Overall criteria for success:
1. Functional (tests pass)
2. Structural (code quality improved)
3. Quality (metrics improved)

## Output

Generate plan document at:
`.refactor/refactorings/[###-refactor-name]/plan.md`

Using template from:
`.refactor/templates/plan-template.md`

The output includes:
- Summary
- Refactoring context (scope, safety baseline)
- Constitution check
- Project structure (docs and code)
- Implementation phases with detailed changes
- Rollback strategy
- Dependencies and risks
- Acceptance criteria

## Next Step

After plan is complete, use `/refactor.tasks` to generate executable tasks.

## Safety Gate

STOP if:
- Constitution check fails without documented exceptions
- Test coverage is below required threshold
- Critical risks without mitigation
