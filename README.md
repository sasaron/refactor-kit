<div align="center">
    <h1>🔧 Refactor Kit</h1>
    <h3><em>Make your codebase AI-ready through systematic refactoring.</em></h3>
</div>

<p align="center">
    <strong>An open source toolkit for structured, safe, and systematic code refactoring that enables effective AI-assisted development.</strong>
</p>

---

## Table of Contents

- [🤔 Why Refactoring is Essential for AI-Enabled Development](#-why-refactoring-is-essential-for-ai-enabled-development)
- [⚡ Get Started](#-get-started)
- [🤖 Supported AI Agents](#-supported-ai-agents)
- [🔧 Refactor CLI Reference](#-refactor-cli-reference)
- [📚 Core Philosophy](#-core-philosophy)
- [🌟 Refactoring Phases](#-refactoring-phases)
- [📋 Detailed Process](#-detailed-process)
- [🔧 Prerequisites](#-prerequisites)
- [👥 Maintainers](#-maintainers)
- [📄 License](#-license)

## 🤔 Why Refactoring is Essential for AI-Enabled Development

AI coding assistants work best with **clean, well-structured code**. Legacy codebases with tangled dependencies, unclear responsibilities, and poor naming make it difficult for AI to understand context and provide accurate suggestions.

**Refactor Kit** provides a systematic approach to prepare your codebase for effective AI collaboration:

- **Clear Structure**: AI understands modular, well-organized code better
- **Reduced Complexity**: Simpler code means more accurate AI suggestions
- **Better Naming**: Self-documenting code gives AI clearer context
- **Isolated Components**: AI can work on independent units without side effects

### The AI-Ready Codebase

A codebase that is easy for AI to work with is also easier for humans to understand and maintain. This toolkit promotes systematic refactoring that benefits both AI assistants and human developers.

## ⚡ Get Started

### 1. Install Refactor CLI

Choose your preferred installation method:

#### Option 1: Persistent Installation (Recommended)

Install once and use everywhere:

```bash
uv tool install refactor-cli --from git+https://github.com/sasaron/refactor-kit.git
```

Then use the tool directly:

```bash
refactor init <PROJECT_NAME>
refactor check
```

#### Option 2: One-time Usage

Run directly without installing:

```bash
uvx --from git+https://github.com/sasaron/refactor-kit.git refactor init <PROJECT_NAME>
```

### 2. Establish refactoring principles

Launch your AI assistant in the project directory. The `/refactor.*` commands are available in the assistant.

Use the **`/refactor.constitution`** command to create your project's governing principles for refactoring.

```bash
/refactor.constitution Create principles focused on code quality, backward compatibility, testing standards, and incremental improvement
```

### 3. Analyze the codebase

Use the **`/refactor.analyze`** command to understand your current codebase structure.

```bash
/refactor.analyze Analyze the authentication module for code smells and improvement opportunities
```

### 4. Define refactoring strategy

Use the **`/refactor.strategy`** command to define your refactoring approach.

```bash
/refactor.strategy Extract authentication logic into a separate service with clean interfaces
```

### 5. Create implementation plan

Use **`/refactor.plan`** to create a detailed, step-by-step refactoring plan.

```bash
/refactor.plan
```

### 6. Break down into tasks

Use **`/refactor.tasks`** to generate an executable task list.

```bash
/refactor.tasks
```

### 7. Execute refactoring

Use **`/refactor.execute`** to systematically implement the refactoring.

```bash
/refactor.execute
```

### 8. Verify the refactoring

Use **`/refactor.verify`** to ensure the refactoring is complete and behavior is preserved.

```bash
/refactor.verify
```

For detailed step-by-step instructions, see our [comprehensive guide](./ai-enabling-refactoring.md).

## 🤖 Supported AI Agents

| Agent | Support | Notes |
|-------|---------|-------|
| [Claude Code](https://www.anthropic.com/claude-code) | ✅ | |
| [GitHub Copilot](https://code.visualstudio.com/) | ✅ | |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | ✅ | |
| [Cursor](https://cursor.sh/) | ✅ | |

## 🔧 Refactor CLI Reference

The `refactor` command supports the following options:

### Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize a new Refactor Kit project from the latest template |
| `check` | Check for installed tools (`git`, `claude`, `gemini`, etc.) |
| `version` | Show the version of Refactor CLI |

### `refactor init` Arguments & Options

| Argument/Option | Type | Description |
|-----------------|------|-------------|
| `<project-name>` | Argument | Name for your new project directory (use `.` for current directory) |
| `--ai` | Option | AI assistant to use: `claude`, `gemini`, `copilot`, `cursor-agent` |
| `--here` | Flag | Initialize project in the current directory |
| `--force` | Flag | Force merge/overwrite when initializing in current directory |
| `--no-git` | Flag | Skip git repository initialization |
| `--ignore-agent-tools` | Flag | Skip checks for AI agent tools |

### Available Slash Commands

After running `refactor init`, your AI coding agent will have access to these slash commands:

#### Core Commands

| Command | Description |
|---------|-------------|
| `/refactor.constitution` | Create or update project refactoring principles and guidelines |
| `/refactor.analyze` | Analyze codebase for refactoring opportunities |
| `/refactor.strategy` | Define refactoring strategy and approach |
| `/refactor.plan` | Create detailed implementation plan |
| `/refactor.tasks` | Generate actionable task lists for implementation |
| `/refactor.execute` | Execute all tasks to implement the refactoring |
| `/refactor.verify` | Verify behavior preservation and refactoring success |

## 📚 Core Philosophy

Systematic refactoring for AI-enabled development emphasizes:

- **Analysis-first approach** where understanding precedes action
- **Behavior preservation** as the non-negotiable constraint
- **Incremental transformations** rather than big-bang rewrites
- **Test-driven safety nets** to catch regressions early
- **AI collaboration** as a key benefit of clean, well-structured code

## 🌟 Refactoring Phases

| Phase | Focus | Key Activities |
|-------|-------|----------------|
| **Analysis** | Understand current state | <ul><li>Map code structure and dependencies</li><li>Identify code smells and technical debt</li><li>Assess test coverage and safety</li></ul> |
| **Strategy** | Define approach | <ul><li>Set refactoring goals</li><li>Choose refactoring patterns</li><li>Define success criteria</li></ul> |
| **Planning** | Detailed roadmap | <ul><li>Break into phases</li><li>Identify risks and mitigations</li><li>Define checkpoints</li></ul> |
| **Execution** | Implement safely | <ul><li>Incremental changes</li><li>Continuous verification</li><li>Rollback capability</li></ul> |
| **Verification** | Confirm success | <ul><li>Behavior preservation tests</li><li>Code quality metrics</li><li>Documentation updates</li></ul> |

## 📋 Detailed Process

<details>
<summary>Click to expand the detailed step-by-step walkthrough</summary>

### **STEP 1:** Analyze the codebase

Use `/refactor.analyze` with a description of what you want to refactor:

```text
/refactor.analyze The user authentication module has grown complex with multiple responsibilities. 
Analyze the current structure, identify code smells, and assess the risk level of refactoring.
```

This will produce:
- Code structure analysis
- Dependency mapping
- Code smell identification
- Test coverage assessment
- Risk analysis

### **STEP 2:** Define refactoring strategy

Use `/refactor.strategy` to define your approach:

```text
/refactor.strategy Extract the authentication logic into a separate AuthService class, 
separating concerns for login, session management, and token handling.
```

This will produce:
- Refactoring goals
- Chosen patterns (Extract Class, Move Method, etc.)
- Success criteria
- Risk mitigation strategies

### **STEP 3:** Create implementation plan

Use `/refactor.plan` to create a detailed plan:

```text
/refactor.plan
```

This will produce:
- Phased implementation plan
- Safety checkpoints
- Rollback strategies
- Test requirements

### **STEP 4:** Generate tasks

Use `/refactor.tasks` to create an executable task list:

```text
/refactor.tasks
```

This produces tasks organized by:
- Dependencies (what must be done first)
- Safety (tests before changes)
- Parallelization opportunities

### **STEP 5:** Execute the refactoring

Use `/refactor.execute` to implement the changes:

```text
/refactor.execute
```

The command will:
- Execute tasks in correct order
- Run tests after each change
- Provide rollback if tests fail

### **STEP 6:** Verify the refactoring

Use `/refactor.verify` to confirm success:

```text
/refactor.verify
```

This will:
- Run all tests
- Compare behavior before/after
- Check code quality metrics
- Generate summary report

</details>

## 🔧 Prerequisites

- **Linux/macOS/Windows**
- [Supported](#-supported-ai-agents) AI coding agent
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## 👥 Maintainers

- RyunosukeSasaki ([@sasaron](https://github.com/sasaron))

## 📄 License

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) file for the full terms.