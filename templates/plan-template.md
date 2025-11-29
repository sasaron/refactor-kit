# Refactoring Plan: [FEATURE NAME]

**Target**: `[path/to/target/code]`  
**Created**: [DATE]  
**Status**: Draft  
**Strategy Reference**: `[link to strategy document]`  
**Analysis Reference**: `[link to analysis document]`

## Summary

[Extract from strategy: primary goal + approach + expected outcome]

## Refactoring Context

### Scope

**Files Affected**:
- `[path/to/file1]`
- `[path/to/file2]`

**Estimated Changes**: [number] files, [rough LOC changes]

### Safety Baseline

| Metric | Current Value | Required Minimum |
|--------|---------------|------------------|
| Test Coverage | [%] | [%] |
| Tests Passing | [all/some issues] | all |
| Build Status | [passing/failing] | passing |

### Constitution Check

*GATE: Must pass before implementation begins.*

- [ ] Analysis completed (Principle I)
- [ ] Behavior preservation ensured (Principle II)
- [ ] Incremental steps defined (Principle III)
- [ ] Test coverage adequate (Principle IV)
- [ ] Strategy defined (Principle V)
- [ ] Backward compatibility addressed (Principle VI)
- [ ] Simplest approach chosen (Principle VII)
- [ ] Documentation plan in place (Principle VIII)

## Project Structure

### Documentation (this refactoring)

```text
.refactor/refactorings/[###-refactor-name]/
├── analysis.md       # /refactor.analyze output
├── strategy.md       # /refactor.strategy output
├── plan.md           # This file (/refactor.plan output)
├── tasks.md          # /refactor.tasks output
└── verification.md   # /refactor.verify output
```

### Code Changes

<!--
  Map of what code will change and how.
-->

```text
Before:
[current structure]

After:
[target structure]
```

## Implementation Phases

### Phase 0: Preparation

**Goal**: Establish safety net before any changes

#### Prerequisites

- [ ] P0-01: Create feature branch from main
- [ ] P0-02: Verify all tests pass
- [ ] P0-03: Document current test coverage
- [ ] P0-04: Add characterization tests for gaps

**Exit Criteria**:
- All tests passing
- Required coverage threshold met
- Team notified of refactoring start

### Phase 1: [First Transformation Phase Name]

**Goal**: [Specific goal for this phase]

#### Changes

| ID | Change | Pattern | Files | Tests |
|----|--------|---------|-------|-------|
| P1-01 | [description] | [pattern] | [files] | [test file] |
| P1-02 | [description] | [pattern] | [files] | [test file] |

#### Verification

- [ ] All tests pass after each change
- [ ] New tests added for new structure
- [ ] Code review completed

**Checkpoint**: [What can be verified at this point]

### Phase 2: [Second Transformation Phase Name]

**Goal**: [Specific goal for this phase]

#### Changes

| ID | Change | Pattern | Files | Tests |
|----|--------|---------|-------|-------|
| P2-01 | [description] | [pattern] | [files] | [test file] |
| P2-02 | [description] | [pattern] | [files] | [test file] |

#### Verification

- [ ] All tests pass after each change
- [ ] Integration points verified
- [ ] Code review completed

**Checkpoint**: [What can be verified at this point]

### Phase 3: Cleanup

**Goal**: Remove scaffolding and finalize

#### Changes

| ID | Change | Pattern | Files | Tests |
|----|--------|---------|-------|-------|
| P3-01 | Remove deprecated code | Inline | [files] | - |
| P3-02 | Update documentation | - | [docs] | - |

#### Verification

- [ ] All deprecated code removed
- [ ] Documentation updated
- [ ] Final code review completed

## Rollback Strategy

### Per-Phase Rollback

| Phase | Rollback Method | Difficulty |
|-------|-----------------|------------|
| Phase 0 | Delete branch | Easy |
| Phase 1 | [method] | [Easy/Medium/Hard] |
| Phase 2 | [method] | [Easy/Medium/Hard] |
| Phase 3 | [method] | [Easy/Medium/Hard] |

### Full Rollback

If refactoring must be completely abandoned:

1. Revert all commits to the last known good state (or delete the feature branch)
2. Restore any backup configuration files or data
3. Notify stakeholders of the rollback and document the reasons
4. [Add project-specific rollback steps if needed]

## Dependencies & Risks

### Dependencies

| Dependency | Phase | Type | Status |
|------------|-------|------|--------|
| [Dependency] | [Phase] | [blocking/non-blocking] | [ready/pending] |

### Risk Monitoring

| Risk | Indicator | Response |
|------|-----------|----------|
| [Risk 1] | [How to detect] | [What to do] |
| [Risk 2] | [How to detect] | [What to do] |

## Acceptance Criteria

### Functional

- [ ] All existing tests pass
- [ ] No regression in functionality
- [ ] Performance maintained or improved

### Structural

- [ ] [Success criterion from strategy]
- [ ] [Success criterion from strategy]

### Quality

- [ ] Code complexity reduced
- [ ] Test coverage maintained or improved
- [ ] Documentation updated

## Next Steps

Use `/refactor.tasks` to generate detailed, executable tasks from this plan.
