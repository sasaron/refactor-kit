"""Tests for the Refactor CLI."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from refactor_cli import (
    AGENT_CONFIG,
    StepTracker,
    __version__,
    _extract_and_merge_to_current_dir,
    _extract_to_new_directory,
    _format_rate_limit_error,
    _get_http_client,
    _get_source_dir_from_extracted,
    _github_auth_headers,
    _github_token,
    _merge_item_to_dest,
    _parse_rate_limit_headers,
    app,
    check_tool,
    debug_print,
    ensure_executable_scripts,
    get_key,
    handle_vscode_settings,
    init_git_repo,
    is_git_repo,
    merge_json_files,
    select_with_arrows,
    show_banner,
)

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
            result = runner.invoke(app, ["init", "--here", "--ai", "claude", "--no-git", "--ignore-agent-tools"])
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
            result = runner.invoke(app, ["init", project_name, "--ai", "claude", "--no-git", "--ignore-agent-tools"])
            assert result.exit_code == 0
            assert "Refactor Kit Project Setup" in result.stdout
            assert (tmp_path / project_name / ".refactor").exists()

    def test_init_with_dot_as_project_name(self, tmp_path):
        """Test init with '.' as project name."""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(app, ["init", ".", "--ai", "claude", "--no-git", "--ignore-agent-tools"])
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
            result = runner.invoke(
                app, ["init", "--here", "--ai", "claude", "--no-git", "--ignore-agent-tools", "--debug"]
            )
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


class TestInitAllAgents:
    """Tests for init command with all AI agents."""

    @pytest.mark.parametrize(
        ("agent_key", "expected_folder"),
        [
            ("claude", ".claude/commands"),
            ("gemini", ".gemini/commands"),
            ("copilot", ".github/agents"),
            ("cursor-agent", ".cursor/commands"),
        ],
    )
    def test_init_creates_agent_folder(self, tmp_path, agent_key, expected_folder):
        """Test that init creates the correct agent folder for each AI assistant."""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(
                app, ["init", "--here", "--ai", agent_key, "--no-git", "--ignore-agent-tools"]
            )
            assert result.exit_code == 0, f"init failed for {agent_key}: {result.stdout}"
            agent_path = tmp_path / expected_folder
            assert agent_path.exists(), f"Agent folder {expected_folder} not created for {agent_key}"

    @pytest.mark.parametrize("agent_key", list(AGENT_CONFIG.keys()))
    def test_init_agent_folder_matches_config(self, tmp_path, agent_key):
        """Test that the created agent folder matches AGENT_CONFIG."""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(
                app, ["init", "--here", "--ai", agent_key, "--no-git", "--ignore-agent-tools"]
            )
            assert result.exit_code == 0, f"init failed for {agent_key}: {result.stdout}"

            # Get expected folder from AGENT_CONFIG (strip trailing slash)
            expected_folder = AGENT_CONFIG[agent_key]["folder"].rstrip("/")
            agent_path = tmp_path / expected_folder
            assert agent_path.exists(), (
                f"Agent folder mismatch for {agent_key}: "
                f"expected {expected_folder}, but it doesn't exist"
            )

    @pytest.mark.parametrize("agent_key", list(AGENT_CONFIG.keys()))
    def test_init_creates_refactor_directory(self, tmp_path, agent_key):
        """Test that init creates .refactor directory for all agents."""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(
                app, ["init", "--here", "--ai", agent_key, "--no-git", "--ignore-agent-tools"]
            )
            assert result.exit_code == 0
            assert (tmp_path / ".refactor").exists(), f".refactor not created for {agent_key}"
            assert (tmp_path / ".refactor" / "memory").exists()
            assert (tmp_path / ".refactor" / "templates").exists()
            assert (tmp_path / ".refactor" / "refactorings").exists()

    @pytest.mark.parametrize(
        ("agent_key", "expected_folder"),
        [
            ("claude", ".claude/commands"),
            ("gemini", ".gemini/commands"),
            ("copilot", ".github/agents"),
            ("cursor-agent", ".cursor/commands"),
        ],
    )
    def test_init_with_project_name_creates_agent_folder(self, tmp_path, agent_key, expected_folder):
        """Test that init with project name creates agent folder in new directory."""
        project_name = "test-project"
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(
                app, ["init", project_name, "--ai", agent_key, "--no-git", "--ignore-agent-tools"]
            )
            assert result.exit_code == 0, f"init failed for {agent_key}: {result.stdout}"
            project_path = tmp_path / project_name
            agent_path = project_path / expected_folder
            assert agent_path.exists(), f"Agent folder {expected_folder} not created for {agent_key}"


class TestGitHubTokenUtils:
    """Tests for GitHub token utility functions."""

    def test_github_token_returns_cli_token_when_provided(self):
        """Test that CLI token takes precedence."""
        result = _github_token(cli_token="cli-token-123")
        assert result == "cli-token-123"

    def test_github_token_returns_env_gh_token(self, monkeypatch):
        """Test that GH_TOKEN env var is used when no CLI token."""
        monkeypatch.setenv("GH_TOKEN", "gh-token-456")
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        result = _github_token()
        assert result == "gh-token-456"

    def test_github_token_returns_env_github_token(self, monkeypatch):
        """Test that GITHUB_TOKEN env var is used as fallback."""
        monkeypatch.delenv("GH_TOKEN", raising=False)
        monkeypatch.setenv("GITHUB_TOKEN", "github-token-789")
        result = _github_token()
        assert result == "github-token-789"

    def test_github_token_prefers_gh_token_over_github_token(self, monkeypatch):
        """Test that GH_TOKEN takes precedence over GITHUB_TOKEN."""
        monkeypatch.setenv("GH_TOKEN", "gh-token")
        monkeypatch.setenv("GITHUB_TOKEN", "github-token")
        result = _github_token()
        assert result == "gh-token"

    def test_github_token_returns_none_when_empty(self, monkeypatch):
        """Test that None is returned when no token is available."""
        monkeypatch.delenv("GH_TOKEN", raising=False)
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        result = _github_token()
        assert result is None

    def test_github_token_strips_whitespace(self, monkeypatch):
        """Test that tokens are stripped of whitespace."""
        monkeypatch.setenv("GH_TOKEN", "  token-with-spaces  ")
        result = _github_token()
        assert result == "token-with-spaces"

    def test_github_token_returns_none_for_whitespace_only(self, monkeypatch):
        """Test that whitespace-only tokens return None."""
        monkeypatch.setenv("GH_TOKEN", "   ")
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        result = _github_token()
        assert result is None

    def test_github_auth_headers_with_token(self):
        """Test that auth headers are generated with token."""
        headers = _github_auth_headers(cli_token="test-token")
        assert headers == {"Authorization": "Bearer test-token"}

    def test_github_auth_headers_without_token(self, monkeypatch):
        """Test that empty dict is returned without token."""
        monkeypatch.delenv("GH_TOKEN", raising=False)
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        headers = _github_auth_headers()
        assert headers == {}


class TestRateLimitParsing:
    """Tests for rate limit header parsing."""

    def test_parse_rate_limit_headers_full(self):
        """Test parsing complete rate limit headers."""
        from httpx import Headers

        headers = Headers(
            {
                "X-RateLimit-Limit": "60",
                "X-RateLimit-Remaining": "59",
                "X-RateLimit-Reset": "1700000000",
            }
        )
        result = _parse_rate_limit_headers(headers)
        assert result["limit"] == "60"
        assert result["remaining"] == "59"
        assert result["reset_epoch"] == 1700000000
        assert "reset_time" in result
        assert "reset_local" in result

    def test_parse_rate_limit_headers_partial(self):
        """Test parsing partial rate limit headers."""
        from httpx import Headers

        headers = Headers({"X-RateLimit-Remaining": "10"})
        result = _parse_rate_limit_headers(headers)
        assert result["remaining"] == "10"
        assert "limit" not in result

    def test_parse_rate_limit_headers_empty(self):
        """Test parsing empty headers."""
        from httpx import Headers

        headers = Headers({})
        result = _parse_rate_limit_headers(headers)
        assert result == {}

    def test_parse_rate_limit_headers_with_retry_after(self):
        """Test parsing headers with Retry-After."""
        from httpx import Headers

        headers = Headers({"Retry-After": "120"})
        result = _parse_rate_limit_headers(headers)
        assert result["retry_after_seconds"] == 120


class TestGitUtils:
    """Tests for git utility functions."""

    def test_is_git_repo_true(self, tmp_path):
        """Test is_git_repo returns True for git repository."""
        import subprocess

        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        assert is_git_repo(tmp_path) is True

    def test_is_git_repo_false(self, tmp_path):
        """Test is_git_repo returns False for non-git directory."""
        assert is_git_repo(tmp_path) is False

    def test_is_git_repo_default_cwd(self):
        """Test is_git_repo uses cwd by default."""
        # This test runs in the refactor-kit repo which is a git repo
        result = is_git_repo()
        assert isinstance(result, bool)

    def test_is_git_repo_nonexistent_path(self, tmp_path):
        """Test is_git_repo returns False for nonexistent path."""
        nonexistent = tmp_path / "does-not-exist"
        assert is_git_repo(nonexistent) is False

    def test_init_git_repo_success(self, tmp_path):
        """Test successful git repository initialization."""
        success, _error = init_git_repo(tmp_path, quiet=True)
        assert success is True
        assert _error is None
        assert (tmp_path / ".git").exists()

    def test_init_git_repo_already_initialized(self, tmp_path):
        """Test init_git_repo on already initialized repo."""
        import subprocess

        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        # Running init again should still succeed
        success, _error = init_git_repo(tmp_path, quiet=True)
        assert success is True


class TestMergeJsonFiles:
    """Tests for JSON file merging."""

    def test_merge_json_files_simple(self, tmp_path):
        """Test simple JSON merge."""
        import json

        existing_file = tmp_path / "existing.json"
        existing_file.write_text(json.dumps({"key1": "value1"}))

        new_content = {"key2": "value2"}
        result = merge_json_files(existing_file, new_content)

        assert result["key1"] == "value1"
        assert result["key2"] == "value2"

    def test_merge_json_files_override(self, tmp_path):
        """Test JSON merge with override."""
        import json

        existing_file = tmp_path / "existing.json"
        existing_file.write_text(json.dumps({"key": "old"}))

        new_content = {"key": "new"}
        result = merge_json_files(existing_file, new_content)

        assert result["key"] == "new"

    def test_merge_json_files_nested(self, tmp_path):
        """Test deep merge of nested JSON."""
        import json

        existing_file = tmp_path / "existing.json"
        existing_file.write_text(
            json.dumps({"parent": {"child1": "value1", "child2": "value2"}})
        )

        new_content = {"parent": {"child2": "updated", "child3": "value3"}}
        result = merge_json_files(existing_file, new_content)

        assert result["parent"]["child1"] == "value1"
        assert result["parent"]["child2"] == "updated"
        assert result["parent"]["child3"] == "value3"

    def test_merge_json_files_nonexistent(self, tmp_path):
        """Test merge with nonexistent file returns new content."""
        nonexistent = tmp_path / "nonexistent.json"
        new_content = {"key": "value"}
        result = merge_json_files(nonexistent, new_content)
        assert result == new_content

    def test_merge_json_files_invalid_json(self, tmp_path):
        """Test merge with invalid JSON file returns new content."""
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("not valid json")
        new_content = {"key": "value"}
        result = merge_json_files(invalid_file, new_content)
        assert result == new_content


class TestStepTracker:
    """Tests for StepTracker class."""

    def test_step_tracker_init(self):
        """Test StepTracker initialization."""
        tracker = StepTracker("Test Title")
        assert tracker.title == "Test Title"
        assert tracker.steps == []

    def test_step_tracker_add(self):
        """Test adding steps to tracker."""
        tracker = StepTracker("Test")
        tracker.add("step1", "First Step")
        assert len(tracker.steps) == 1
        assert tracker.steps[0]["key"] == "step1"
        assert tracker.steps[0]["label"] == "First Step"
        assert tracker.steps[0]["status"] == "pending"

    def test_step_tracker_no_duplicate_add(self):
        """Test that duplicate keys are not added."""
        tracker = StepTracker("Test")
        tracker.add("step1", "First")
        tracker.add("step1", "Duplicate")
        assert len(tracker.steps) == 1
        assert tracker.steps[0]["label"] == "First"

    def test_step_tracker_start(self):
        """Test starting a step."""
        tracker = StepTracker("Test")
        tracker.add("step1", "Step 1")
        tracker.start("step1", "in progress")
        assert tracker.steps[0]["status"] == "running"
        assert tracker.steps[0]["detail"] == "in progress"

    def test_step_tracker_complete(self):
        """Test completing a step."""
        tracker = StepTracker("Test")
        tracker.add("step1", "Step 1")
        tracker.complete("step1", "done")
        assert tracker.steps[0]["status"] == "done"
        assert tracker.steps[0]["detail"] == "done"

    def test_step_tracker_error(self):
        """Test marking step as error."""
        tracker = StepTracker("Test")
        tracker.add("step1", "Step 1")
        tracker.error("step1", "failed")
        assert tracker.steps[0]["status"] == "error"
        assert tracker.steps[0]["detail"] == "failed"

    def test_step_tracker_skip(self):
        """Test skipping a step."""
        tracker = StepTracker("Test")
        tracker.add("step1", "Step 1")
        tracker.skip("step1", "not needed")
        assert tracker.steps[0]["status"] == "skipped"
        assert tracker.steps[0]["detail"] == "not needed"

    def test_step_tracker_render(self):
        """Test rendering the tracker."""
        tracker = StepTracker("Test Title")
        tracker.add("step1", "Step 1")
        tracker.complete("step1")
        tree = tracker.render()
        # Just verify it returns a Tree object without error
        assert tree is not None

    def test_step_tracker_update_nonexistent_creates_step(self):
        """Test that updating nonexistent step creates it."""
        tracker = StepTracker("Test")
        tracker.complete("new_step", "created")
        assert len(tracker.steps) == 1
        assert tracker.steps[0]["key"] == "new_step"
        assert tracker.steps[0]["status"] == "done"


class TestInitEdgeCases:
    """Tests for init command edge cases."""

    def test_init_directory_already_exists_without_force(self, tmp_path):
        """Test that init fails when directory exists without --force."""
        project_name = "existing-project"
        (tmp_path / project_name).mkdir()

        with patch("pathlib.Path.cwd", return_value=tmp_path):
            result = runner.invoke(
                app, ["init", project_name, "--ai", "claude", "--no-git", "--ignore-agent-tools"]
            )
            assert result.exit_code == 1
            assert "Directory Conflict" in result.stdout or "already exists" in result.stdout

    def test_init_with_force_in_nonempty_dir(self, tmp_path):
        """Test init with --force in non-empty directory."""
        # Create some existing files
        (tmp_path / "existing.txt").write_text("existing content")

        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(
                app, ["init", "--here", "--force", "--ai", "claude", "--no-git", "--ignore-agent-tools"]
            )
            assert result.exit_code == 0
            # Existing file should still be there
            assert (tmp_path / "existing.txt").exists()
            # New structure should be created
            assert (tmp_path / ".refactor").exists()

    def test_init_both_project_name_and_here_flag_fails(self, tmp_path):
        """Test that specifying both project name and --here fails."""
        with patch("pathlib.Path.cwd", return_value=tmp_path):
            result = runner.invoke(
                app, ["init", "project-name", "--here", "--ai", "claude"]
            )
            assert result.exit_code == 1
            assert "Cannot specify both" in result.stdout

    def test_init_cli_agent_not_installed(self, tmp_path):
        """Test that init fails when CLI agent is not installed (without --ignore-agent-tools)."""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("shutil.which", return_value=None),
        ):
            result = runner.invoke(
                app, ["init", "--here", "--ai", "claude", "--no-git"]
            )
            assert result.exit_code == 1
            assert "Agent Detection Error" in result.stdout or "not found" in result.stdout

    def test_init_git_already_initialized(self, tmp_path):
        """Test init in directory that is already a git repo detects existing repo."""
        import subprocess

        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)

        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            # --force is needed because git init creates .git directory making it non-empty
            result = runner.invoke(
                app, ["init", "--here", "--force", "--ai", "claude", "--ignore-agent-tools"]
            )
            assert result.exit_code == 0
            assert "existing repo detected" in result.stdout

    def test_init_shows_security_notice(self, tmp_path):
        """Test that init shows agent folder security notice."""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(
                app, ["init", "--here", "--ai", "claude", "--no-git", "--ignore-agent-tools"]
            )
            assert result.exit_code == 0
            assert "Agent Folder Security" in result.stdout

    def test_init_shows_next_steps(self, tmp_path):
        """Test that init shows next steps panel."""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(
                app, ["init", "--here", "--ai", "claude", "--no-git", "--ignore-agent-tools"]
            )
            assert result.exit_code == 0
            assert "Next Steps" in result.stdout


class TestFormatRateLimitError:
    """Tests for rate limit error formatting."""

    def test_format_rate_limit_error_basic(self):
        """Test basic error message formatting."""
        from httpx import Headers

        headers = Headers({})
        result = _format_rate_limit_error(403, headers, "https://api.github.com/test")
        assert "403" in result
        assert "https://api.github.com/test" in result
        assert "Troubleshooting Tips" in result

    def test_format_rate_limit_error_with_rate_info(self):
        """Test error message with rate limit information."""
        from httpx import Headers

        headers = Headers(
            {
                "X-RateLimit-Limit": "60",
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": "1700000000",
            }
        )
        result = _format_rate_limit_error(429, headers, "https://api.github.com/test")
        assert "Rate Limit Information" in result
        assert "60 requests/hour" in result
        assert "Remaining: 0" in result

    def test_format_rate_limit_error_with_retry_after(self):
        """Test error message with Retry-After header."""
        from httpx import Headers

        headers = Headers({"Retry-After": "300"})
        result = _format_rate_limit_error(429, headers, "https://api.github.com/test")
        assert "Retry after: 300 seconds" in result


class TestHttpClient:
    """Tests for HTTP client creation."""

    def test_get_http_client_default(self):
        """Test getting default HTTP client."""
        import refactor_cli

        # Reset the global client
        refactor_cli._http_client = None
        client = _get_http_client(skip_tls=False)
        assert client is not None
        # Clean up
        client.close()
        refactor_cli._http_client = None

    def test_get_http_client_skip_tls(self):
        """Test getting HTTP client with TLS verification skipped."""
        client = _get_http_client(skip_tls=True)
        assert client is not None
        client.close()

    def test_get_http_client_reuses_instance(self):
        """Test that HTTP client is reused."""
        import refactor_cli

        refactor_cli._http_client = None
        client1 = _get_http_client(skip_tls=False)
        client2 = _get_http_client(skip_tls=False)
        assert client1 is client2
        client1.close()
        refactor_cli._http_client = None


class TestCheckTool:
    """Tests for check_tool function."""

    def test_check_tool_found(self):
        """Test check_tool when tool is found."""
        # git should be available in most environments
        result = check_tool("git")
        assert result is True

    def test_check_tool_not_found(self):
        """Test check_tool when tool is not found."""
        result = check_tool("nonexistent-tool-xyz123")
        assert result is False

    def test_check_tool_with_tracker_found(self):
        """Test check_tool with tracker when found."""
        tracker = StepTracker("Test")
        tracker.add("git", "Git")
        result = check_tool("git", tracker=tracker)
        assert result is True
        assert tracker.steps[0]["status"] == "done"

    def test_check_tool_with_tracker_not_found(self):
        """Test check_tool with tracker when not found."""
        tracker = StepTracker("Test")
        tracker.add("nonexistent-tool-xyz123", "Nonexistent")
        result = check_tool("nonexistent-tool-xyz123", tracker=tracker)
        assert result is False
        assert tracker.steps[0]["status"] == "error"


class TestHandleVscodeSettings:
    """Tests for VSCode settings handling."""

    def test_handle_vscode_settings_new_file(self, tmp_path):
        """Test handling VSCode settings when no existing file."""
        import json

        # Create source settings
        vscode_dir = tmp_path / "source" / ".vscode"
        vscode_dir.mkdir(parents=True)
        source_settings = vscode_dir / "settings.json"
        source_settings.write_text(json.dumps({"editor.fontSize": 14}))

        # Create destination directory
        dest_vscode = tmp_path / "dest" / ".vscode"
        dest_vscode.mkdir(parents=True)
        dest_settings = dest_vscode / "settings.json"

        handle_vscode_settings(
            source_settings, dest_settings, Path(".vscode/settings.json")
        )

        assert dest_settings.exists()
        content = json.loads(dest_settings.read_text())
        assert content["editor.fontSize"] == 14

    def test_handle_vscode_settings_merge(self, tmp_path):
        """Test merging VSCode settings with existing file."""
        import json

        # Create source settings
        vscode_dir = tmp_path / "source" / ".vscode"
        vscode_dir.mkdir(parents=True)
        source_settings = vscode_dir / "settings.json"
        source_settings.write_text(json.dumps({"editor.fontSize": 14}))

        # Create existing destination settings
        dest_vscode = tmp_path / "dest" / ".vscode"
        dest_vscode.mkdir(parents=True)
        dest_settings = dest_vscode / "settings.json"
        dest_settings.write_text(json.dumps({"editor.tabSize": 2}))

        handle_vscode_settings(
            source_settings, dest_settings, Path(".vscode/settings.json")
        )

        content = json.loads(dest_settings.read_text())
        assert content["editor.fontSize"] == 14
        assert content["editor.tabSize"] == 2


class TestEnsureExecutableScripts:
    """Tests for ensure_executable_scripts function."""

    def test_ensure_executable_scripts_no_scripts_dir(self, tmp_path):
        """Test when .refactor/scripts doesn't exist."""
        # Should not raise any errors
        ensure_executable_scripts(tmp_path)

    def test_ensure_executable_scripts_with_scripts(self, tmp_path):
        """Test setting executable permissions on scripts."""
        import os
        import stat

        # Create scripts directory with a shell script
        scripts_dir = tmp_path / ".refactor" / "scripts"
        scripts_dir.mkdir(parents=True)
        script = scripts_dir / "test.sh"
        script.write_text("#!/bin/bash\necho hello")

        # Remove execute permissions
        os.chmod(script, stat.S_IRUSR | stat.S_IWUSR)

        ensure_executable_scripts(tmp_path)

        # Check that execute bit is set
        mode = script.stat().st_mode
        assert mode & stat.S_IXUSR  # Owner execute bit

    def test_ensure_executable_scripts_nested(self, tmp_path):
        """Test setting permissions on nested scripts."""
        import os
        import stat

        # Create nested scripts
        scripts_dir = tmp_path / ".refactor" / "scripts" / "subdir"
        scripts_dir.mkdir(parents=True)
        script = scripts_dir / "nested.sh"
        script.write_text("#!/bin/bash\necho nested")
        os.chmod(script, stat.S_IRUSR | stat.S_IWUSR)

        ensure_executable_scripts(tmp_path)

        mode = script.stat().st_mode
        assert mode & stat.S_IXUSR

    def test_ensure_executable_scripts_with_tracker(self, tmp_path):
        """Test with StepTracker."""
        scripts_dir = tmp_path / ".refactor" / "scripts"
        scripts_dir.mkdir(parents=True)
        script = scripts_dir / "test.sh"
        script.write_text("#!/bin/bash\necho hello")

        tracker = StepTracker("Test")
        ensure_executable_scripts(tmp_path, tracker=tracker)

        # Tracker should have chmod step
        chmod_steps = [s for s in tracker.steps if s["key"] == "chmod"]
        assert len(chmod_steps) == 1


