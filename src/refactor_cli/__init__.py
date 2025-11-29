"""Refactor CLI - A tool for Refactoring-Driven Development (RDD)."""

import shutil
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

__version__ = "0.0.1"

app = typer.Typer(
    name="refactor",
    help="Refactor Kit CLI - Bootstrap your projects for Refactoring-Driven Development",
    no_args_is_help=True,
)

console = Console()

# Agent configuration - single source of truth for all agent metadata
AGENT_CONFIG = {
    "claude": {
        "name": "Claude Code",
        "folder": ".claude/commands/",
        "install_url": "https://docs.anthropic.com/en/docs/claude-code",
        "requires_cli": True,
    },
    "gemini": {
        "name": "Gemini CLI",
        "folder": ".gemini/commands/",
        "install_url": "https://github.com/google-gemini/gemini-cli",
        "requires_cli": True,
    },
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github/agents/",
        "install_url": None,
        "requires_cli": False,
    },
    "cursor-agent": {
        "name": "Cursor",
        "folder": ".cursor/commands/",
        "install_url": "https://cursor.sh/",
        "requires_cli": True,
    },
}


def check_tool(tool: str, install_url: str) -> bool:
    """Check if a tool is installed and available in PATH."""
    result = shutil.which(tool)
    if result:
        console.print(f"  [green]✓[/green] {tool} found at {result}")
        return True
    else:
        console.print(f"  [red]✗[/red] {tool} not found")
        if install_url:
            console.print(f"    Install from: {install_url}")
        return False


@app.command()
def check():
    """Check for installed tools (git, AI agents, etc.)."""
    console.print(Panel.fit("[bold]Refactor Kit - System Check[/bold]"))
    console.print()

    table = Table(title="Required Tools")
    table.add_column("Tool", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Notes", style="dim")

    # Check git
    git_ok = check_tool("git", "https://git-scm.com/downloads")
    table.add_row("git", "✓" if git_ok else "✗", "Version control (required)")

    # Check Python
    python_ok = sys.version_info >= (3, 11)
    table.add_row(
        "python",
        "✓" if python_ok else "✗",
        f"Python {sys.version_info.major}.{sys.version_info.minor}",
    )

    console.print()
    console.print(table)

    # Check AI agents
    console.print()
    console.print("[bold]AI Agent Tools (optional)[/bold]")
    for agent_key, config in AGENT_CONFIG.items():
        if config["requires_cli"]:
            check_tool(agent_key, config["install_url"])


@app.command()
def init(
    project_name: Optional[str] = typer.Argument(
        None, help="Name for your new project directory (use '.' for current directory)"
    ),
    ai_assistant: Optional[str] = typer.Option(
        None,
        "--ai",
        help="AI assistant to use: claude, gemini, copilot, cursor-agent",
    ),
    here: bool = typer.Option(
        False, "--here", help="Initialize project in the current directory"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Force merge/overwrite when initializing in current directory",
    ),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    ignore_agent_tools: bool = typer.Option(
        False, "--ignore-agent-tools", help="Skip checks for AI agent tools"
    ),
):
    """Initialize a new Refactor Kit project from the latest template."""
    console.print(Panel.fit("[bold]Refactor Kit - Project Initialization[/bold]"))

    # Determine target directory
    if here or project_name == ".":
        target_dir = Path.cwd()
        console.print(f"Initializing in current directory: {target_dir}")
    elif project_name:
        target_dir = Path.cwd() / project_name
        if target_dir.exists() and not force:
            console.print(
                f"[red]Error:[/red] Directory '{project_name}' already exists. Use --force to overwrite."
            )
            raise typer.Exit(1)
    else:
        console.print("[red]Error:[/red] Please provide a project name or use --here flag.")
        raise typer.Exit(1)

    # Create directory structure
    target_dir.mkdir(parents=True, exist_ok=True)

    # Create .refactor directory structure
    refactor_dir = target_dir / ".refactor"
    (refactor_dir / "memory").mkdir(parents=True, exist_ok=True)
    (refactor_dir / "templates").mkdir(parents=True, exist_ok=True)
    (refactor_dir / "refactorings").mkdir(parents=True, exist_ok=True)

    console.print(f"[green]✓[/green] Created project structure at {target_dir}")

    # Initialize git if not disabled
    if not no_git and not (target_dir / ".git").exists():
        import subprocess

        subprocess.run(["git", "init"], cwd=target_dir, capture_output=True)
        console.print("[green]✓[/green] Initialized git repository")

    # Set up AI agent commands if specified
    if ai_assistant:
        if ai_assistant not in AGENT_CONFIG:
            console.print(
                f"[red]Error:[/red] Unknown AI assistant '{ai_assistant}'. "
                f"Available: {', '.join(AGENT_CONFIG.keys())}"
            )
            raise typer.Exit(1)

        config = AGENT_CONFIG[ai_assistant]

        # Check if CLI tool is available (unless --ignore-agent-tools is set)
        if config["requires_cli"] and not ignore_agent_tools:
            if not shutil.which(ai_assistant):
                console.print(
                    f"[yellow]Warning:[/yellow] {config['name']} CLI not found. "
                    f"Install from: {config['install_url']}"
                )

        # Create agent commands directory
        agent_dir = target_dir / config["folder"]
        agent_dir.mkdir(parents=True, exist_ok=True)
        console.print(f"[green]✓[/green] Set up {config['name']} commands directory")

    console.print()
    console.print("[bold green]Project initialized successfully![/bold green]")
    console.print()
    console.print("Next steps:")
    console.print("  1. Navigate to your project directory")
    console.print("  2. Run your AI assistant")
    console.print("  3. Use /refactor.analyze to analyze your codebase")
    console.print("  4. Use /refactor.strategy to define refactoring strategy")


@app.command()
def version():
    """Show the version of Refactor CLI."""
    console.print(f"Refactor CLI version {__version__}")


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
