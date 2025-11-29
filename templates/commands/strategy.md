---
description: "Define refactoring strategy and approach"
---

# /refactor.strategy Command

**Purpose**: Define the refactoring strategy, goals, patterns, and approach based on analysis.

## Input

User provides refactoring goals and approach:
- What improvement is desired
- Any specific patterns or approaches to use
- Constraints or requirements

Example: `$ARGUMENTS`

## Prerequisites

Before running this command:
- [ ] `/refactor.analyze` has been run for the target code
- [ ] Analysis document exists at `.refactor/refactorings/[###-refactor-name]/analysis.md`

## Workflow

### Step 1: Review Analysis

1. Read the analysis document
2. Understand identified issues and risks
3. Review recommended refactoring opportunities

### Step 2: Define Objectives

Based on user input and analysis:

1. **Primary Goal**: What is the main improvement?
2. **Success Criteria**: How will we measure success?
3. **Non-Goals**: What is explicitly out of scope?

### Step 3: Design Target State

1. Describe the desired end state
2. Compare with current state
3. Identify the transformation needed

### Step 4: Select Refactoring Patterns

Choose appropriate patterns from the catalog:

**Extract Patterns**:
- Extract Method
- Extract Class
- Extract Interface
- Extract Variable

**Move Patterns**:
- Move Method
- Move Field
- Move Class

**Rename Patterns**:
- Rename Method
- Rename Variable
- Rename Class

**Inline Patterns**:
- Inline Method
- Inline Variable
- Inline Class

**Restructure Patterns**:
- Replace Conditional with Polymorphism
- Replace Inheritance with Delegation
- Replace Delegation with Inheritance

**Simplify Patterns**:
- Consolidate Duplicate Conditional Fragments
- Decompose Conditional
- Remove Dead Code

### Step 5: Evaluate Alternatives

For each major decision:
1. List alternatives considered
2. Document pros and cons
3. Justify the chosen approach

### Step 6: Plan Backward Compatibility

If the code has consumers:
1. Identify public interface changes
2. Define migration strategy
3. Plan deprecation timeline (if applicable)

### Step 7: Identify Risks

Based on analysis:
1. List potential risks
2. Assess probability and impact
3. Define mitigation strategies

### Step 8: Define Rollback Strategy

1. Identify natural checkpoints
2. Define how to undo each phase
3. Plan for full rollback if needed

### Step 9: Define Phases

Break the refactoring into manageable phases:

1. **Preparation Phase**: Establish safety net
2. **Transformation Phases**: Core refactoring work
3. **Cleanup Phase**: Finalize and polish

For each phase, define:
- Goal
- Key activities
- Exit criteria

## Output

Generate strategy document at:
`.refactor/refactorings/[###-refactor-name]/strategy.md`

Using template from:
`.refactor/templates/strategy-template.md`

The output includes:
- Objective (goal, success criteria, non-goals)
- Current vs target state
- Selected refactoring patterns with rationale
- Alternative approaches considered
- Backward compatibility plan
- Risk mitigation strategies
- Rollback strategy
- Phase breakdown

## Next Step

After strategy is complete, use `/refactor.plan` to create a detailed implementation plan.

## Constitution Check

Before proceeding, verify:
- [ ] Strategy serves clear goal (Principle V: Strategy Over Tactics)
- [ ] Behavior preservation addressed (Principle II: Behavior Preservation)
- [ ] Incremental phases defined (Principle III: Incremental Transformation)
- [ ] Backward compatibility considered (Principle VI: Backward Compatibility)
- [ ] Simplest approach chosen (Principle VII: Simplicity)
