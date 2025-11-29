# Quick Start Guide

This guide will help you get started with Refactoring-Driven Development using Refactor Kit.

## The 7-Step Process

### Step 1: Install Refactor Kit

**In your terminal**, run the `refactor` CLI command to initialize your project:

```bash
# Create a new project directory
uvx --from git+https://github.com/sasaron/refactor-kit.git refactor init <PROJECT_NAME>

# OR initialize in the current directory
uvx --from git+https://github.com/sasaron/refactor-kit.git refactor init .
```

Specify your AI agent:

```bash
uvx --from git+https://github.com/sasaron/refactor-kit.git refactor init <PROJECT_NAME> --ai claude
```

### Step 2: Define Your Constitution

**In your AI Agent's chat interface**, use the `/refactor.constitution` slash command to establish the core rules and principles for your refactoring project.

```markdown
/refactor.constitution This project follows strict behavior preservation. All refactoring must maintain 100% test coverage. We prioritize readability over cleverness. We use incremental commits for each refactoring step.
```

### Step 3: Analyze the Codebase

**In the chat**, use the `/refactor.analyze` slash command to understand the current state of your codebase.

```markdown
/refactor.analyze Focus on identifying code smells, dependency issues, and test coverage gaps.
```

This will generate a comprehensive analysis including:
- Code structure metrics
- Dependency analysis
- Code smell detection
- Test coverage assessment
- Risk assessment

### Step 4: Define Refactoring Strategy

**In the chat**, use the `/refactor.strategy` slash command to define your approach.

```markdown
/refactor.strategy Our goal is to improve testability by reducing coupling. We'll use dependency injection and extract interfaces where needed.
```

### Step 5: Create Implementation Plan

**In the chat**, use the `/refactor.plan` slash command to create a detailed plan.

```markdown
/refactor.plan Break down the refactoring into phases, with safety checkpoints after each phase.
```

### Step 6: Generate Tasks

**In the chat**, use the `/refactor.tasks` slash command to create actionable tasks.

```markdown
/refactor.tasks
```

### Step 7: Execute and Verify

**In the chat**, use `/refactor.execute` to implement the refactoring:

```markdown
/refactor.execute
```

After each step, verify with `/refactor.verify`:

```markdown
/refactor.verify
```

## Example: Refactoring a Legacy Module

Here's a complete example of refactoring a tightly-coupled module:

### Step 1: Initialize Project

```bash
refactor init my-legacy-app --ai claude
cd my-legacy-app
```

### Step 2: Define Constitution

```markdown
/refactor.constitution This is a legacy codebase with limited tests. Our priority is to add test coverage before refactoring. All changes must be backward compatible. We'll use the Strangler Fig pattern for gradual replacement.
```

### Step 3: Analyze

```markdown
/refactor.analyze The main pain point is the UserService class which has grown to 2000+ lines and handles authentication, authorization, profile management, and notification sending.
```

### Step 4: Strategy

```markdown
/refactor.strategy We will extract each responsibility into separate services: AuthService, AuthorizationService, ProfileService, and NotificationService. We'll use the Extract Class refactoring pattern.
```

### Step 5: Plan

```markdown
/refactor.plan Create a phased approach:
Phase 1: Add comprehensive tests to UserService
Phase 2: Extract AuthService
Phase 3: Extract AuthorizationService
Phase 4: Extract ProfileService
Phase 5: Extract NotificationService
Phase 6: Remove deprecated code from UserService
```

### Step 6: Generate Tasks

```markdown
/refactor.tasks Generate tasks for Phase 1 only. We'll iterate through each phase.
```

### Step 7: Execute

```markdown
/refactor.execute Start with the first task in Phase 1.
```

After completing Phase 1:

```markdown
/refactor.verify Confirm all tests pass and coverage is adequate before proceeding to Phase 2.
```

## Key Principles

- **Understand before changing** - Always analyze first
- **Test coverage is non-negotiable** - Add tests before refactoring if needed
- **Small, incremental steps** - Each change should be verifiable
- **Behavior preservation** - Tests must pass after each step
- **Document as you go** - Keep track of what changed and why

## Next Steps

- Read the [Installation Guide](installation.md) for detailed setup instructions
- Check out the [Refactoring-Driven Development methodology](../ai-enabling-refactoring.md)
- Explore the [source code on GitHub](https://github.com/sasaron/refactor-kit)
