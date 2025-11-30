"""Refactor CLI - A tool for Refactoring-Driven Development (RDD)."""

import os
import subprocess
import shutil
import sys
from pathlib import Path
from typing import Optional, Tuple

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.text import Text
from rich.align import Align
from rich.live import Live
from typer.core import TyperGroup

import readchar

__version__ = "0.0.1"

# ASCII Art Banner
BANNER = """
██████╗ ███████╗███████╗ █████╗  ██████╗████████╗ ██████╗ ██████╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██████╔╝█████╗  █████╗  ███████║██║        ██║   ██║   ██║██████╔╝
██╔══██╗██╔══╝  ██╔══╝  ██╔══██║██║        ██║   ██║   ██║██╔══██╗
██║  ██║███████╗██║     ██║  ██║╚██████╗   ██║   ╚██████╔╝██║  ██║
╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
"""

TAGLINE = "Refactor Kit - Systematic Refactoring Toolkit"

console = Console()

# Global debug flag
_debug_mode = False


def debug_print(message: str) -> None:
    """Print debug message if debug mode is enabled."""
    if _debug_mode:
        console.print(f"[dim][DEBUG][/dim] {message}")


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
        "requires_cli": False,
    },
}


class StepTracker:
    """Track and render hierarchical steps with tree structure."""

    def __init__(self, title: str):
        self.title = title
        self.steps = []  # list of dicts: {key, label, status, detail}
        self._refresh_cb = None

    def attach_refresh(self, refresh_callback):
        self._refresh_cb = refresh_callback

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return
        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception as e:
                debug_print(f"Exception in refresh callback: {e}")

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""
            status = step["status"]

            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree


def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    key = readchar.readkey()

    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return "up"
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return "down"
    if key == readchar.key.ENTER:
        return "enter"
    if key == readchar.key.ESC:
        return "escape"
    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key