class TestDebugPrint:
    """Tests for debug_print function."""

    def test_debug_print_enabled(self):
        """Test debug print when enabled."""
        import refactor_cli

        original = refactor_cli._debug_mode
        refactor_cli._debug_mode = True
        try:
            debug_print("test message")
            # Output goes to rich console, just verify no error
        finally:
            refactor_cli._debug_mode = original

    def test_debug_print_disabled(self):
        """Test debug print when disabled."""
        import refactor_cli

        original = refactor_cli._debug_mode
        refactor_cli._debug_mode = False
        try:
            debug_print("test message")
            # Should produce no output
        finally:
            refactor_cli._debug_mode = original


class TestShowBanner:
    """Tests for show_banner function."""

    def test_show_banner_runs(self):
        """Test that show_banner executes without error."""
        # Just verify it doesn't raise
        show_banner()


class TestStepTrackerRenderVariants:
    """Additional tests for StepTracker render with different states."""

    def test_render_pending_with_detail(self):
        """Test rendering pending step with detail."""
        tracker = StepTracker("Test")
        tracker.add("step1", "Step 1")
        tracker.steps[0]["detail"] = "waiting"
        tree = tracker.render()
        assert tree is not None

    def test_render_running_step(self):
        """Test rendering running step."""
        tracker = StepTracker("Test")
        tracker.add("step1", "Step 1")
        tracker.start("step1", "processing")
        tree = tracker.render()
        assert tree is not None

    def test_render_error_step(self):
        """Test rendering error step."""
        tracker = StepTracker("Test")
        tracker.add("step1", "Step 1")
        tracker.error("step1", "failed!")
        tree = tracker.render()
        assert tree is not None

    def test_render_skipped_step(self):
        """Test rendering skipped step."""
        tracker = StepTracker("Test")
        tracker.add("step1", "Step 1")
        tracker.skip("step1", "not needed")
        tree = tracker.render()
        assert tree is not None

    def test_render_multiple_steps(self):
        """Test rendering multiple steps with different states."""
        tracker = StepTracker("Multi-step Test")
        tracker.add("step1", "Step 1")
        tracker.add("step2", "Step 2")
        tracker.add("step3", "Step 3")
        tracker.add("step4", "Step 4")
        tracker.complete("step1", "done")
        tracker.start("step2", "in progress")
        tracker.error("step3", "failed")
        tracker.skip("step4", "skipped")
        tree = tracker.render()
        assert tree is not None

    def test_attach_refresh_callback(self):
        """Test attaching refresh callback."""
        tracker = StepTracker("Test")
        callback_called = []

        def callback():
            callback_called.append(True)

        tracker.attach_refresh(callback)
        tracker.add("step1", "Step 1")
        assert len(callback_called) == 1

    def test_refresh_callback_exception_handled(self):
        """Test that exceptions in refresh callback are handled."""
        tracker = StepTracker("Test")

        def bad_callback():
            raise ValueError("test error")

        tracker.attach_refresh(bad_callback)
        # Should not raise
        tracker.add("step1", "Step 1")


