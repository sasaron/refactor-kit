# Refactoring Strategy: [FEATURE NAME]

**Target**: `[path/to/target/code]`  
**Created**: [DATE]  
**Status**: Draft  
**Analysis Reference**: `[link to analysis document]`  
**Input**: User description: "$ARGUMENTS"

## Objective

### Primary Goal

<!--
  What is the main goal of this refactoring?
  Be specific and measurable.
-->

[Clear statement of what this refactoring aims to achieve]

### Success Criteria

<!--
  How will we know the refactoring is successful?
  These should be measurable and verifiable.
-->

- **SC-001**: [Measurable criterion, e.g., "Reduce class size from 2000 to <500 lines"]
- **SC-002**: [Measurable criterion, e.g., "Eliminate duplicate code in 3 locations"]
- **SC-003**: [Measurable criterion, e.g., "Achieve 80% test coverage"]
- **SC-004**: [Measurable criterion, e.g., "All existing tests continue to pass"]

### Non-Goals

<!--
  What is explicitly NOT in scope for this refactoring?
  This prevents scope creep.
-->

- [Explicit non-goal]
- [Another non-goal]

## Current State vs Target State

### Current State

<!--
  Brief description of the current code structure and its problems.
-->

```text
[Current structure diagram or description]
```

**Problems with current state:**
- [Problem 1]
- [Problem 2]

### Target State

<!--
  Description of the desired end state after refactoring.
-->

```text
[Target structure diagram or description]
```

**Benefits of target state:**
- [Benefit 1]
- [Benefit 2]

## Refactoring Approach

### Selected Patterns

<!--
  Which refactoring patterns will be applied?
  Reference: https://refactoring.guru/refactoring/catalog
-->

| Pattern | Purpose | Location |
|---------|---------|----------|
| [Extract Class] | [Why this pattern] | [Where to apply] |
| [Move Method] | [Why this pattern] | [Where to apply] |
| [Replace Conditional with Polymorphism] | [Why this pattern] | [Where to apply] |

### Alternative Approaches Considered

<!--
  What other approaches were considered and why were they rejected?
-->

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| [Approach 1] | [pros] | [cons] | [reason] |
| [Approach 2] | [pros] | [cons] | [reason] |

## Backward Compatibility

### Public Interface Changes

<!--
  What changes to public interfaces are required?
-->

| Interface | Change Type | Migration Path |
|-----------|-------------|----------------|
| [API/Method] | [none/deprecated/breaking] | [migration strategy] |

### Deprecation Strategy

<!--
  How will deprecated interfaces be handled?
-->

- **Phase 1**: Add deprecation warnings (keep old interface working)
- **Phase 2**: Update documentation with migration guide
- **Phase 3**: Remove deprecated interface after [timeframe]

## Risk Mitigation

### Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | [high/medium/low] | [high/medium/low] | [mitigation strategy] |
| [Risk 2] | [high/medium/low] | [high/medium/low] | [mitigation strategy] |

### Rollback Strategy

<!--
  How can we undo the refactoring if problems are discovered?
-->

- **Checkpoint 1**: [Point where rollback is easy]
- **Checkpoint 2**: [Another rollback point]
- **Full Rollback**: [Strategy for complete rollback]

## Prerequisites

### Test Coverage

- [ ] Minimum [X]% line coverage on affected code
- [ ] Characterization tests for undocumented behavior
- [ ] Integration tests for affected interfaces

### Team Readiness

- [ ] Strategy reviewed with team
- [ ] Dependencies on other work identified
- [ ] Communication plan in place

### Environment

- [ ] Feature branch created
- [ ] CI/CD pipeline ready
- [ ] Rollback procedure tested

## Phases

### Phase 1: Preparation

**Goal**: Establish safety net

**Activities**:
- Add missing tests
- Document current behavior
- Set up monitoring

**Exit Criteria**:
- All prerequisites met
- Tests passing
- Team sign-off

### Phase 2: Core Transformation

**Goal**: Apply main refactoring patterns

**Activities**:
- [Specific refactoring activities]
- [More activities]

**Exit Criteria**:
- Main structure changes complete
- Tests passing
- Code review complete

### Phase 3: Cleanup

**Goal**: Finalize and polish

**Activities**:
- Remove deprecated code
- Update documentation
- Clean up temporary scaffolding

**Exit Criteria**:
- All success criteria met
- Documentation updated
- Team sign-off

## Dependencies

### Technical Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| [Dependency 1] | [required/optional] | [ready/pending] |

### Team Dependencies

| Team/Person | Dependency | Status |
|-------------|------------|--------|
| [Team A] | [What's needed] | [ready/pending] |

## Timeline Estimate

| Phase | Estimated Duration | Notes |
|-------|-------------------|-------|
| Preparation | [X days] | [notes] |
| Core Transformation | [X days] | [notes] |
| Cleanup | [X days] | [notes] |
| **Total** | **[X days]** | |

## Review Checklist

### Strategy Completeness

- [ ] Goals are clear and measurable
- [ ] Success criteria are defined
- [ ] Non-goals are explicit
- [ ] Patterns selected with rationale
- [ ] Alternatives considered
- [ ] Risks identified with mitigations
- [ ] Rollback strategy defined
- [ ] Prerequisites listed
- [ ] Phases defined with exit criteria

### Safety

- [ ] Behavior preservation is ensured
- [ ] Test coverage is adequate
- [ ] Rollback is possible at each phase

## Next Steps

Use `/refactor.plan` to create a detailed implementation plan based on this strategy.