def select_with_arrows(options: dict, prompt_text: str = "Select an option", default_key: str = None) -> str:
    """Interactive selection using arrow keys with Rich Live display."""
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    selected_key = None

    def create_selection_panel():
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")

        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")

        table.add_row("", "")
        table.add_row("", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")

        return Panel(table, title=f"[bold]{prompt_text}[/bold]", border_style="cyan", padding=(1, 2))

    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                try:
                    key = get_key()
                    if key == "up":
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == "down":
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == "enter":
                        selected_key = option_keys[selected_index]
                        break
                    elif key == "escape":
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    return selected_key


def show_banner():
    """Display the ASCII art banner."""
    banner_lines = BANNER.strip().split("\n")
    colors = ["bright_yellow", "yellow", "bright_red", "red", "bright_magenta", "magenta"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()


class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""

    def format_help(self, ctx, formatter):
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="refactor",
    help="Refactor Kit CLI - Bootstrap your projects for Refactoring-Driven Development",
    no_args_is_help=True,
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)


@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'refactor --help' for usage information[/dim]"))
        console.print()


def check_tool(tool: str, install_url: str = None, tracker: StepTracker = None) -> bool:
    """Check if a tool is installed and available in PATH."""
    result = shutil.which(tool)
    if result:
        if tracker:
            tracker.complete(tool, "available")
        else:
            console.print(f"  [green]✓[/green] {tool} found at {result}")
        return True
    else:
        if tracker:
            tracker.error(tool, "not found")
        else:
            console.print(f"  [red]✗[/red] {tool} not found")
            if install_url:
                console.print(f"    Install from: {install_url}")
        return False


def is_git_repo(path: Path = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()

    if not path.is_dir():
        return False

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            cwd=path,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def init_git_repo(project_path: Path, quiet: bool = False) -> Tuple[bool, Optional[str]]:
    """Initialize a git repository in the specified path."""
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        result = subprocess.run(["git", "init"], capture_output=True, text=True)
        if result.returncode != 0:
            error_msg = f"Command: git init\nExit code: {result.returncode}"
            if result.stderr:
                error_msg += f"\nError: {result.stderr.strip()}"
            if not quiet:
                console.print("[red]Error initializing git repository[/red]")
            return False, error_msg
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True, None
    finally:
        os.chdir(original_cwd)


@app.command()
def check():
    """Check for installed tools (git, AI agents, etc.)."""
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    tracker = StepTracker("Check Available Tools")

    # Check git
    tracker.add("git", "Git version control")
    git_ok = check_tool("git", tracker=tracker)

    # Check Python
    tracker.add("python", "Python runtime")
    python_ok = sys.version_info >= (3, 11)
    if python_ok:
        tracker.complete("python", f"v{sys.version_info.major}.{sys.version_info.minor}")
    else:
        tracker.error("python", f"v{sys.version_info.major}.{sys.version_info.minor} (3.11+ required)")

    # Check AI agents
    agent_results = {}
    for agent_key, config in AGENT_CONFIG.items():
        tracker.add(agent_key, config["name"])
        if config["requires_cli"]:
            agent_results[agent_key] = check_tool(agent_key, tracker=tracker)
        else:
            tracker.skip(agent_key, "IDE-based, no CLI check")
            agent_results[agent_key] = False

    console.print(tracker.render())

    console.print("\n[bold green]Refactor CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")

    if not any(agent_results.values()):
        console.print("[dim]Tip: Install an AI assistant for the best experience[/dim]")


@app.command()
def init(
    project_name: Optional[str] = typer.Argument(
        None, help="Name for your new project directory (use '.' for current directory)"
    ),
    ai_assistant: Optional[str] = typer.Option(
        None,
        "--ai",
        help=f"AI assistant to use: {', '.join(AGENT_CONFIG.keys())}",
    ),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory"),
    force: bool = typer.Option(
        False,
        "--force",
        help="Force merge/overwrite when initializing in current directory",
    ),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    ignore_agent_tools: bool = typer.Option(
        False, "--ignore-agent-tools", help="Skip checks for AI agent tools"
    ),
    debug: bool = typer.Option(
        False, "--debug", help="Show verbose diagnostic output for troubleshooting"
    ),
):
    """Initialize a new Refactor Kit project from the latest template."""
    global _debug_mode
    _debug_mode = debug

    show_banner()

    debug_print(f"Python version: {sys.version}")
    debug_print(f"Platform: {sys.platform}")
    debug_print(f"Current directory: {Path.cwd()}")

    # Handle project_name == "."
    if project_name == ".":
        here = True
        project_name = None

    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)

    if not here and not project_name:
        console.print("[red]Error:[/red] Must specify either a project name, use '.' for current directory, or use --here flag")
        raise typer.Exit(1)

    # Determine target directory
    debug_print(f"here={here}, project_name={project_name}")
    if here:
        project_name = Path.cwd().name
        target_dir = Path.cwd()

        # Check for non-empty directory
        existing_items = list(target_dir.iterdir())
        if existing_items:
            console.print(f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)")
            console.print("[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]")
            if force:
                console.print("[cyan]--force supplied: skipping confirmation and proceeding with merge[/cyan]")
            else:
                response = typer.confirm("Do you want to continue?")
                if not response:
                    console.print("[yellow]Operation cancelled[/yellow]")
                    raise typer.Exit(0)
    else:
        target_dir = Path.cwd() / project_name
        debug_print(f"Target directory (new): {target_dir}")
        if target_dir.exists() and not force:
            error_panel = Panel(
                f"Directory '[cyan]{project_name}[/cyan]' already exists\n"
                "Please choose a different project name or remove the existing directory.",
                title="[red]Directory Conflict[/red]",
                border_style="red",
                padding=(1, 2),
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    current_dir = Path.cwd()

    # Project setup summary panel
    setup_lines = [
        "[cyan]Refactor Kit Project Setup[/cyan]",
        "",
        f"{'Project':<15} [green]{target_dir.name}[/green]",
        f"{'Working Path':<15} [dim]{current_dir}[/dim]",
    ]
    if not here:
        setup_lines.append(f"{'Target Path':<15} [dim]{target_dir}[/dim]")

    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

    # Check for git
    should_init_git = False
    if not no_git:
        should_init_git = shutil.which("git") is not None
        if not should_init_git:
            console.print("[yellow]Git not found - will skip repository initialization[/yellow]")

    # AI assistant selection
    if ai_assistant:
        if ai_assistant not in AGENT_CONFIG:
            console.print(
                f"[red]Error:[/red] Invalid AI assistant '{ai_assistant}'. "
                f"Choose from: {', '.join(AGENT_CONFIG.keys())}"
            )
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        ai_choices = {key: config["name"] for key, config in AGENT_CONFIG.items()}
        selected_ai = select_with_arrows(ai_choices, "Choose your AI assistant:", "claude")

    # Check if CLI tool is available
    if not ignore_agent_tools:
        agent_config = AGENT_CONFIG.get(selected_ai)
        if agent_config and agent_config["requires_cli"]:
            install_url = agent_config["install_url"]
            if not shutil.which(selected_ai):
                error_panel = Panel(
                    f"[cyan]{selected_ai}[/cyan] not found\n"
                    f"Install from: [cyan]{install_url}[/cyan]\n"
                    f"{agent_config['name']} is required to continue with this project type.\n\n"
                    "Tip: Use [cyan]--ignore-agent-tools[/cyan] to skip this check",
                    title="[red]Agent Detection Error[/red]",
                    border_style="red",
                    padding=(1, 2),
                )
                console.print()
                console.print(error_panel)
                raise typer.Exit(1)

    console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_ai}")

    # Initialize step tracker
    tracker = StepTracker("Initialize Refactor Kit Project")

    tracker.add("precheck", "Check required tools")
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", "Select AI assistant")
    tracker.complete("ai-select", selected_ai)

    for key, label in [
        ("structure", "Create project structure"),
        ("agent-dir", "Set up agent commands directory"),
        ("gitignore", "Update .gitignore"),
        ("git", "Initialize git repository"),
        ("final", "Finalize"),
    ]:
        tracker.add(key, label)

    git_error_message = None

    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))

        try:
            # Create directory structure
            tracker.start("structure")
            target_dir.mkdir(parents=True, exist_ok=True)

            refactor_dir = target_dir / ".refactor"
            (refactor_dir / "memory").mkdir(parents=True, exist_ok=True)
            (refactor_dir / "templates").mkdir(parents=True, exist_ok=True)
            (refactor_dir / "refactorings").mkdir(parents=True, exist_ok=True)

            tracker.complete("structure", str(target_dir))

            # Set up AI agent commands
            tracker.start("agent-dir")
            config = AGENT_CONFIG[selected_ai]
            agent_dir = target_dir / config["folder"]
            agent_dir.mkdir(parents=True, exist_ok=True)
            tracker.complete("agent-dir", config["folder"])

            # Add agent folder to .gitignore for security
            tracker.start("gitignore")
            gitignore_path = target_dir / ".gitignore"
            # Get the root agent folder (e.g., ".claude" from ".claude/commands/")
            agent_root = config["folder"].split("/")[0]
            agent_pattern = f"{agent_root}/"

            if gitignore_path.exists():
                content = gitignore_path.read_text()
                if agent_pattern not in content:
                    with gitignore_path.open("a") as f:
                        f.write(f"\n# AI agent folder (may contain credentials)\n{agent_pattern}\n")
                    tracker.complete("gitignore", f"added {agent_pattern}")
                else:
                    tracker.complete("gitignore", "already configured")
            else:
                gitignore_path.write_text(f"# AI agent folder (may contain credentials)\n{agent_pattern}\n")
                tracker.complete("gitignore", f"created with {agent_pattern}")

            # Initialize git
            if not no_git:
                tracker.start("git")
                if is_git_repo(target_dir):
                    tracker.complete("git", "existing repo detected")
                elif should_init_git:
                    success, error_msg = init_git_repo(target_dir, quiet=True)
                    if success:
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                        git_error_message = error_msg
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            tracker.complete("final", "project ready")

        except Exception as e:
            tracker.error("final", str(e))
            console.print(Panel(f"Initialization failed: {e}", title="Failure", border_style="red"))
            if debug:
                env_pairs = [
                    ("Python", sys.version.split()[0]),
                    ("Platform", sys.platform),
                    ("CWD", str(Path.cwd())),
                ]
                label_width = max(len(k) for k, _ in env_pairs)
                env_lines = [f"{k.ljust(label_width)} → [bright_black]{v}[/bright_black]" for k, v in env_pairs]
                console.print(Panel("\n".join(env_lines), title="Debug Environment", border_style="magenta"))
            raise typer.Exit(1)

    # Print final tree
    console.print(tracker.render())
    console.print("\n[bold green]Project ready.[/bold green]")

    # Show git error details if initialization failed
    if git_error_message:
        console.print()
        git_error_panel = Panel(
            f"[yellow]Warning:[/yellow] Git repository initialization failed\n\n"
            f"{git_error_message}\n\n"
            f"[dim]You can initialize git manually later with:[/dim]\n"
            f"[cyan]cd {target_dir if not here else '.'}[/cyan]\n"
            f"[cyan]git init[/cyan]",
            title="[red]Git Initialization Failed[/red]",
            border_style="red",
            padding=(1, 2),
        )
        console.print(git_error_panel)

    # Agent folder security notice
    agent_config = AGENT_CONFIG.get(selected_ai)
    if agent_config:
        agent_folder = agent_config["folder"].rstrip("/")
        security_notice = Panel(
            f"Some agents may store credentials, auth tokens, or other identifying and private artifacts in the agent folder within your project.\n"
            f"Consider adding [cyan]{agent_folder}/[/cyan] (or parts of it) to [cyan].gitignore[/cyan] to prevent accidental credential leakage.",
            title="[yellow]Agent Folder Security[/yellow]",
            border_style="yellow",
            padding=(1, 2),
        )
        console.print()
        console.print(security_notice)

    # Next steps panel
    steps_lines = []
    if not here:
        steps_lines.append(f"1. Go to the project folder: [cyan]cd {project_name}[/cyan]")
        step_num = 2
    else:
        steps_lines.append("1. You're already in the project directory!")
        step_num = 2

    steps_lines.append(f"{step_num}. Start using slash commands with your AI agent:")
    steps_lines.append("   2.1 [cyan]/refactor.analyze[/] - Analyze your codebase")
    steps_lines.append("   2.2 [cyan]/refactor.strategy[/] - Define refactoring strategy")
    steps_lines.append("   2.3 [cyan]/refactor.plan[/] - Create implementation plan")
    steps_lines.append("   2.4 [cyan]/refactor.tasks[/] - Generate actionable tasks")
    steps_lines.append("   2.5 [cyan]/refactor.execute[/] - Execute refactoring")
    steps_lines.append("   2.6 [cyan]/refactor.verify[/] - Verify changes")

    steps_panel = Panel("\n".join(steps_lines), title="Next Steps", border_style="cyan", padding=(1, 2))
    console.print()
    console.print(steps_panel)

    # Enhancement commands panel
    enhancement_lines = [
        "Additional commands for systematic refactoring workflow",
        "",
        "○ [cyan]/refactor.constitution[/] - Establish project principles and guidelines",
    ]
    enhancements_panel = Panel(
        "\n".join(enhancement_lines), title="Enhancement Commands", border_style="cyan", padding=(1, 2)
    )
    console.print()
    console.print(enhancements_panel)


@app.command()
def version():
    """Show the version of Refactor CLI."""
    import platform

    show_banner()

    info_table = Table(show_header=False, box=None, padding=(0, 2))
    info_table.add_column("Key", style="cyan", justify="right")
    info_table.add_column("Value", style="white")

    info_table.add_row("CLI Version", __version__)
    info_table.add_row("", "")
    info_table.add_row("Python", platform.python_version())
    info_table.add_row("Platform", platform.system())
    info_table.add_row("Architecture", platform.machine())

    panel = Panel(
        info_table,
        title="[bold cyan]Refactor CLI Information[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    )

    console.print(panel)
    console.print()


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
