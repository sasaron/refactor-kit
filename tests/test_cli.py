"""Tests for the Refactor CLI."""

import sys
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from refactor_cli import AGENT_CONFIG, __version__, app

runner = CliRunner()


def mock_download_and_extract(project_path, ai_assistant, _is_current_dir=False, **_kwargs):
    """Mock function that creates the expected directory structure without downloading."""
    # Create the .refactor directory structure
    refactor_dir = project_path / ".refactor"
    refactor_dir.mkdir(parents=True, exist_ok=True)
    (refactor_dir / "memory").mkdir(exist_ok=True)
    (refactor_dir / "templates").mkdir(exist_ok=True)
    (refactor_dir / "refactorings").mkdir(exist_ok=True)

    # Create the agent-specific directory
    agent_folders = {
        "claude": ".claude/commands",
        "gemini": ".gemini/commands",
        "copilot": ".github/agents",
        "cursor-agent": ".cursor/commands",
    }
    if ai_assistant in agent_folders:
        agent_dir = project_path / agent_folders[ai_assistant]
        agent_dir.mkdir(parents=True, exist_ok=True)
        # Create a dummy command file
        (agent_dir / "refactor.start.md").write_text("# Start refactoring")

    return project_path


class TestVersion:
    """Tests for the version command."""

    def test_version_command(self):
        """Test that version command returns the correct version."""
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert __version__ in result.stdout


class TestCheck:
    """Tests for the check command."""

    def test_check_command_runs(self):
        """Test that check command runs without error."""
        result = runner.invoke(app, ["check"])
        assert result.exit_code == 0
        assert "Check Available Tools" in result.stdout


class TestInit:
    """Tests for the init command."""

    def test_init_requires_project_name_or_here(self):
        """Test that init fails without project name or --here flag."""
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 1
        assert "Error" in result.stdout

    def test_init_with_here_flag(self, tmp_path):
        """Test init with --here flag in empty directory."""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(app, ["init", "--here", "--ai", "claude", "--no-git"])
            assert result.exit_code == 0
            assert "Refactor Kit Project Setup" in result.stdout
            assert (tmp_path / ".refactor").exists()
            assert (tmp_path / ".refactor" / "memory").exists()

    def test_init_with_project_name(self, tmp_path):
        """Test init with project name."""
        project_name = "my-test-project"
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(app, ["init", project_name, "--ai", "claude", "--no-git"])
            assert result.exit_code == 0
            assert "Refactor Kit Project Setup" in result.stdout
            assert (tmp_path / project_name / ".refactor").exists()

    def test_init_with_dot_as_project_name(self, tmp_path):
        """Test init with '.' as project name."""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(app, ["init", ".", "--ai", "claude", "--no-git"])
            assert result.exit_code == 0
            assert (tmp_path / ".refactor").exists()

    def test_init_with_unknown_ai_assistant(self, tmp_path):
        """Test init fails with unknown AI assistant."""
        with patch("pathlib.Path.cwd", return_value=tmp_path):
            result = runner.invoke(app, ["init", "--here", "--ai", "unknown-agent", "--no-git"])
            assert result.exit_code == 1
            assert "Invalid AI assistant" in result.stdout

    def test_init_with_claude_assistant(self, tmp_path):
        """Test init with Claude AI assistant."""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(app, ["init", "--here", "--ai", "claude", "--no-git", "--ignore-agent-tools"])
            assert result.exit_code == 0
            assert (tmp_path / ".claude" / "commands").exists()

    def test_init_with_copilot_assistant(self, tmp_path):
        """Test init with GitHub Copilot AI assistant."""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(app, ["init", "--here", "--ai", "copilot", "--no-git", "--ignore-agent-tools"])
            assert result.exit_code == 0
            assert (tmp_path / ".github" / "agents").exists()

    def test_init_with_debug_flag(self, tmp_path):
        """Test init with --debug flag shows debug output."""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(app, ["init", "--here", "--ai", "claude", "--no-git", "--debug"])
            assert result.exit_code == 0
            assert "[DEBUG]" in result.stdout
            assert "Python version" in result.stdout


class TestAgentConfig:
    """Tests for agent configuration."""

    def test_all_agents_have_required_fields(self):
        """Test that all agents in config have required fields."""
        required_fields = ["name", "folder", "install_url", "requires_cli"]
        for agent_key, config in AGENT_CONFIG.items():
            for field in required_fields:
                assert field in config, f"Agent '{agent_key}' missing field '{field}'"

    def test_agent_folders_are_valid_paths(self):
        """Test that agent folders are valid path strings."""
        for agent_key, config in AGENT_CONFIG.items():
            folder = config["folder"]
            assert isinstance(folder, str), f"Agent '{agent_key}' folder is not a string"
            assert folder.startswith("."), f"Agent '{agent_key}' folder should start with '.'"

    def test_cli_agents_have_install_urls(self):
        """Test that CLI-based agents have install URLs."""
        for agent_key, config in AGENT_CONFIG.items():
            if config["requires_cli"]:
                assert config["install_url"] is not None, f"CLI agent '{agent_key}' should have install_url"