class TestInitGitRepoEdgeCases:
    """Additional edge case tests for init_git_repo."""

    def test_init_git_repo_verbose(self, tmp_path):
        """Test init_git_repo with verbose output."""
        success, _error = init_git_repo(tmp_path, quiet=False)
        assert success is True
        assert (tmp_path / ".git").exists()


class TestRateLimitHeadersEdgeCases:
    """Additional tests for rate limit header parsing."""

    def test_parse_invalid_retry_after(self):
        """Test parsing non-numeric Retry-After."""
        from httpx import Headers

        headers = Headers({"Retry-After": "not-a-number"})
        result = _parse_rate_limit_headers(headers)
        assert "retry_after" in result
        assert result["retry_after"] == "not-a-number"

    def test_parse_zero_reset_epoch(self):
        """Test parsing zero reset epoch."""
        from httpx import Headers

        headers = Headers({"X-RateLimit-Reset": "0"})
        result = _parse_rate_limit_headers(headers)
        # Zero epoch should not produce reset_time
        assert "reset_time" not in result


class TestMergeItemToDest:
    """Tests for _merge_item_to_dest function."""

    def test_merge_file_to_dest(self, tmp_path):
        """Test merging a single file."""
        src = tmp_path / "source"
        src.mkdir()
        src_file = src / "test.txt"
        src_file.write_text("source content")

        dest = tmp_path / "dest"
        dest.mkdir()
        dest_file = dest / "test.txt"

        _merge_item_to_dest(src_file, dest_file, verbose=False, tracker=None)
        assert dest_file.exists()
        assert dest_file.read_text() == "source content"

    def test_merge_directory_to_dest_new(self, tmp_path):
        """Test merging a directory to non-existing dest."""
        src_dir = tmp_path / "source_dir"
        src_dir.mkdir()
        (src_dir / "file1.txt").write_text("content1")

        dest_dir = tmp_path / "dest_dir"

        _merge_item_to_dest(src_dir, dest_dir, verbose=False, tracker=None)
        assert dest_dir.exists()
        assert (dest_dir / "file1.txt").exists()

    def test_merge_directory_to_existing(self, tmp_path):
        """Test merging directory to existing dest."""
        src_dir = tmp_path / "source_dir"
        src_dir.mkdir()
        (src_dir / "new_file.txt").write_text("new content")

        dest_dir = tmp_path / "dest_dir"
        dest_dir.mkdir()
        (dest_dir / "existing.txt").write_text("existing")

        _merge_item_to_dest(src_dir, dest_dir, verbose=True, tracker=None)
        assert (dest_dir / "new_file.txt").exists()
        assert (dest_dir / "existing.txt").exists()

    def test_merge_file_overwrite(self, tmp_path):
        """Test overwriting existing file."""
        src_file = tmp_path / "src.txt"
        src_file.write_text("new")

        dest_file = tmp_path / "dest.txt"
        dest_file.write_text("old")

        _merge_item_to_dest(src_file, dest_file, verbose=True, tracker=None)
        assert dest_file.read_text() == "new"


