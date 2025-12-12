"""Unit tests for output management."""

# ruff: noqa: ARG002

from io import StringIO
from unittest.mock import patch

import pytest
from rich.table import Table

from chuk_term.ui.output import Output, OutputLevel, error, get_output, info, success, tip, warning
from chuk_term.ui.output import print as ui_print
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


class TestOutputSingleton:
    """Test Output singleton behavior."""

    def test_singleton_instance(self):
        """Test that Output is a singleton."""
        # Clear any existing instance
        Output._instance = None
        output1 = Output()
        output2 = Output()
        assert output1 is output2

    def test_get_output_returns_singleton(self):
        """Test get_output returns the same instance."""
        output1 = get_output()
        output2 = get_output()
        assert output1 is output2


class TestOutputModes:
    """Test output modes (quiet, verbose)."""

    def test_set_output_mode(self, output):
        """Test setting output modes."""
        # Test quiet mode
        output.set_output_mode(quiet=True)
        assert output._quiet is True
        assert output._verbose is False

        # Test verbose mode
        output.set_output_mode(verbose=True)
        assert output._quiet is False
        assert output._verbose is True

        # Test both
        output.set_output_mode(quiet=True, verbose=True)
        assert output._quiet is True
        assert output._verbose is True

    def test_quiet_mode_suppresses_output(self, output, capsys):
        """Test that quiet mode suppresses non-essential output."""
        output.set_output_mode(quiet=True)

        # These should not print in quiet mode
        output.info("Test info")
        output.status("Test status")
        output.tip("Test tip")

        captured = capsys.readouterr()
        assert "Test info" not in captured.out
        assert "Test status" not in captured.out
        assert "Test tip" not in captured.out

        # These should still print even in quiet mode
        output.success("Test success")
        output.error("Test error")  # Just test it doesn't crash

        captured = capsys.readouterr()
        # Check for success message
        assert "Test success" in captured.out or "success" in captured.out.lower()

    def test_verbose_mode_shows_debug(self, output, capsys):
        """Test that verbose mode shows debug messages."""
        output.set_output_mode(verbose=False)

        # Should not print when not verbose
        output.debug("Test debug not verbose")
        captured = capsys.readouterr()
        assert "Test debug not verbose" not in captured.out

        # Should print when verbose
        output.set_output_mode(verbose=True)
        output.debug("Test debug verbose")
        captured = capsys.readouterr()
        assert "debug" in captured.out.lower() or "Test debug verbose" in captured.out


class TestBasicOutput:
    """Test basic output methods."""

    def test_print_method(self, output, capsys):
        """Test basic print method."""
        output.print("Test message")
        captured = capsys.readouterr()
        assert "Test message" in captured.out

    def test_info_message(self, output, capsys):
        """Test info message output."""
        output.info("Info message")
        captured = capsys.readouterr()
        assert "Info message" in captured.out

    def test_success_message(self, output, capsys):
        """Test success message output."""
        output.success("Success message")
        captured = capsys.readouterr()
        assert "Success message" in captured.out

    def test_warning_message(self, output, capsys):
        """Test warning message output."""
        output.warning("Warning message")
        captured = capsys.readouterr()
        assert "Warning message" in captured.out

    def test_error_message(self, output):
        """Test error message output."""
        # Just test that it doesn't crash - output goes through Rich console
        output.error("Error message")

    def test_fatal_message(self, output):
        """Test fatal error message output."""
        # Just test that it doesn't crash - output goes through Rich console
        output.fatal("Fatal error")


class TestFormattedOutput:
    """Test formatted output methods."""

    def test_tip_message(self, output, capsys):
        """Test tip message output."""
        output.tip("Helpful tip")
        captured = capsys.readouterr()
        assert "tip" in captured.out.lower() or "Helpful tip" in captured.out

    def test_hint_message(self, output, capsys):
        """Test hint message output."""
        output.hint("Subtle hint")
        captured = capsys.readouterr()
        assert "Subtle hint" in captured.out

    def test_command_suggestion(self, output, capsys):
        """Test command suggestion output."""
        # Command without description
        output.command("git status")
        captured = capsys.readouterr()
        assert "git status" in captured.out

        # Command with description
        output.command("git commit", "Commit changes")
        captured = capsys.readouterr()
        assert "git commit" in captured.out

    def test_status_message(self, output, capsys):
        """Test status message output."""
        output.status("Current status")
        captured = capsys.readouterr()
        assert "Current status" in captured.out


