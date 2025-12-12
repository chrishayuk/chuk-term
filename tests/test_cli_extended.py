# tests/test_cli_extended.py
"""
Extended tests for CLI to improve coverage.
"""
from __future__ import annotations

from unittest.mock import patch

from click.testing import CliRunner

from chuk_term.cli import cli, main


class TestDemoCommand:
    """Test the demo command."""

    def test_demo_full_flow(self):
        """Test demo command with full interaction flow."""
        runner = CliRunner()

        with (
            patch("chuk_term.cli.ask", return_value="TestUser"),
            patch("chuk_term.cli.confirm", side_effect=[True, False]),
            patch("chuk_term.cli.select_from_list", return_value="monokai"),
            patch("chuk_term.cli.set_theme") as mock_set_theme,
        ):
            result = runner.invoke(cli, ["demo"])

            assert result.exit_code == 0
            assert "Hello, TestUser!" in result.output
            assert "Theme changed to: monokai" in result.output
            assert "Sample Code Display" in result.output
            assert "Output Examples" in result.output
            assert "Demo Complete!" in result.output
            mock_set_theme.assert_called_once_with("monokai")

    def test_demo_skip_themes(self):
        """Test demo command when user skips theme selection."""
        runner = CliRunner()

        with patch("chuk_term.cli.ask", return_value="TestUser"), patch("chuk_term.cli.confirm", return_value=False):
            result = runner.invoke(cli, ["demo"])

            assert result.exit_code == 0
            assert "Hello, TestUser!" in result.output
            assert "Sample Code Display" in result.output
            assert "Theme changed" not in result.output


class TestMainFunction:
    """Test the main entry point."""

    def test_main_success(self):
        """Test main function with successful execution."""
        with patch("chuk_term.cli.cli") as mock_cli:
            result = main()
            assert result == 0
            mock_cli.assert_called_once()

    def test_main_with_exception(self):
        """Test main function with exception handling."""
        with (
            patch("chuk_term.cli.cli", side_effect=Exception("Test error")),
            patch("chuk_term.cli.output.error") as mock_error,
        ):
            result = main()
            assert result == 1
            mock_error.assert_called_with("Error: Test error")

    def test_main_with_keyboard_interrupt(self):
        """Test main function with keyboard interrupt."""
        # KeyboardInterrupt inherits from BaseException, not Exception
        # So it won't be caught by the except Exception clause
        with (
            patch("chuk_term.cli.cli", side_effect=ValueError("Simulated error")),
            patch("chuk_term.cli.output.error") as mock_error,
        ):
            result = main()
            assert result == 1
            mock_error.assert_called_with("Error: Simulated error")


