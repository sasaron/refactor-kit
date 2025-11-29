# Installation Guide

## Prerequisites

- **Linux/macOS** (or Windows with WSL)
- AI coding agent: [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [GitHub Copilot](https://code.visualstudio.com/), [Gemini CLI](https://github.com/google-gemini/gemini-cli), or [Cursor](https://cursor.sh/)
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Installation

### Initialize a New Project

The easiest way to get started is to initialize a new project:

```bash
uvx --from git+https://github.com/sasaron/refactor-kit.git refactor init <PROJECT_NAME>
```

Or initialize in the current directory:

```bash
uvx --from git+https://github.com/sasaron/refactor-kit.git refactor init .
# or use the --here flag
uvx --from git+https://github.com/sasaron/refactor-kit.git refactor init --here
```

### Persistent Installation

For frequent use, install the CLI globally:

```bash
uv tool install refactor-cli --from git+https://github.com/sasaron/refactor-kit.git
```

Then use directly:

```bash
refactor init <PROJECT_NAME>
```

### Specify AI Agent

You can specify your AI agent during initialization:

```bash
refactor init <project_name> --ai claude
refactor init <project_name> --ai gemini
refactor init <project_name> --ai copilot
refactor init <project_name> --ai cursor-agent
```

### Skip Git Initialization

If you don't want to initialize a git repository:

```bash
refactor init <project_name> --no-git
```

### Ignore Agent Tools Check

Skip checking for AI agent CLI tools:

```bash
refactor init <project_name> --ai claude --ignore-agent-tools
```

### Debug Mode

For troubleshooting, use the `--debug` flag to see verbose diagnostic output:

```bash
refactor init <project_name> --debug
```

## Verification

After initialization, verify your setup:

```bash
refactor check
```

This will check for:
- Git version control
- Python 3.11+
- AI agent CLI tools (Claude, Gemini, Cursor)

## Project Structure

After initialization, your project will have the following structure:

```
<project_name>/
├── .refactor/
│   ├── memory/          # Project refactoring memory
│   ├── templates/       # Refactoring templates
│   └── refactorings/    # Refactoring history
├── .claude/commands/    # (if --ai claude)
├── .gemini/commands/    # (if --ai gemini)
├── .github/agents/      # (if --ai copilot)
└── .cursor/commands/    # (if --ai cursor-agent)
```

## Troubleshooting

### Git Not Found

If git is not found, install it from [git-scm.com](https://git-scm.com/downloads).

### AI Agent CLI Not Found

If your AI agent CLI is not found:

- **Claude Code**: Install from [Anthropic docs](https://docs.anthropic.com/en/docs/claude-code)
- **Gemini CLI**: Install from [GitHub](https://github.com/google-gemini/gemini-cli)
- **Cursor**: Install from [cursor.sh](https://cursor.sh/)
- **GitHub Copilot**: No CLI required (IDE-based)

### Debug Issues

Use the `--debug` flag to see detailed diagnostic information:

```bash
refactor init my-project --debug
```

This will show:
- Python version and platform information
- Directory paths being used
- Step-by-step execution details
