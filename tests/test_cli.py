"""Tests for the CLI interface."""

from chuk_term import __version__
from chuk_term.cli import cli


def test_version(cli_runner):
    """Test version display."""
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_info_command(cli_runner):
    """Test info command."""
    result = cli_runner.invoke(cli, ["info"])
    assert result.exit_code == 0
    assert "ChukTerm" in result.output
    assert __version__ in result.output


def test_info_verbose(cli_runner):
    """Test info command with verbose flag."""
    result = cli_runner.invoke(cli, ["info", "--verbose"])
    assert result.exit_code == 0
    assert "ChukTerm" in result.output
    assert "Rich UI components" in result.output


def test_run_with_command(cli_runner):
    """Test run command with a command argument."""
    result = cli_runner.invoke(cli, ["run", "test-command"])
    assert result.exit_code == 0
    assert "Command executed" in result.output
    assert "test-command" in result.output


def test_run_interactive(cli_runner):
    """Test run command without arguments (interactive mode)."""
    result = cli_runner.invoke(cli, ["run"])
    assert result.exit_code == 0
    assert "Interactive mode" in result.output


def test_run_with_config(cli_runner, temp_config_file):
    """Test run command with config file."""
    result = cli_runner.invoke(cli, ["run", "--config", str(temp_config_file)])
    assert result.exit_code == 0
    assert "Using config:" in result.output


def test_test_command(cli_runner):
    """Test the test command."""
    result = cli_runner.invoke(cli, ["test"])
    assert result.exit_code == 0
    assert "Running terminal tests" in result.output
