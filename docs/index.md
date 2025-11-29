# Refactor Kit

*Prepare your codebase for AI-assisted development.*

**An effort to help developers systematically refactor codebases to enable more effective AI collaboration through Refactoring-Driven Development (RDD).**

## What is Refactoring-Driven Development?

Refactoring-Driven Development (RDD) is a structured approach that prioritizes **clean, well-organized code** as the foundation for AI-assisted development. The core insight: AI assistants provide better suggestions when working with well-structured codebases.

## Getting Started

- [Installation Guide](installation.md)
- [Quick Start Guide](quickstart.md)

## Core Philosophy

Refactoring-Driven Development emphasizes:

- **Analysis-First**: Understand before refactoring
- **Behavior Preservation**: Non-negotiable - all tests must pass
- **Incremental Transformation**: Small, verifiable steps
- **Test-Driven Safety**: Adequate coverage required
- **Strategy Over Tactics**: Clear goals before action
- **Backward Compatibility**: Maintain interfaces
- **Simplicity Principle**: Prefer simple solutions
- **Documentation & Communication**: Keep docs updated

## Development Phases

| Phase | Focus | Key Activities |
|-------|-------|----------------|
| **Analysis** | Understand the codebase | <ul><li>Identify code smells</li><li>Map dependencies</li><li>Assess test coverage</li><li>Evaluate risks</li></ul> |
| **Strategy** | Define refactoring approach | <ul><li>Set objectives</li><li>Choose patterns</li><li>Plan backward compatibility</li><li>Define success criteria</li></ul> |
| **Planning** | Create implementation plan | <ul><li>Break into phases</li><li>Set safety checkpoints</li><li>Plan rollback strategies</li><li>Define test requirements</li></ul> |
| **Execution** | Implement refactoring | <ul><li>Execute tasks</li><li>Verify at each step</li><li>Maintain tests</li><li>Document changes</li></ul> |

## Slash Commands

Refactor Kit provides the following slash commands for AI agents:

| Command | Description |
|---------|-------------|
| `/refactor.constitution` | Establish project refactoring principles |
| `/refactor.analyze` | Analyze codebase for refactoring opportunities |
| `/refactor.strategy` | Define refactoring strategy and approach |
| `/refactor.plan` | Create detailed implementation plan |
| `/refactor.tasks` | Generate actionable task lists |
| `/refactor.execute` | Execute refactoring systematically |
| `/refactor.verify` | Verify behavior preservation and success |

## Supported AI Agents

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [GitHub Copilot](https://github.com/features/copilot)
- [Cursor](https://cursor.sh/)

## Contributing

Please see our [Contributing Guide](https://github.com/sasaron/refactor-kit/blob/main/CONTRIBUTING.md) for information on how to contribute to this project.

## Support

For support, please open an issue on [GitHub](https://github.com/sasaron/refactor-kit/issues).
