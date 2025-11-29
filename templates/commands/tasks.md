---
description: "Generate actionable task list from refactoring plan"
---

# /refactor.tasks Command

**Purpose**: Convert the implementation plan into a detailed, executable task list.

## Input

Uses existing plan document. Optional additional instructions:
- Task granularity preferences
- Team assignment information
- Priority adjustments

Example: `$ARGUMENTS`

## Prerequisites

Before running this command:
- [ ] `/refactor.analyze` has been run
- [ ] `/refactor.strategy` has been run
- [ ] `/refactor.plan` has been run
- [ ] Analysis, strategy, and plan documents exist

## Workflow

### Step 1: Read Planning Documents

1. Load plan.md
2. Load strategy.md
3. Load analysis.md
4. Understand the full context

### Step 2: Extract Tasks from Plan

For each phase in the plan:

1. **Preparation tasks**
   - Branch creation
   - Test verification
   - Coverage documentation
   - Characterization test creation

2. **Implementation tasks**
   - Test writing (if new structure)
   - Code changes
   - Import updates
   - Integration updates

3. **Cleanup tasks**
   - Dead code removal
   - Documentation updates
   - Final verification

### Step 3: Order Tasks

1. Respect phase dependencies
2. Order by prerequisites within phases
3. Mark parallel opportunities [P]
4. Ensure tests come before implementation

### Step 4: Add Verification Points

After each significant task group:
1. Test run commands
2. Coverage check commands
3. Checkpoint markers

### Step 5: Define Rollback Points

Mark clear rollback boundaries:
1. After each phase
2. After major structural changes
3. Document rollback method

### Step 6: Format Tasks

Each task includes:
- **ID**: Unique identifier (T001, T002, etc.)
- **[P]**: Parallel marker if applicable
- **[Phase]**: Phase identifier (P0, P1, P2, etc.)
- **Description**: What to do
- **File path**: Where to make changes
- **Verification**: How to verify

## Output

Generate tasks document at:
`.refactor/refactorings/[###-refactor-name]/tasks.md`

Using template from:
`.refactor/templates/tasks-template.md`

The output includes:
- Task format explanation
- Phase 0 (Preparation) tasks
- Phase 1+ (Implementation) tasks
- Cleanup phase tasks
- Dependencies and execution order
- Parallel opportunities
- Rollback points
- Verification commands

## Task Characteristics

### Good Tasks

- **Specific**: Clear action and location
- **Verifiable**: Can confirm completion
- **Atomic**: One logical change
- **Ordered**: Dependencies clear
- **Safe**: Doesn't break things mid-task

### Bad Tasks (Avoid)

- Vague ("improve code")
- Unverifiable ("should work better")
- Too large (multiple concerns)
- Wrong order (dependencies violated)
- Unsafe (leaves code broken)

## Next Step

After tasks are generated, use `/refactor.execute` to implement the refactoring.

## Notes

- Tasks should be small enough to complete and verify quickly
- Each task should leave the code in a working state
- Commit frequently during execution
- Mark tasks complete as you go