class TestGetSourceDirFromExtracted:
    """Tests for _get_source_dir_from_extracted function."""

    def test_single_nested_directory(self, tmp_path):
        """Test flattening single nested directory."""
        nested = tmp_path / "nested"
        nested.mkdir()
        (nested / "file.txt").write_text("content")

        result = _get_source_dir_from_extracted([nested], tmp_path, verbose=False, tracker=None)
        assert result == nested

    def test_multiple_items(self, tmp_path):
        """Test multiple items - should return base path."""
        (tmp_path / "file1.txt").write_text("1")
        (tmp_path / "file2.txt").write_text("2")
        items = list(tmp_path.iterdir())

        result = _get_source_dir_from_extracted(items, tmp_path, verbose=False, tracker=None)
        assert result == tmp_path

    def test_single_file_not_flattened(self, tmp_path):
        """Test single file is not treated as nested dir."""
        single_file = tmp_path / "single.txt"
        single_file.write_text("content")

        result = _get_source_dir_from_extracted([single_file], tmp_path, verbose=False, tracker=None)
        assert result == tmp_path

    def test_with_tracker(self, tmp_path):
        """Test with tracker enabled."""
        nested = tmp_path / "nested"
        nested.mkdir()

        tracker = StepTracker("Test")
        result = _get_source_dir_from_extracted([nested], tmp_path, verbose=False, tracker=tracker)
        assert result == nested