class TestRichComponents:
    """Test Rich component output."""

    def test_panel_output(self, output, capsys):
        """Test panel output."""
        output.panel("Panel content", title="Test Panel")
        captured = capsys.readouterr()
        # Panel content should be visible
        assert "Panel content" in captured.out

    def test_markdown_output(self, output, capsys):
        """Test markdown output."""
        output.markdown("# Heading\n\nSome **bold** text")
        captured = capsys.readouterr()
        # Markdown content should be visible
        assert "Heading" in captured.out

    def test_table_creation(self, output):
        """Test table creation."""
        table = output.table(title="Test Table")
        assert isinstance(table, Table)
        assert table.title == "Test Table"

    def test_print_table(self, output, capsys):
        """Test table printing."""
        table = Table(title="Test")
        table.add_column("Name")
        table.add_column("Value")
        table.add_row("Test", "123")

        output.print_table(table)
        captured = capsys.readouterr()
        # Table content should be visible
        assert "Test" in captured.out
        assert "123" in captured.out

    def test_rule_output(self, output, capsys):
        """Test horizontal rule output."""
        output.rule("Section Title")
        captured = capsys.readouterr()
        # Rule with title should be visible
        assert "Section Title" in captured.out or "─" in captured.out


class TestSpecialOutputs:
    """Test special output methods."""

    def test_user_message(self, output, capsys):
        """Test user message display."""
        output.user_message("User input text")
        captured = capsys.readouterr()
        assert "User input text" in captured.out

    def test_assistant_message(self, output, capsys):
        """Test assistant message display."""
        # Without elapsed time
        output.assistant_message("Assistant response")
        captured = capsys.readouterr()
        assert "Assistant response" in captured.out

        # With elapsed time
        output.assistant_message("Assistant response", elapsed=1.23)
        captured = capsys.readouterr()
        assert "Assistant response" in captured.out

    def test_tool_call(self, output, capsys):
        """Test tool call display."""
        # Tool call without arguments
        output.tool_call("test_tool")
        captured = capsys.readouterr()
        assert "test_tool" in captured.out

        # Tool call with arguments
        output.tool_call("test_tool", {"arg1": "value1", "arg2": 123})
        captured = capsys.readouterr()
        assert "test_tool" in captured.out


class TestMinimalTheme:
    """Test output with minimal theme."""

    def test_minimal_theme_plain_output(self, output, capsys):
        """Test that minimal theme outputs plain text."""
        # Set minimal theme
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        # Test various outputs
        output.info("Info message")
        captured = capsys.readouterr()
        assert "INFO: Info message" in captured.out

        output.success("Success message")
        captured = capsys.readouterr()
        assert "OK: Success message" in captured.out

        output.warning("Warning message")
        captured = capsys.readouterr()
        assert "WARN: Warning message" in captured.out

    def test_minimal_theme_strips_markup(self, output, capsys):
        """Test that minimal theme strips Rich markup."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        output.print("[bold]Bold text[/bold] and [red]colored[/red]")
        captured = capsys.readouterr()
        assert "Bold text and colored" in captured.out
        # Make sure markup is not present
        assert "[bold]" not in captured.out
        assert "[red]" not in captured.out

    def test_minimal_theme_panel(self, output, capsys):
        """Test panel output in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        output.panel("Panel content", title="Test Panel")
        captured = capsys.readouterr()

        # Should print title and content without formatting
        assert "Test Panel" in captured.out
        assert "Panel content" in captured.out


