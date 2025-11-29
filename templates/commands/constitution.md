---
description: "Create or update project refactoring principles and guidelines"
---

# /refactor.constitution Command

**Purpose**: Create or update the project's governing principles for refactoring.

## Input

User provides guidelines for the constitution:
- Code quality standards
- Testing requirements
- Backward compatibility rules
- Documentation standards
- Any project-specific constraints

Example: `$ARGUMENTS`

## Workflow

### Step 1: Check Existing Constitution

1. Check if `.refactor/memory/constitution.md` exists
2. If exists, read current content
3. Prepare for update or creation

### Step 2: Gather Requirements

Based on user input and project context:

1. **Identify core principles** to include
2. **Adapt principles** to project needs
3. **Add project-specific** requirements

### Step 3: Apply Default Principles

If not overridden, include these core principles:

1. **Analysis-First Principle**
   - Thorough analysis before changes
   - Map dependencies and risks

2. **Behavior Preservation (NON-NEGOTIABLE)**
   - All tests must pass
   - External behavior unchanged

3. **Incremental Transformation**
   - Small, verifiable steps
   - Reversible at each point

4. **Test-Driven Safety**
   - Adequate coverage required
   - Characterization tests for gaps

5. **Strategy Over Tactics**
   - Clear goals before action
   - Pattern selection with rationale

6. **Backward Compatibility**
   - Maintain interfaces when possible
   - Migration paths for breaking changes

7. **Simplicity Principle**
   - Simplest solution first
   - YAGNI applied

8. **Documentation and Communication**
   - Update docs with changes
   - Communicate to team

### Step 4: Customize for Project

Based on user input:

1. Add project-specific principles
2. Adjust safety requirements
3. Define governance rules
4. Set version and dates

### Step 5: Generate/Update Constitution

Write to `.refactor/memory/constitution.md`

## Output

Constitution document with:
- Core principles (with descriptions)
- Safety requirements (checklists)
- Governance rules
- Version information

## Template Location

Base template at: `memory/constitution.md`

## Usage Examples

### Create New Constitution

```text
/refactor.constitution Create principles focused on:
- High test coverage requirements (>80%)
- Strict backward compatibility
- Performance must not degrade
- All changes require code review
```

### Update Existing Constitution

```text
/refactor.constitution Update to add:
- New principle for security review
- Stricter requirements for API changes
```

### Project-Specific Constitution

```text
/refactor.constitution Create for a legacy system with:
- Emphasis on characterization testing
- Gradual modernization approach
- Strong rollback requirements
- Team communication requirements
```

## Constitution Sections

### Required Sections

1. **Core Principles**: Numbered, named principles with descriptions
2. **Safety Requirements**: Checklists for before/during/after refactoring
3. **Governance**: Rules for amendments and violations

### Optional Sections

1. **Project-Specific Constraints**
2. **Technology Standards**
3. **Performance Requirements**
4. **Security Considerations**
5. **Team Communication**

## Next Steps

After constitution is created:
1. Share with team for review
2. Get buy-in on principles
3. Begin refactoring work with `/refactor.analyze`
