---
description: "Execute refactoring tasks systematically"
---

# /refactor.execute Command

**Purpose**: Systematically execute refactoring tasks while maintaining code safety.

## Input

Uses existing tasks document. Optional parameters:
- Start from specific task
- Execute specific phase only
- Dry run mode

Example: `$ARGUMENTS`

## Prerequisites

Before running this command:
- [ ] All previous commands have been run
- [ ] tasks.md exists with executable tasks
- [ ] All tests currently pass
- [ ] Feature branch created

## Workflow

### Step 1: Pre-Execution Verification

1. Verify all tests pass
2. Confirm on correct branch
3. Check for uncommitted changes
4. Document starting state

### Step 2: Load Tasks

1. Read tasks.md
2. Parse task list
3. Identify current progress
4. Plan execution order

### Step 3: Execute Tasks

For each task:

1. **Read task requirements**
   - Understand what needs to change
   - Identify affected files
   - Check prerequisites

2. **Implement change**
   - Make the code modification
   - Follow the task specification exactly
   - Keep changes minimal and focused

3. **Verify change**
   - Run relevant tests
   - Check for regressions
   - Verify code compiles/lints

4. **Commit change**
   - Create descriptive commit message
   - Reference task ID
   - Keep commits atomic

5. **Update progress**
   - Mark task complete in tasks.md
   - Note any deviations
   - Record any issues

### Step 4: Phase Checkpoints

At end of each phase:

1. Run full test suite
2. Verify phase exit criteria
3. Create phase summary
4. Decide: continue, pause, or rollback

### Step 5: Handle Failures

If tests fail:

1. **Stop immediately**
2. **Diagnose the issue**
   - Which test failed?
   - What change caused it?
   - Is this a bug or expected failure?

3. **Resolve**
   - Fix the issue, or
   - Rollback the change, or
   - Update tests if behavior change is expected

4. **Verify fix**
   - All tests pass
   - Continue execution

### Step 6: Progress Tracking

Maintain execution log:
- Tasks completed
- Time taken
- Issues encountered
- Deviations from plan

## Execution Rules

### Safety First

- Run tests after EVERY change
- Never leave code in broken state
- Commit frequently
- Keep commits reversible

### One Thing at a Time

- Complete one task before starting next
- Don't mix changes from different tasks
- Keep focus narrow

### Verify Continuously

- Tests after each change
- Full suite at checkpoints
- Manual verification for UI/behavior

### Document Everything

- Update task status
- Note any issues
- Record deviations
- Keep logs

## Output

1. **Updated tasks.md** with completed tasks marked
2. **Git commits** for each completed task
3. **Execution log** (optional, in memory or separate file)

## Commands for Common Scenarios

### Resume from Last Task

```text
/refactor.execute Continue from where we left off
```

### Execute Single Phase

```text
/refactor.execute Execute Phase 1 only
```

### Dry Run

```text
/refactor.execute Show what would be done without executing
```

### After Failure

```text
/refactor.execute Resume after fixing test failure
```

## Next Step

After all tasks are complete, use `/refactor.verify` to confirm refactoring success.

## Emergency Rollback

If refactoring must be abandoned:

1. Stop execution
2. Review rollback strategy in plan.md
3. Revert to last known good state
4. Document reasons for rollback
