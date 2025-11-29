# [PROJECT_NAME] Refactoring Constitution

## Core Principles

### I. Analysis-First Principle

Before any refactoring begins, thorough analysis is **mandatory**:

- Map code structure, dependencies, and relationships
- Identify code smells with severity ratings
- Assess test coverage and safety level
- Document risk factors and mitigation strategies

**Rationale**: Understanding precedes transformation. Refactoring without understanding is just editing with extra risk.

### II. Behavior Preservation (NON-NEGOTIABLE)

Refactoring MUST NOT change external behavior:

- All existing tests must continue to pass
- Public APIs must remain compatible (or migration paths provided)
- Side effects must be preserved exactly
- Performance characteristics should be maintained or improved

**Rationale**: This is the definition of refactoring. Changing behavior is a feature change, not refactoring.

### III. Incremental Transformation

Large refactorings MUST be broken into small, verifiable steps:

- Each step should be independently verifiable
- Each step should be reversible if needed
- Progress should be committable at any point
- The codebase should remain functional after each step

**Rationale**: Big-bang changes are high-risk and often fail. Incremental changes are safer and more manageable.

### IV. Test-Driven Safety

Adequate test coverage is REQUIRED before refactoring:

- If tests don't exist, create characterization tests first
- If test coverage is low, increase it before changing code
- Tests must run fast enough for continuous feedback
- All tests must be reliable (no flaky tests)

**Rationale**: Tests are the safety net. Without them, you're walking a tightrope without protection.

### V. Strategy Over Tactics

Individual refactoring moves must serve a larger goal:

- Define clear refactoring objectives before starting
- Choose patterns that serve the objectives
- Evaluate alternatives before committing
- Document the reasoning for future reference

**Rationale**: Without strategy, individual moves may not add up to improvement.

### VI. Backward Compatibility

When refactoring public interfaces:

- Maintain existing interfaces when possible
- Provide clear migration paths for breaking changes
- Use deprecation warnings before removal
- Document all changes that affect consumers

**Rationale**: Refactoring should not break downstream dependencies.

### VII. Simplicity Principle

Prefer simple solutions over complex ones:

- Start with the simplest refactoring that could work
- Add complexity only when proven necessary
- Remove unnecessary abstractions
- Follow YAGNI (You Aren't Gonna Need It)

**Rationale**: Complexity is the enemy of maintainability. Refactoring should reduce complexity, not add it.

### VIII. Documentation and Communication

All significant refactorings must be documented:

- Update code comments to reflect new structure
- Update design documentation
- Communicate changes to affected team members
- Record decisions and rationale

**Rationale**: Refactoring changes structure. Documentation must keep pace.

## Safety Requirements

### Before Starting Any Refactoring

- [ ] Codebase analysis is complete
- [ ] All tests pass (green state)
- [ ] Test coverage is adequate for affected code
- [ ] Refactoring strategy is defined and reviewed
- [ ] Rollback plan exists

### During Refactoring

- [ ] Run tests after each change
- [ ] Commit frequently
- [ ] Track progress against plan
- [ ] Note any deviations or discoveries

### After Completing Refactoring

- [ ] All tests pass
- [ ] Code quality metrics improved or maintained
- [ ] Documentation updated
- [ ] Changes communicated to team
- [ ] Lessons learned documented

## Governance

- This constitution supersedes ad-hoc refactoring practices
- Amendments require team review and approval
- Violations must be documented with justification
- Regular reviews to improve the process

**Version**: 1.0.0 | **Ratified**: [DATE] | **Last Amended**: [DATE]
