---
description: "Analyze codebase for refactoring opportunities"
---

# /refactor.analyze Command

**Purpose**: Analyze target code to understand structure, identify code smells, and assess refactoring risk.

## Input

User provides a description of what to analyze:
- Target code location (file, module, class, or feature)
- Specific concerns or focus areas (optional)

Example: `$ARGUMENTS`

## Workflow

### Step 1: Locate Target Code

1. Parse user input to identify target code location
2. Read and understand the target files
3. Identify the scope of analysis (single file, module, or feature)

### Step 2: Structure Analysis

Examine the target code for:

1. **Size Metrics**
   - Lines of code
   - Number of classes/modules
   - Number of methods/functions
   - Cyclomatic complexity

2. **Dependency Mapping**
   - Internal dependencies (what it uses)
   - External dependencies (libraries, services)
   - Dependents (what uses it)

3. **History Analysis** (if git available)
   - Change frequency
   - Recent modifications
   - Multiple authors

### Step 3: Code Smell Detection

Identify common code smells:

**Bloaters**:
- Long Method (>20 lines)
- Large Class (>200 lines)
- Long Parameter List (>3 parameters)
- Primitive Obsession
- Data Clumps

**Object-Orientation Abusers**:
- Switch Statements
- Refused Bequest
- Parallel Inheritance Hierarchies

**Change Preventers**:
- Divergent Change (one class changed for multiple reasons)
- Shotgun Surgery (one change affects many classes)
- Parallel Inheritance

**Dispensables**:
- Dead Code
- Speculative Generality
- Duplicate Code
- Comments (excessive)

**Couplers**:
- Feature Envy
- Inappropriate Intimacy
- Message Chains
- Middle Man

### Step 4: Test Coverage Assessment

1. Identify existing tests for target code
2. Assess coverage level (if tools available)
3. Evaluate test quality (focus, reliability)
4. Identify coverage gaps

### Step 5: Risk Assessment

Evaluate refactoring risk based on:

1. **Complexity**: How complex is the code?
2. **Coverage**: Is behavior protected by tests?
3. **Dependencies**: How many things depend on this?
4. **Volatility**: How often does this change?
5. **Understanding**: How well is this understood?

### Step 6: Generate Recommendations

Based on analysis:

1. Identify high-priority refactoring opportunities
2. List prerequisites (e.g., add tests)
3. Suggest refactoring patterns
4. Estimate effort levels

## Output

Generate analysis document at:
`.refactor/refactorings/[###-refactor-name]/analysis.md`

Using template from:
`.refactor/templates/analyze-template.md`

The output includes:
- Executive summary
- Code structure analysis
- Dependency mapping
- Code smell catalog
- Test coverage assessment
- Risk assessment
- Refactoring opportunities
- Recommendations

## Next Step

After analysis is complete, use `/refactor.strategy` to define the refactoring approach.

## Constitution Check

Before proceeding, verify:
- [ ] Analysis is thorough (Principle I: Analysis-First)
- [ ] Safety baseline documented (Principle IV: Test-Driven Safety)