class TestExtractFunctions:
    """Tests for extraction functions."""

    def test_extract_and_merge_to_current_dir(self, tmp_path):
        """Test extracting and merging to current directory."""
        import zipfile

        # Create a test ZIP file
        zip_path = tmp_path / "test.zip"
        content_dir = tmp_path / "content"
        content_dir.mkdir()
        (content_dir / "file.txt").write_text("test content")

        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.write(content_dir / "file.txt", "file.txt")

        dest_dir = tmp_path / "dest"
        dest_dir.mkdir()

        with zipfile.ZipFile(zip_path, "r") as zf:
            _extract_and_merge_to_current_dir(zf, dest_dir, verbose=False, tracker=None)

        assert (dest_dir / "file.txt").exists()

    def test_extract_to_new_directory(self, tmp_path):
        """Test extracting to new directory."""
        import zipfile

        # Create a test ZIP file
        zip_path = tmp_path / "test.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("file.txt", "test content")

        dest_dir = tmp_path / "new_dest"
        dest_dir.mkdir()

        with zipfile.ZipFile(zip_path, "r") as zf:
            _extract_to_new_directory(zf, dest_dir, verbose=False, tracker=None)

        assert (dest_dir / "file.txt").exists()

    def test_extract_to_new_directory_with_nested(self, tmp_path):
        """Test extracting nested directory to new location."""
        import zipfile

        # Create a ZIP with nested directory structure
        zip_path = tmp_path / "test.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("nested_dir/file.txt", "test content")

        dest_dir = tmp_path / "new_dest"
        dest_dir.mkdir()

        with zipfile.ZipFile(zip_path, "r") as zf:
            _extract_to_new_directory(zf, dest_dir, verbose=True, tracker=None)

        # After flattening, file should be directly in dest_dir
        assert (dest_dir / "file.txt").exists()

    def test_extract_with_tracker(self, tmp_path):
        """Test extraction with tracker."""
        import zipfile

        zip_path = tmp_path / "test.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("file.txt", "content")

        dest_dir = tmp_path / "dest"
        dest_dir.mkdir()
        tracker = StepTracker("Test")

        with zipfile.ZipFile(zip_path, "r") as zf:
            _extract_and_merge_to_current_dir(zf, dest_dir, verbose=False, tracker=tracker)