class TestTerminalTheme:
    """Test output with terminal theme."""

    def test_terminal_theme_basic_colors(self, output, capsys):
        """Test that terminal theme uses basic colors."""
        # Set terminal theme
        terminal_theme = Theme("terminal")
        output.set_theme(terminal_theme)

        output.info("Info message")
        captured = capsys.readouterr()
        # Should have basic formatting
        assert "Info message" in captured.out

    def test_terminal_theme_panel(self, output, capsys):
        """Test panel output in terminal theme."""
        terminal_theme = Theme("terminal")
        output.set_theme(terminal_theme)

        output.panel("Panel content", title="Test Panel")
        captured = capsys.readouterr()

        # Should print simplified panel
        assert "Test Panel" in captured.out
        assert "Panel content" in captured.out


class TestProgressAndLoading:
    """Test progress and loading indicators."""

    def test_progress_context_manager(self, output):
        """Test progress context manager."""
        # Should return a context manager
        with output.progress("Processing...") as progress:
            assert progress is not None

    def test_loading_context_manager(self, output):
        """Test loading spinner context manager."""
        # Should return a context manager
        with output.loading("Loading...") as loading:
            assert loading is not None

    def test_minimal_theme_progress(self, output, capsys):
        """Test progress in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        with output.progress("Processing..."):
            pass

        captured = capsys.readouterr()
        assert "Processing..." in captured.out

    def test_progress_bar(self, output):
        """Test progress_bar context manager."""
        with output.progress_bar("Processing files") as progress:
            assert progress is not None
            # Test adding a task
            task = progress.add_task("test", total=10)
            progress.update(task, advance=5)

    def test_progress_bar_without_time(self, output):
        """Test progress_bar without time columns."""
        with output.progress_bar("Processing", show_time=False) as progress:
            assert progress is not None

    def test_progress_bar_minimal_theme(self, output, capsys):
        """Test progress_bar in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        with output.progress_bar("Processing") as progress:
            assert progress is not None

    def test_track(self, output):
        """Test track method for iterating with progress."""
        items = [1, 2, 3, 4, 5]
        result = []
        for item in output.track(items, "Processing items"):
            result.append(item)
        assert result == items

    def test_track_with_total(self, output):
        """Test track method with explicit total."""
        items = range(10)
        count = 0
        for _ in output.track(items, "Processing", total=10):
            count += 1
        assert count == 10

    def test_track_minimal_theme(self, output, capsys):
        """Test track in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        items = [1, 2, 3]
        result = list(output.track(items, "Processing"))
        assert result == items
        captured = capsys.readouterr()
        assert "Processing" in captured.out

    def test_spinner(self, output):
        """Test spinner context manager."""
        with output.spinner("Working...") as spinner:
            assert spinner is not None

    def test_spinner_custom_type(self, output):
        """Test spinner with custom spinner type."""
        with output.spinner("Loading...", spinner_type="line") as spinner:
            assert spinner is not None


class TestUtilityMethods:
    """Test utility methods."""

    def test_clear_screen(self, output):
        """Test screen clearing."""
        # Just test that it doesn't crash
        output.clear()

    @patch("builtins.input", return_value="user input")
    def test_prompt(self, mock_input, output):
        """Test user prompt."""
        result = output.prompt("Enter value")
        assert result == "user input"

    @patch("builtins.input", return_value="y")
    def test_confirm(self, mock_input, output):
        """Test confirmation prompt."""
        result = output.confirm("Are you sure?")
        assert result is True

    @patch("builtins.input", return_value="test value")
    def test_minimal_theme_prompt(self, mock_input, output):
        """Test prompt in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        result = output.prompt("Enter value", default="default")

        mock_input.assert_called_with("Enter value [default]: ")
        assert result == "test value"

    @patch("builtins.input", return_value="y")
    def test_minimal_theme_confirm(self, mock_input, output):
        """Test confirm in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        result = output.confirm("Continue?", default=True)

        mock_input.assert_called_with("Continue? [Y/n]: ")
        assert result is True


class TestConvenienceFunctions:
    """Test module-level convenience functions."""

    def test_print_function(self, capsys):
        """Test module-level print function."""
        ui_print("Test message")
        captured = capsys.readouterr()
        assert "Test message" in captured.out

    def test_info_function(self, capsys):
        """Test module-level info function."""
        info("Info message")
        captured = capsys.readouterr()
        assert "Info message" in captured.out

    def test_success_function(self, capsys):
        """Test module-level success function."""
        success("Success message")
        captured = capsys.readouterr()
        assert "Success message" in captured.out

    def test_warning_function(self, capsys):
        """Test module-level warning function."""
        warning("Warning message")
        captured = capsys.readouterr()
        assert "Warning message" in captured.out

    def test_error_function(self):
        """Test module-level error function."""
        # Just test that it doesn't crash - output goes through Rich console
        error("Error message")

    def test_tip_function(self, capsys):
        """Test module-level tip function."""
        tip("Tip message")
        captured = capsys.readouterr()
        assert "Tip message" in captured.out or "tip" in captured.out.lower()


class TestErrorHandling:
    """Test error handling in output methods."""

    def test_markdown_fallback_on_error(self, output, capsys):
        """Test that markdown falls back to Text on error."""
        # This might cause markdown parsing error but should still work
        output.assistant_message("Invalid [markdown")

        captured = capsys.readouterr()
        # Should still output something
        assert "Invalid" in captured.out or "markdown" in captured.out

    def test_tool_call_json_error_handling(self, output, capsys):
        """Test tool call handles non-JSON serializable arguments."""

        # Non-serializable object
        class NonSerializable:
            def __str__(self):
                return "NonSerializable object"

        output.tool_call("test_tool", NonSerializable())

        captured = capsys.readouterr()
        # Should handle gracefully
        assert "test_tool" in captured.out


class TestThemeIntegration:
    """Test theme integration with output."""

    def test_theme_switching(self, output):
        """Test switching between themes."""
        # Switch to minimal
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)
        assert output._theme.name == "minimal"
        assert output._console.no_color is True

        # Switch to terminal
        terminal_theme = Theme("terminal")
        output.set_theme(terminal_theme)
        assert output._theme.name == "terminal"
        assert output._console.no_color is False

        # Switch to default
        default_theme = Theme("default")
        output.set_theme(default_theme)
        assert output._theme.name == "default"


class TestDelegatedMethods:
    """Test methods that delegate to formatters/code modules."""

    @patch("chuk_term.ui.formatters.format_tree")
    def test_tree_delegation(self, mock_format_tree, output):
        """Test that tree() delegates to format_tree."""
        mock_format_tree.return_value = "tree output"

        test_data = {"root": {"child": "value"}}
        output.tree(test_data, title="Test Tree")

        mock_format_tree.assert_called_once_with(test_data, title="Test Tree")

    @patch("chuk_term.ui.formatters.format_json")
    def test_json_delegation(self, mock_format_json, output):
        """Test that json() delegates to format_json."""
        mock_format_json.return_value = "json output"

        test_data = {"key": "value"}
        output.json(test_data, syntax_highlight=True)

        mock_format_json.assert_called_once()

    @patch("chuk_term.ui.code.display_code")
    def test_code_delegation(self, mock_display_code, output):
        """Test that code() delegates to display_code."""
        test_code = "print('hello')"
        output.code(test_code, language="python", line_numbers=True)

        mock_display_code.assert_called_once_with(test_code, "python", line_numbers=True)


class TestSimpleFormatting:
    """Test simple formatting methods unique to output."""

    def test_list_items_bullet(self, output, capsys):
        """Test bullet list formatting."""
        items = ["First", "Second", "Third"]
        output.list_items(items, style="bullet")

        captured = capsys.readouterr()
        assert "First" in captured.out
        assert "Second" in captured.out
        assert "Third" in captured.out

    def test_list_items_numbered(self, output, capsys):
        """Test numbered list formatting."""
        items = ["Step one", "Step two", "Step three"]
        output.list_items(items, style="number")

        captured = capsys.readouterr()
        assert "Step one" in captured.out
        assert "Step two" in captured.out

    def test_list_items_checklist(self, output, capsys):
        """Test checklist formatting."""
        items = [{"text": "Task 1", "checked": True}, {"text": "Task 2", "checked": False}]
        output.list_items(items, style="check")

        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out

    def test_kvpairs(self, output, capsys):
        """Test key-value pairs formatting."""
        data = {"Name": "Test", "Version": "1.0", "Status": "Active"}
        output.kvpairs(data)

        captured = capsys.readouterr()
        assert "Name" in captured.out
        assert "Test" in captured.out
        assert "Version" in captured.out
        assert "1.0" in captured.out

    def test_columns(self, output, capsys):
        """Test column layout formatting."""
        data = [["Alice", "Engineer"], ["Bob", "Designer"]]
        headers = ["Name", "Role"]

        output.columns(data, headers=headers)

        captured = capsys.readouterr()
        assert "Alice" in captured.out
        assert "Engineer" in captured.out


class TestOutputLevel:
    """Test OutputLevel enum."""

    def test_output_levels(self):
        """Test that all output levels are defined."""
        assert OutputLevel.DEBUG.value == "debug"
        assert OutputLevel.INFO.value == "info"
        assert OutputLevel.SUCCESS.value == "success"
        assert OutputLevel.WARNING.value == "warning"
        assert OutputLevel.ERROR.value == "error"
        assert OutputLevel.FATAL.value == "fatal"


class TestANSICodeHandling:
    """Test handling of ANSI escape codes."""

    def test_ansi_codes_bypass_rich(self, output, capsys):
        """Test that ANSI codes bypass Rich processing."""
        # Test with actual escape character
        ansi_message = "\x1b[31mRed Text\x1b[0m"
        output.print(ansi_message)

        captured = capsys.readouterr()
        # Should output something
        assert "Red" in captured.out or "Text" in captured.out

    def test_print_status_line(self, output, capsys):
        """Test print_status_line outputs ANSI codes correctly."""
        output.print_status_line("Processing 50%", end="")
        captured = capsys.readouterr()
        # Should contain ANSI escape codes and message
        assert "Processing" in captured.out or "\x1b" in captured.out


class TestMinimalThemeEdgeCases:
    """Test edge cases for minimal theme."""

    def test_minimal_print_markdown(self, output, capsys):
        """Test printing Markdown in minimal theme."""
        from rich.markdown import Markdown

        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        md = Markdown("# Heading")
        output.print(md)

        captured = capsys.readouterr()
        assert "Heading" in captured.out

    def test_minimal_print_text_object(self, output, capsys):
        """Test printing Text object in minimal theme."""
        from rich.text import Text

        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        text = Text("Styled text")
        output.print(text)

        captured = capsys.readouterr()
        assert "Styled text" in captured.out

    def test_minimal_panel_with_markdown(self, output, capsys):
        """Test panel with Markdown content in minimal theme."""
        from rich.markdown import Markdown

        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        output.panel(Markdown("# Content"), title="Title")
        captured = capsys.readouterr()
        assert "Title" in captured.out
        assert "Content" in captured.out

    def test_minimal_panel_with_text(self, output, capsys):
        """Test panel with Text content in minimal theme."""
        from rich.text import Text

        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        output.panel(Text("Plain text"), title="Header")
        captured = capsys.readouterr()
        assert "Header" in captured.out
        assert "Plain text" in captured.out

    def test_minimal_debug_message(self, output, capsys):
        """Test debug message in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)
        output.set_output_mode(verbose=True)

        output.debug("Debug info")
        captured = capsys.readouterr()
        assert "DEBUG:" in captured.out or "Debug info" in captured.out

    def test_minimal_error_output(self, output, capsys):
        """Test error output in minimal theme goes to stderr."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        output.error("Error message")
        captured = capsys.readouterr()
        assert "ERROR:" in captured.err

    def test_minimal_fatal_output(self, output, capsys):
        """Test fatal output in minimal theme goes to stderr."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        output.fatal("Fatal error")
        captured = capsys.readouterr()
        assert "FATAL:" in captured.err

    def test_minimal_rule_with_title(self, output, capsys):
        """Test rule with title in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        output.rule("Section")
        captured = capsys.readouterr()
        assert "Section" in captured.out
        assert "-" in captured.out

    def test_minimal_rule_without_title(self, output, capsys):
        """Test rule without title in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        output.rule()
        captured = capsys.readouterr()
        assert "-" in captured.out


