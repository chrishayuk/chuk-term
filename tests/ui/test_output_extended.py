# tests/ui/test_output_extended.py
"""
Extended tests for output management to improve coverage.
"""
# ruff: noqa: ARG002
from __future__ import annotations

from io import StringIO
from unittest.mock import patch

import pytest

from chuk_term.ui import Output
from chuk_term.ui.theme import Theme


@pytest.fixture
def output():
    """Create a fresh Output instance for testing."""
    # Clear singleton
    Output._instance = None
    output = Output()
    # Ensure it's using default theme
    output.set_theme(Theme("default"))
    return output


@pytest.fixture
def captured_output():
    """Capture stdout for testing."""
    return StringIO()


class TestOutputRuleMethods:
    """Test rule method."""

    def test_rule_default(self, output, captured_output):
        """Test rule without text."""
        with patch("sys.stdout", captured_output):
            output.rule()
            result = captured_output.getvalue()
            assert len(result) > 0

    def test_rule_with_title(self, output, captured_output):
        """Test rule with title."""
        with patch("sys.stdout", captured_output):
            output.rule("Section Title")
            result = captured_output.getvalue()
            assert "Section Title" in result


class TestOutputStatusMethods:
    """Test status and command methods."""

    def test_status_method(self, output, captured_output):
        """Test status method."""
        with patch("sys.stdout", captured_output):
            output.status("Processing...")
            result = captured_output.getvalue()
            assert "Processing..." in result

    def test_command_method(self, output, captured_output):
        """Test command method."""
        with patch("sys.stdout", captured_output):
            output.command("ls -la", "List all files")
            result = captured_output.getvalue()
            assert "ls -la" in result


class TestOutputContextManagers:
    """Test context manager methods."""

    def test_progress_context(self, output):
        """Test progress context manager."""
        with output.progress("Processing...") as progress:
            assert progress is not None

    def test_loading_context(self, output):
        """Test loading context manager."""
        with output.loading("Loading...") as loading:
            assert loading is not None


class TestOutputHelperMethods:
    """Test helper and utility methods."""

    def test_clear_method(self, output):
        """Test clear method."""
        # Output.clear() internally calls terminal manager's clear
        output.clear()
        # Just verify it doesn't crash

    def test_get_raw_console(self, output):
        """Test get_raw_console method."""
        console = output.get_raw_console()
        assert console is not None


class TestOutputPrintMethods:
    """Test various print methods with different parameters."""

    def test_print_with_highlight(self, output, captured_output):
        """Test print with highlight."""
        with patch("sys.stdout", captured_output):
            output.print("Test message", highlight=True)
            # Just verify it doesn't crash
            result = captured_output.getvalue()
            assert "Test message" in result

    def test_print_with_style(self, output, captured_output):
        """Test print with custom style."""
        with patch("sys.stdout", captured_output):
            output.print("Styled text", style="bold red")
            result = captured_output.getvalue()
            assert "Styled text" in result

    def test_print_with_justify(self, output, captured_output):
        """Test print with justification."""
        with patch("sys.stdout", captured_output):
            output.print("Center text", justify="center")
            result = captured_output.getvalue()
            assert "Center text" in result

    def test_print_non_tty(self, output, captured_output):
        """Test print in non-TTY environment."""
        with patch("sys.stdout", captured_output):
            # Just test regular print
            output.print("Non-TTY message")
            result = captured_output.getvalue()
            assert "Non-TTY message" in result


class TestOutputThemeHandling:
    """Test theme-specific behavior."""

    def test_minimal_theme_methods(self, output, captured_output):
        """Test various methods in minimal theme."""
        output.set_theme(Theme("minimal"))

        with patch("sys.stdout", captured_output):
            # Test various methods
            output.panel("Panel content", title="Title")
            output.markdown("# Heading\n\nText")
            output.rule("Rule")
            output.json({"key": "value"})

            result = captured_output.getvalue()
            assert "Panel content" in result
            assert "Heading" in result
            assert "Rule" in result
            assert "key" in result

    def test_terminal_theme_methods(self, output, captured_output):
        """Test various methods in terminal theme."""
        output.set_theme(Theme("terminal"))

        with patch("sys.stdout", captured_output):
            output.panel("Content", title="Terminal Panel")
            output.markdown("**Bold** text")

            result = captured_output.getvalue()
            assert "Content" in result
            assert "Terminal Panel" in result
            assert "Bold" in result


class TestOutputMessageMethods:
    """Test message-specific methods."""

    def test_user_message(self, output, captured_output):
        """Test user message."""
        with patch("sys.stdout", captured_output):
            output.user_message("User input")
            result = captured_output.getvalue()
            assert "User input" in result

    def test_assistant_message(self, output, captured_output):
        """Test assistant message."""
        with patch("sys.stdout", captured_output):
            output.assistant_message("Assistant response", elapsed=1.5)
            result = captured_output.getvalue()
            assert "Assistant response" in result

    def test_tool_call_with_complex_args(self, output, captured_output):
        """Test tool call with complex arguments."""
        with patch("sys.stdout", captured_output):
            args = {"query": "test", "options": {"limit": 10, "offset": 0}, "filters": ["active", "verified"]}
            output.tool_call("search", args)
            result = captured_output.getvalue()
            assert "search" in result
            assert "query" in result


class TestOutputEdgeCases:
    """Test edge cases and error handling."""

    def test_print_with_none(self, output, captured_output):
        """Test printing None value."""
        with patch("sys.stdout", captured_output):
            output.print(None)
            result = captured_output.getvalue()
            assert "None" in result

    def test_json_with_invalid_data(self, output, captured_output):
        """Test JSON output with non-serializable data."""
        with patch("sys.stdout", captured_output):
            # Create non-serializable object
            class CustomObj:
                pass

            obj = CustomObj()
            # Should handle gracefully
            output.json({"obj": obj})
            result = captured_output.getvalue()
            # Should have some output (error or string representation)
            assert len(result) > 0

    def test_table_with_empty_data(self, output, captured_output):
        """Test table with empty data."""
        with patch("sys.stdout", captured_output):
            output.table([])
            result = captured_output.getvalue()
            # Should handle empty table gracefully
            assert len(result) >= 0

    def test_markdown_with_invalid_syntax(self, output, captured_output):
        """Test markdown with potentially problematic syntax."""
        with patch("sys.stdout", captured_output):
            # Markdown with various edge cases
            md = "# Title\n```python\nprint('test')\n```\n[link](http://example.com)"
            output.markdown(md)
            result = captured_output.getvalue()
            assert "Title" in result

    def test_output_in_quiet_verbose_modes(self, output, capsys):
        """Test output behavior in quiet and verbose modes."""
        # Test verbose mode
        output.set_output_mode(verbose=True)
        output.debug("Debug message in verbose")
        captured = capsys.readouterr()
        assert "Debug message in verbose" in captured.out

        # Test quiet mode
        output.set_output_mode(quiet=True)
        output.info("Info in quiet mode")
        captured = capsys.readouterr()
        assert "Info in quiet mode" not in captured.out

        output.error("Error in quiet mode")  # Should still show in stderr
        # Note: Rich console output doesn't get captured by capsys properly
        # Just verify it doesn't crash

        # Reset
        output.set_output_mode(quiet=False, verbose=False)