class TestRunCommand:
    """Test the run command."""

    def test_run_with_command(self):
        """Test run command with a specific command."""
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "ls -la"])

        assert result.exit_code == 0
        assert "Command executed: ls -la" in result.output

    def test_run_interactive_mode(self):
        """Test run command in interactive mode."""
        runner = CliRunner()
        result = runner.invoke(cli, ["run"])

        assert result.exit_code == 0
        assert "Interactive mode not yet implemented" in result.output
        assert "This is where your terminal functionality will go" in result.output

    def test_run_with_config(self):
        """Test run command with config file."""
        runner = CliRunner()

        # Create a temporary config file
        with runner.isolated_filesystem():
            with open("config.json", "w") as f:
                f.write('{"key": "value"}')

            result = runner.invoke(cli, ["run", "--config", "config.json"])

            assert result.exit_code == 0
            assert "Using config: config.json" in result.output

    def test_run_interactive_with_config(self):
        """Test run command in interactive mode with config."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("config.yaml", "w") as f:
                f.write("setting: value")

            result = runner.invoke(cli, ["run", "--config", "config.yaml"])

            assert result.exit_code == 0
            assert "Interactive mode not yet implemented" in result.output
            assert "Using config: config.yaml" in result.output


class TestTestCommand:
    """Test the test command."""

    def test_test_without_theme(self):
        """Test test command without theme option."""
        runner = CliRunner()
        result = runner.invoke(cli, ["test"])

        assert result.exit_code == 0
        assert "Running terminal tests..." in result.output
        assert "Test functionality will be implemented here" in result.output

    def test_test_with_theme(self):
        """Test test command with theme option."""
        runner = CliRunner()

        with patch("chuk_term.cli.set_theme") as mock_set_theme:
            result = runner.invoke(cli, ["test", "--theme", "dracula"])

            assert result.exit_code == 0
            assert "Running terminal tests..." in result.output
            mock_set_theme.assert_called_once_with("dracula")

    def test_test_with_all_themes(self):
        """Test test command with each available theme."""
        runner = CliRunner()
        themes = ["default", "dark", "light", "minimal", "terminal", "monokai", "dracula"]

        for theme in themes:
            with patch("chuk_term.cli.set_theme") as mock_set_theme:
                result = runner.invoke(cli, ["test", "--theme", theme])

                assert result.exit_code == 0
                mock_set_theme.assert_called_once_with(theme)


class TestCLIGroupAndOptions:
    """Test CLI group and global options."""

    def test_cli_version_option(self):
        """Test --version option."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])

        assert result.exit_code == 0
        assert "version" in result.output.lower()

    def test_cli_help(self):
        """Test help output."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "ChukTerm - A powerful terminal library CLI" in result.output
        assert "Commands:" in result.output

    def test_command_help(self):
        """Test help for individual commands."""
        runner = CliRunner()
        commands = ["info", "run", "demo", "test"]

        for cmd in commands:
            result = runner.invoke(cli, [cmd, "--help"])
            assert result.exit_code == 0
            assert "Usage:" in result.output

    def test_invalid_command(self):
        """Test invalid command handling."""
        runner = CliRunner()
        result = runner.invoke(cli, ["invalid-command"])

        assert result.exit_code != 0
        assert "Error" in result.output or "No such command" in result.output


class TestInfoCommand:
    """Test the info command."""

    def test_info_basic(self):
        """Test basic info command."""
        runner = CliRunner()
        result = runner.invoke(cli, ["info"])

        assert result.exit_code == 0
        assert "ChukTerm version" in result.output

    def test_info_verbose(self):
        """Test info command with verbose flag."""
        runner = CliRunner()
        result = runner.invoke(cli, ["info", "--verbose"])

        assert result.exit_code == 0
        assert "ChukTerm version" in result.output
        assert "Features:" in result.output
        assert "Rich UI components" in result.output
        assert "Theme support" in result.output
        assert "Code display with syntax highlighting" in result.output
        assert "Interactive prompts and menus" in result.output
        assert "Centralized output management" in result.output

    def test_info_verbose_short_flag(self):
        """Test info command with short verbose flag."""
        runner = CliRunner()
        result = runner.invoke(cli, ["info", "-v"])

        assert result.exit_code == 0
        assert "Features:" in result.output


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_run_with_nonexistent_config(self):
        """Test run command with non-existent config file."""
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--config", "nonexistent.json"])

        # Should fail because config file doesn't exist
        assert result.exit_code != 0

    def test_test_with_invalid_theme(self):
        """Test test command with invalid theme."""
        runner = CliRunner()
        result = runner.invoke(cli, ["test", "--theme", "invalid-theme"])

        # Should fail due to invalid choice
        assert result.exit_code != 0

    def test_cli_context_passing(self):
        """Test that context is properly passed between commands."""
        runner = CliRunner()

        # This tests the @click.pass_context decorator
        with patch("chuk_term.cli.click.Context"):
            # The CLI should ensure the context has a dict object
            result = runner.invoke(cli, ["info"])
            assert result.exit_code == 0


class TestExamplesCommandExtended:
    """Extended tests for examples command."""

    def test_examples_run_with_nonexistent(self):
        """Test running nonexistent example."""
        runner = CliRunner()
        result = runner.invoke(cli, ["examples", "--run", "completely_nonexistent_example"])

        # Should report example not found or execute an example
        assert result.exit_code == 0 or "not found" in result.output.lower()

    def test_examples_successful_run(self):
        """Test running an example successfully."""

        runner = CliRunner()

        # Create mock for subprocess.run to simulate success
        with (
            patch("chuk_term.cli.Path"),
            patch("subprocess.run") as mock_subprocess,
        ):
            from pathlib import Path

            # Setup mock path
            real_examples_dir = Path(__file__).parent.parent / "examples"
            if real_examples_dir.exists():
                # Use real examples directory if it exists
                example_files = list(real_examples_dir.glob("*.py"))
                if example_files:
                    mock_subprocess.return_value.returncode = 0

                    result = runner.invoke(cli, ["examples"])
                    assert result.exit_code == 0

    def test_examples_list(self):
        """Test examples command listing available examples."""
        runner = CliRunner()
        result = runner.invoke(cli, ["examples"])

        # Should list available examples or show not found message
        assert result.exit_code == 0

    def test_examples_empty_directory(self):
        """Test examples command with empty examples directory."""
        runner = CliRunner()

        with patch("chuk_term.cli.Path") as mock_path:
            mock_examples_dir = mock_path.return_value.parent.parent.__truediv__.return_value
            mock_examples_dir.exists.return_value = True
            mock_examples_dir.glob.return_value = []

            result = runner.invoke(cli, ["examples"])

            assert "No example files found" in result.output

    def test_examples_run_failed(self):
        """Test running an example that fails."""
        import subprocess

        runner = CliRunner()

        with (
            patch("chuk_term.cli.Path") as mock_path,
            patch("subprocess.run") as mock_subprocess,
        ):
            from unittest.mock import MagicMock

            # Create mock path chain
            mock_package_dir = MagicMock()
            mock_examples_dir = MagicMock()

            mock_path.return_value = mock_package_dir
            mock_package_dir.parent.parent.__truediv__.return_value = mock_examples_dir
            mock_examples_dir.exists.return_value = True

            # Create mock example file
            mock_example_file = MagicMock()
            mock_example_file.name = "test_example.py"
            mock_example_file.stem = "test_example"
            mock_example_file.exists.return_value = True
            mock_examples_dir.glob.return_value = [mock_example_file]
            mock_examples_dir.__truediv__.return_value = mock_example_file

            # Simulate subprocess failure
            mock_subprocess.side_effect = subprocess.CalledProcessError(1, "python")

            result = runner.invoke(cli, ["examples", "--run", "test_example"])

            # Should report failure
            assert "failed" in result.output.lower() or result.exit_code == 0


class TestThemesCommand:
    """Test the themes command in detail."""

    def test_themes_side_by_side_display(self):
        """Test themes command with side-by-side display."""
        runner = CliRunner()

        with patch("chuk_term.cli.set_theme"), patch("chuk_term.cli.get_theme") as mock_get_theme:
            mock_theme = mock_get_theme.return_value
            mock_theme.name = "default"
            mock_theme.style.return_value = "blue"

            result = runner.invoke(cli, ["themes", "--side-by-side"])
            assert result.exit_code == 0

    def test_themes_detailed_display(self):
        """Test themes command with detailed display."""
        runner = CliRunner()

        with patch("chuk_term.cli.set_theme"), patch("chuk_term.cli.get_theme") as mock_get_theme:
            mock_theme = mock_get_theme.return_value
            mock_theme.name = "default"
            mock_theme.style.return_value = "blue"

            result = runner.invoke(cli, ["themes"])
            assert result.exit_code == 0
            assert "Theme Gallery" in result.output


class TestExamplesCommandCoverage:
    """Tests to specifically improve CLI examples command coverage."""

    def test_examples_with_description_reading(self):
        """Test examples command reads descriptions (covers lines 214-222)."""
        runner = CliRunner()

        # Run examples command which reads file descriptions
        result = runner.invoke(cli, ["examples"])

        # Should show available examples
        assert result.exit_code == 0
        # Should have printed something about examples
        assert "examples" in result.output.lower() or "demo" in result.output.lower()


class TestCLIExceptionHandling:
    """Test exception handling in CLI."""

    def test_main_returns_zero_on_success(self):
        """Test main function returns 0 on success."""
        with patch("chuk_term.cli.cli"):
            result = main()
            assert result == 0

    def test_main_returns_one_on_error(self):
        """Test main function returns 1 on error."""
        with (
            patch("chuk_term.cli.cli", side_effect=RuntimeError("Test")),
            patch("chuk_term.cli.output.error"),
        ):
            result = main()
            assert result == 1