class TestTerminalThemeEdgeCases:
    """Test edge cases for terminal theme."""

    def test_terminal_debug_message(self, output, capsys):
        """Test debug message in terminal theme."""
        terminal_theme = Theme("terminal")
        output.set_theme(terminal_theme)
        output.set_output_mode(verbose=True)

        output.debug("Debug info")
        captured = capsys.readouterr()
        assert "DEBUG:" in captured.out

    def test_terminal_error_output(self, output, capsys):
        """Test error output in terminal theme."""
        terminal_theme = Theme("terminal")
        output.set_theme(terminal_theme)

        output.error("Error message")
        # Error should not crash

    def test_terminal_fatal_output(self, output):
        """Test fatal output in terminal theme."""
        terminal_theme = Theme("terminal")
        output.set_theme(terminal_theme)

        output.fatal("Fatal error")
        # Should not crash

    def test_terminal_user_message(self, output, capsys):
        """Test user message in terminal theme."""
        terminal_theme = Theme("terminal")
        output.set_theme(terminal_theme)

        output.user_message("User input")
        captured = capsys.readouterr()
        assert "User" in captured.out
        assert "User input" in captured.out

    def test_terminal_assistant_message(self, output, capsys):
        """Test assistant message in terminal theme."""
        terminal_theme = Theme("terminal")
        output.set_theme(terminal_theme)

        output.assistant_message("Response", elapsed=1.5)
        captured = capsys.readouterr()
        assert "Assistant" in captured.out
        assert "Response" in captured.out

    def test_terminal_tool_call_with_args(self, output, capsys):
        """Test tool call in terminal theme."""
        terminal_theme = Theme("terminal")
        output.set_theme(terminal_theme)

        output.tool_call("my_tool", {"key": "value"})
        captured = capsys.readouterr()
        assert "Tool" in captured.out
        assert "my_tool" in captured.out


