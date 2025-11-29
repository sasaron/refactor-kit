# AGENTS.md

## About Refactor Kit and Refactor CLI

**Refactor Kit** is a comprehensive toolkit for implementing Refactoring-Driven Development (RDD) - a methodology that emphasizes systematic analysis and safe code transformation. The toolkit includes templates, scripts, and workflows that guide development teams through a structured approach to improving existing software.

**Refactor CLI** is the command-line interface that bootstraps projects with the Refactor Kit framework. It sets up the necessary directory structures, templates, and AI agent integrations to support the Refactoring-Driven Development workflow.

The toolkit supports multiple AI coding assistants, allowing teams to use their preferred tools while maintaining consistent project structure and development practices.

---

## General Practices

- Any changes to `__init__.py` for the Refactor CLI require a version rev in `pyproject.toml` and addition of entries to `CHANGELOG.md`.

## Adding New Agent Support

This section explains how to add support for new AI agents/assistants to the Refactor CLI. Use this guide as a reference when integrating new AI tools into the Refactoring-Driven Development workflow.

### Overview

Refactor Kit supports multiple AI agents by generating agent-specific command files and directory structures when initializing projects. Each agent has its own conventions for:

- **Command file formats** (Markdown, TOML, etc.)
- **Directory structures** (`.claude/commands/`, `.windsurf/workflows/`, etc.)
- **Command invocation patterns** (slash commands, CLI tools, etc.)
- **Argument passing conventions** (`$ARGUMENTS`, `{{args}}`, etc.)

### Current Supported Agents

| Agent | Directory | Format | CLI Tool | Description |
|-------|-----------|--------|----------|-------------|
| **Claude Code** | `.claude/commands/` | Markdown | `claude` | Anthropic's Claude Code CLI |
| **Gemini CLI** | `.gemini/commands/` | TOML | `gemini` | Google's Gemini CLI |
| **GitHub Copilot** | `.github/agents/` | Markdown | N/A (IDE-based) | GitHub Copilot in VS Code |
| **Cursor** | `.cursor/commands/` | Markdown | `cursor-agent` | Cursor CLI |

### Step-by-Step Integration Guide

Follow these steps to add a new agent:

#### 1. Add to AGENT_CONFIG

**IMPORTANT**: Use the actual CLI tool name as the key, not a shortened version.

Add the new agent to the `AGENT_CONFIG` dictionary in `src/refactor_cli/__init__.py`:

```python
AGENT_CONFIG = {
    # ... existing agents ...
    "new-agent-cli": {  # Use the ACTUAL CLI tool name
        "name": "New Agent Display Name",
        "folder": ".newagent/",
        "install_url": "https://example.com/install",
        "requires_cli": True,  # True if CLI tool required, False for IDE-based agents
    },
}
```

**Key Design Principle**: The dictionary key should match the actual executable name that users install.

#### 2. Create Command Templates

Create command templates for the new agent in `templates/commands/`:

For Markdown-based agents:
```markdown
---
description: "Command description"
---

Command content with {SCRIPT} and $ARGUMENTS placeholders.
```

For TOML-based agents:
```toml
description = "Command description"

prompt = """
Command content with {SCRIPT} and {{args}} placeholders.
"""
```

#### 3. Update CLI Help Text

Update the `--ai` parameter help text in the `init()` command to include the new agent.

#### 4. Update README Documentation

Update the **Supported AI Agents** section in `README.md` to include the new agent.

## Agent Categories

### CLI-Based Agents

Require a command-line tool to be installed:
- **Claude Code**: `claude` CLI
- **Gemini CLI**: `gemini` CLI
- **Cursor**: `cursor-agent` CLI

### IDE-Based Agents

Work within integrated development environments:
- **GitHub Copilot**: Built into VS Code/compatible editors

## Command File Formats

### Markdown Format

Used by: Claude, Cursor, Copilot

```markdown
---
description: "Command description"
---

Command content with $ARGUMENTS placeholders.
```

### TOML Format

Used by: Gemini

```toml
description = "Command description"

prompt = """
Command content with {{args}} placeholders.
"""
```

## Argument Patterns

Different agents use different argument placeholders:

- **Markdown/prompt-based**: `$ARGUMENTS`
- **TOML-based**: `{{args}}`

## Testing New Agent Integration

1. **Build test**: Run package creation script locally
2. **CLI test**: Test `refactor init --ai <agent>` command
3. **File generation**: Verify correct directory structure and files
4. **Command validation**: Ensure generated commands work with the agent

## Common Pitfalls

1. **Using shorthand keys**: Always use the actual executable name as the AGENT_CONFIG key
2. **Wrong argument format**: Use correct placeholder format for each agent type
3. **Directory naming**: Follow agent-specific conventions exactly

---

*This documentation should be updated whenever new agents are added to maintain accuracy and completeness.*
