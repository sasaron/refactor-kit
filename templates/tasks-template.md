---
description: "Task list template for refactoring implementation"
---

# Refactoring Tasks: [FEATURE NAME]

**Input**: Design documents from `.refactor/refactorings/[###-refactor-name]/`
**Prerequisites**: plan.md (required), strategy.md (required), analysis.md (required)

## Format: `[ID] [P?] [Phase] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Phase]**: Which phase this task belongs to (e.g., P0, P1, P2)
- Include exact file paths in descriptions

## Path Conventions

- Reference exact file paths from the plan
- Use relative paths from repository root

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /refactor.tasks command MUST replace these with actual tasks based on:
  - Changes from plan.md phases
  - Safety requirements from strategy.md
  - Risk factors from analysis.md
  
  Tasks MUST be organized by phase so each phase can be:
  - Executed independently (after prerequisites)
  - Verified independently
  - Rolled back if needed
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 0: Preparation (Safety Net)

**Purpose**: Establish safety before any code changes

- [ ] T001 Create feature branch `refactor/[###-refactor-name]`
- [ ] T002 Verify all existing tests pass
- [ ] T003 Document current test coverage percentage
- [ ] T004 [P] Add characterization test for [undocumented behavior 1]
- [ ] T005 [P] Add characterization test for [undocumented behavior 2]
- [ ] T006 Verify coverage meets minimum threshold

**Checkpoint**: Safety net established - all tests pass, coverage adequate

---

## Phase 1: [First Transformation Phase Name]

**Purpose**: [Phase goal from plan]

### Tests First (if adding new structure)

- [ ] T007 [P] [P1] Write test for new [ComponentA] in tests/[path]/test_[name].py
- [ ] T008 [P] [P1] Write test for new [ComponentB] in tests/[path]/test_[name].py
- [ ] T009 Verify new tests FAIL (Red phase)

### Implementation

- [ ] T010 [P1] Extract [CodeA] to new file src/[path]/[new_file].py
- [ ] T011 [P1] Move [MethodA] to [NewClass] in src/[path]/[file].py
- [ ] T012 [P1] Update imports in src/[path]/[original_file].py
- [ ] T013 [P1] Verify all tests pass (Green phase)

### Cleanup

- [ ] T014 [P1] Remove commented-out code in src/[path]/[file].py
- [ ] T015 [P1] Update docstrings in src/[path]/[file].py

**Checkpoint**: Phase 1 complete - structure improved, tests pass

---

## Phase 2: [Second Transformation Phase Name]

**Purpose**: [Phase goal from plan]

### Tests First

- [ ] T016 [P] [P2] Write integration test for [new interaction]
- [ ] T017 Verify new tests FAIL (Red phase)

### Implementation

- [ ] T018 [P2] Refactor [ComponentC] in src/[path]/[file].py
- [ ] T019 [P2] Update [dependent code] in src/[path]/[file].py
- [ ] T020 [P2] Verify all tests pass (Green phase)

**Checkpoint**: Phase 2 complete - integration verified, tests pass

---

## Phase 3: Cleanup

**Purpose**: Remove scaffolding and finalize

- [ ] T021 [P] [P3] Remove deprecated [old_code] from src/[path]/[file].py
- [ ] T022 [P] [P3] Remove backward compatibility shim in src/[path]/[file].py
- [ ] T023 [P3] Update README.md with new structure documentation
- [ ] T024 [P3] Update API documentation in docs/[file].md
- [ ] T025 [P3] Final verification - all tests pass
- [ ] T026 [P3] Create PR for review

**Checkpoint**: Refactoring complete - ready for review

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 0 (Preparation)**: No dependencies - MUST complete first
- **Phase 1**: Depends on Phase 0 completion
- **Phase 2**: Depends on Phase 1 completion
- **Phase 3 (Cleanup)**: Depends on all previous phases

### Within Each Phase

1. Safety checks first (verify tests pass)
2. Write new tests (if adding structure)
3. Implement changes
4. Verify tests pass after each change
5. Cleanup and documentation

### Parallel Opportunities

- All tasks marked [P] can run in parallel
- Tests for different components can be written in parallel
- Documentation updates can parallel implementation (after structure is stable)

---

## Rollback Points

| After Task | Rollback Difficulty | Method |
|------------|---------------------|--------|
| Phase 0 complete | Easy | Delete branch |
| Phase 1 complete | Easy | Revert commits |
| Phase 2 complete | Medium | Revert commits + verify integrations |
| Phase 3 complete | Hard | Full revert, may need migration |

---

## Verification Commands

### After Each Task

```bash
# Run relevant tests
pytest tests/[relevant_path] -v

# Verify coverage
pytest --cov=src/[path] --cov-report=term-missing
```

### After Each Phase

```bash
# Run full test suite
pytest

# Check for regressions
# [Add any regression check commands specific to project]
```

---

## Notes

- [P] tasks = different files, no dependencies
- Commit after each task or logical group
- Run tests after EVERY change
- Stop and investigate any test failure immediately
- Document any deviations from plan in the **Notes** section below or create a new **Deviations** section

## Post-Completion

After all tasks complete:

1. Use `/refactor.verify` to generate verification report
2. Create PR with summary of changes
3. Request code review
4. Update team documentation