class TestGetKey:
    """Tests for get_key function."""

    def test_get_key_up(self):
        """Test get_key returns 'up' for UP key."""
        import readchar

        with patch.object(readchar, "readkey", return_value=readchar.key.UP):
            result = get_key()
            assert result == "up"

    def test_get_key_down(self):
        """Test get_key returns 'down' for DOWN key."""
        import readchar

        with patch.object(readchar, "readkey", return_value=readchar.key.DOWN):
            result = get_key()
            assert result == "down"

    def test_get_key_enter(self):
        """Test get_key returns 'enter' for ENTER key."""
        import readchar

        with patch.object(readchar, "readkey", return_value=readchar.key.ENTER):
            result = get_key()
            assert result == "enter"

    def test_get_key_escape(self):
        """Test get_key returns 'escape' for ESC key."""
        import readchar

        with patch.object(readchar, "readkey", return_value=readchar.key.ESC):
            result = get_key()
            assert result == "escape"

    def test_get_key_ctrl_c_raises(self):
        """Test get_key raises KeyboardInterrupt for Ctrl+C."""
        import readchar

        with (
            patch.object(readchar, "readkey", return_value=readchar.key.CTRL_C),
            pytest.raises(KeyboardInterrupt),
        ):
            get_key()

    def test_get_key_other_returns_key(self):
        """Test get_key returns the key for other keys."""
        import readchar

        with patch.object(readchar, "readkey", return_value="x"):
            result = get_key()
            assert result == "x"

    def test_get_key_ctrl_p_is_up(self):
        """Test get_key returns 'up' for Ctrl+P."""
        import readchar

        with patch.object(readchar, "readkey", return_value=readchar.key.CTRL_P):
            result = get_key()
            assert result == "up"

    def test_get_key_ctrl_n_is_down(self):
        """Test get_key returns 'down' for Ctrl+N."""
        import readchar

        with patch.object(readchar, "readkey", return_value=readchar.key.CTRL_N):
            result = get_key()
            assert result == "down"