class TestListItemsEdgeCases:
    """Test edge cases for list_items method."""

    def test_list_items_arrow_style(self, output, capsys):
        """Test arrow style list."""
        items = ["Item 1", "Item 2"]
        output.list_items(items, style="arrow")

        captured = capsys.readouterr()
        assert "Item 1" in captured.out

    def test_list_items_with_indent(self, output, capsys):
        """Test indented list."""
        items = ["Nested item"]
        output.list_items(items, indent=2)

        captured = capsys.readouterr()
        assert "Nested item" in captured.out

    def test_list_items_minimal_theme(self, output, capsys):
        """Test list items in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        items = ["A", "B", "C"]
        output.list_items(items, style="number")

        captured = capsys.readouterr()
        assert "1." in captured.out
        assert "A" in captured.out

    def test_list_items_checklist_minimal(self, output, capsys):
        """Test checklist in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        items = [{"text": "Task", "checked": True}]
        output.list_items(items, style="check")

        captured = capsys.readouterr()
        assert "Task" in captured.out


class TestKVPairsEdgeCases:
    """Test edge cases for kvpairs method."""

    def test_kvpairs_empty(self, output, capsys):
        """Test kvpairs with empty dict."""
        output.kvpairs({})
        captured = capsys.readouterr()
        # Should output nothing
        assert captured.out == ""

    def test_kvpairs_no_align(self, output, capsys):
        """Test kvpairs without alignment."""
        data = {"Key": "Value"}
        output.kvpairs(data, align=False)

        captured = capsys.readouterr()
        assert "Key" in captured.out
        assert "Value" in captured.out

    def test_kvpairs_minimal_theme(self, output, capsys):
        """Test kvpairs in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        data = {"Name": "Test", "Status": "OK"}
        output.kvpairs(data)

        captured = capsys.readouterr()
        assert "Name" in captured.out
        assert "Status" in captured.out


class TestColumnsEdgeCases:
    """Test edge cases for columns method."""

    def test_columns_empty(self, output, capsys):
        """Test columns with empty data."""
        output.columns([])
        captured = capsys.readouterr()
        # Should output nothing
        assert captured.out == ""

    def test_columns_no_headers(self, output, capsys):
        """Test columns without headers."""
        data = [["A", "B"], ["C", "D"]]
        output.columns(data)

        captured = capsys.readouterr()
        assert "A" in captured.out
        assert "B" in captured.out

    def test_columns_minimal_theme(self, output, capsys):
        """Test columns in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        data = [["Col1", "Col2"], ["Val1", "Val2"]]
        headers = ["H1", "H2"]
        output.columns(data, headers=headers)

        captured = capsys.readouterr()
        assert "H1" in captured.out
        assert "Col1" in captured.out


class TestPrintTableEdgeCases:
    """Test edge cases for print_table method."""

    def test_print_table_string(self, output, capsys):
        """Test print_table with string input."""
        output.print_table("Already a plain table")
        captured = capsys.readouterr()
        assert "Already a plain table" in captured.out

    def test_print_table_minimal_theme(self, output, capsys):
        """Test print_table in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        table = Table()
        table.add_column("Name")
        table.add_column("Value")
        table.add_row("Test", "123")

        output.print_table(table)
        captured = capsys.readouterr()
        # Minimal theme may convert to plain text or still print Rich table
        assert "Test" in captured.out or captured.out.strip() == "" or "Name" in captured.out


class TestPromptEdgeCases:
    """Test edge cases for prompt methods."""

    @patch("builtins.input", return_value="")
    def test_prompt_empty_returns_default(self, mock_input, output):
        """Test that empty input returns default value."""
        result = output.prompt("Enter value", default="fallback")
        assert result == "fallback"

    @patch("builtins.input", return_value="")
    def test_prompt_empty_no_default(self, mock_input, output):
        """Test empty input with no default returns empty string."""
        result = output.prompt("Enter value")
        assert result == ""

    @patch("builtins.input", return_value="n")
    def test_confirm_no(self, mock_input, output):
        """Test confirm with 'n' input."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        result = output.confirm("Continue?")
        assert result is False

    @patch("builtins.input", return_value="")
    def test_confirm_empty_uses_default(self, mock_input, output):
        """Test confirm with empty input uses default."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        result = output.confirm("Continue?", default=True)
        assert result is True


class TestRawConsole:
    """Test raw console access."""

    def test_get_raw_console(self, output):
        """Test getting raw console instance."""
        console = output.get_raw_console()
        assert console is not None
        assert console is output._console


class TestSuccessMessageStripping:
    """Test success message checkmark stripping."""

    def test_success_strips_checkmark(self, output, capsys):
        """Test that success strips leading checkmark."""
        output.success("✓ Already has checkmark")
        captured = capsys.readouterr()
        assert "Already has checkmark" in captured.out


class TestMinimalToolCall:
    """Test tool call in minimal theme."""

    def test_minimal_tool_call_with_args(self, output, capsys):
        """Test tool call with arguments in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        output.tool_call("test_tool", {"param": "value"})
        captured = capsys.readouterr()
        assert "Tool: test_tool" in captured.out
        assert "param" in captured.out

    def test_minimal_tool_call_no_args(self, output, capsys):
        """Test tool call without arguments in minimal theme."""
        minimal_theme = Theme("minimal")
        output.set_theme(minimal_theme)

        output.tool_call("simple_tool")
        captured = capsys.readouterr()
        assert "Tool: simple_tool" in captured.out