class TestSelectWithArrows:
    """Tests for select_with_arrows function."""

    def test_select_with_enter(self):
        """Test selecting with enter key."""
        options = {"opt1": "Option 1", "opt2": "Option 2"}

        def mock_keys():
            keys = ["enter"]
            return keys.pop(0)

        with patch("refactor_cli.get_key", side_effect=["enter"]):
            result = select_with_arrows(options, "Select", "opt1")
            assert result == "opt1"

    def test_select_navigate_down_then_enter(self):
        """Test navigating down and selecting."""
        options = {"opt1": "Option 1", "opt2": "Option 2"}

        with patch("refactor_cli.get_key", side_effect=["down", "enter"]):
            result = select_with_arrows(options, "Select", "opt1")
            assert result == "opt2"

    def test_select_navigate_up_wraps(self):
        """Test navigating up wraps around."""
        options = {"opt1": "Option 1", "opt2": "Option 2"}

        with patch("refactor_cli.get_key", side_effect=["up", "enter"]):
            result = select_with_arrows(options, "Select", "opt1")
            # From index 0, going up wraps to last item
            assert result == "opt2"

    def test_select_escape_exits(self):
        """Test escape cancels selection."""
        import typer

        options = {"opt1": "Option 1", "opt2": "Option 2"}

        with (
            patch("refactor_cli.get_key", side_effect=["escape"]),
            pytest.raises(typer.Exit),
        ):
            select_with_arrows(options, "Select")

    def test_select_keyboard_interrupt_exits(self):
        """Test keyboard interrupt cancels selection."""
        import typer

        options = {"opt1": "Option 1", "opt2": "Option 2"}

        with (
            patch("refactor_cli.get_key", side_effect=KeyboardInterrupt),
            pytest.raises(typer.Exit),
        ):
            select_with_arrows(options, "Select")


class TestInitCommandPaths:
    """Tests for various init command code paths."""

    def test_init_invalid_ai_assistant(self):
        """Test init with invalid AI assistant name."""
        result = runner.invoke(app, ["init", "--ai", "invalid-agent", "test-project"])
        assert result.exit_code == 1
        assert "Invalid AI assistant" in result.output

    def test_init_no_git_flag(self, tmp_path):
        """Test init with --no-git flag."""
        with (
            patch("refactor_cli.Path.cwd", return_value=tmp_path),
            patch("refactor_cli.download_and_extract_template", side_effect=mock_download_and_extract),
        ):
            result = runner.invoke(app, ["init", "--ai", "claude", "--no-git", "test-project"])
            # Should complete without git init
            assert "git init" not in result.output.lower() or result.exit_code == 0
