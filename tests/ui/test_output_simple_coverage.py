"""Simple targeted tests to improve output.py coverage."""

import sys
from unittest.mock import MagicMock, patch

from chuk_term.ui.output import get_output
from chuk_term.ui.theme import set_theme


def test_minimal_theme_paths():
    """Test minimal theme code paths."""
    set_theme("minimal")
    output = get_output()

    # Test _plain_print is called for various message types
    with patch("builtins.print") as mock_print:
        output.info("test")
        output.success("test")
        output.warning("test")
        output.tip("test")
        output.hint("test")
        output.command("cmd")
        output.status("status")
        output.user_message("user")
        output.assistant_message("assistant")
        output.tool_call("tool", {"arg": "val"})

        # All should have called print
        assert mock_print.call_count > 10


def test_terminal_theme_paths():
    """Test terminal theme code paths."""
    set_theme("terminal")
    output = get_output()

    with patch.object(output._console, "print") as mock_print:
        output.info("test")
        output.success("test")
        output.warning("test")
        output.user_message("user")
        output.assistant_message("assistant")
        output.tool_call("tool", {})

        # All should have called console.print
        assert mock_print.call_count >= 6

    # Test panel in terminal
    with patch("builtins.print") as mock_print:
        output.panel("content", title="title")
        assert mock_print.call_count > 0


def test_verbose_and_quiet_modes():
    """Test verbose and quiet output modes."""
    output = get_output()

    # Test verbose mode
    output.set_output_mode(verbose=True)
    set_theme("minimal")
    with patch("builtins.print") as mock_print:
        output.debug("debug msg")
        mock_print.assert_called()

    set_theme("terminal")
    with patch.object(output._console, "print") as mock_print:
        output.debug("debug msg")
        mock_print.assert_called()

    set_theme("default")
    with patch.object(output._console, "print") as mock_print:
        output.debug("debug msg")
        mock_print.assert_called()

    # Test quiet mode
    output.set_output_mode(quiet=True)
    with patch.object(output._console, "print") as mock_print:
        output.info("info")
        output.tip("tip")
        output.hint("hint")
        output.status("status")
        # Should not print in quiet mode
        mock_print.assert_not_called()

    # Reset
    output.set_output_mode(verbose=False, quiet=False)
    set_theme("default")


def test_print_with_different_object_types():
    """Test print with various object types."""
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text

    set_theme("minimal")
    output = get_output()

    with patch("builtins.print") as mock_print:
        # String
        output.print("text")

        # Markdown
        md = Markdown("# Header")
        output.print(md)

        # Panel
        panel = Panel("content")
        output.print(panel)

        # Panel with Markdown
        panel_md = Panel(Markdown("# Header"))
        output.print(panel_md)

        # Panel with Text
        panel_text = Panel(Text("text"))
        output.print(panel_text)

        # Table
        table = Table()
        output.print(table)

        # Text
        text = Text("plain")
        output.print(text)

        # Generic object
        output.print(123)

        assert mock_print.call_count >= 8


def test_panel_various_content_types():
    """Test panel with different content types."""
    from rich.markdown import Markdown
    from rich.text import Text

    set_theme("minimal")
    output = get_output()

    with patch("builtins.print") as mock_print:
        # String content
        output.panel("string", title="Title")

        # Markdown content
        output.panel(Markdown("# Header"))

        # Text content
        output.panel(Text("text"))

        # Generic object
        output.panel(123)

        assert mock_print.call_count > 0

    # Test terminal theme
    set_theme("terminal")
    with patch("builtins.print") as mock_print:
        output.panel("content", title="Title")
        output.panel(Markdown("# Header"))
        output.panel(Text("text"))
        assert mock_print.call_count > 0


def test_list_items_styles():
    """Test different list styles."""
    set_theme("minimal")
    output = get_output()

    items = ["Item 1", "Item 2", "Item 3"]

    with patch("builtins.print") as mock_print:
        # Number style
        output.list_items(items, style="number")
        # Should print 3 items
        assert mock_print.call_count == 3

        mock_print.reset_mock()
        # Checklist style
        output.list_items(items, style="checklist", checked=[0, 2])
        assert mock_print.call_count == 3

        mock_print.reset_mock()
        # Bullet style (default)
        output.list_items(items)
        assert mock_print.call_count == 3


def test_kvpairs_and_columns():
    """Test kvpairs and columns."""
    set_theme("minimal")
    output = get_output()

    with patch("builtins.print") as mock_print:
        # kvpairs
        output.kvpairs({"key1": "val1", "key2": "val2"})
        output.kvpairs({"key": "value"}, align=True)

        # columns
        output.columns(["A", "B", "C", "D"], width=2)
        output.columns([["R1C1", "R1C2"], ["R2C1", "R2C2"]], headers=["H1", "H2"])

        assert mock_print.call_count > 0


def test_rule_variations():
    """Test rule with different options."""
    set_theme("minimal")
    output = get_output()

    with patch("builtins.print") as mock_print:
        output.rule()
        output.rule("Title")
        assert mock_print.call_count == 2


def test_progress_and_loading_contexts():
    """Test progress and loading in different themes."""
    # Minimal theme
    set_theme("minimal")
    output = get_output()

    with patch("builtins.print") as mock_print:
        with output.progress("Processing..."):
            pass
        with output.loading("Loading..."):
            pass
        assert mock_print.call_count == 2

    # Rich theme
    set_theme("default")
    with patch("rich.progress.Progress"), output.progress("Processing..."):
        pass

    with patch.object(output._console, "status") as mock_status:
        mock_status.return_value = MagicMock()
        with output.loading("Loading..."):
            pass
        mock_status.assert_called()


def test_tool_call_json_handling():
    """Test tool call with JSON serialization."""
    set_theme("minimal")
    output = get_output()

    # Valid JSON
    with patch("builtins.print") as mock_print:
        output.tool_call("Tool", {"key": "value", "num": 123})
        assert mock_print.call_count > 1

    # Invalid JSON (should fall back to str)
    class NonSerializable:
        def __repr__(self):
            return "NonSerializable"

    with patch("builtins.print") as mock_print:
        output.tool_call("Tool", NonSerializable())
        calls = [str(call) for call in mock_print.call_args_list]
        assert any("NonSerializable" in call for call in calls)


def test_assistant_message_with_elapsed():
    """Test assistant message with elapsed time."""
    set_theme("minimal")
    output = get_output()

    with patch("builtins.print") as mock_print:
        output.assistant_message("Response", elapsed=1.234)
        mock_print.assert_called_with("\nAssistant (1.23s): Response", file=sys.stdout)

    set_theme("terminal")
    with patch.object(output._console, "print") as mock_print:
        output.assistant_message("Response", elapsed=2.5)
        call_str = str(mock_print.call_args_list[0])
        assert "2.50s" in call_str


def test_print_table_as_text():
    """Test table to text conversion."""
    from rich.table import Table

    set_theme("minimal")
    output = get_output()

    table = Table()
    table.add_column("Name")
    table.add_column("Age")
    table.add_row("Alice", "30")
    table.add_row("Bob", "25")

    # In minimal theme, print_table delegates to _print_table_as_text which uses _plain_print
    with patch.object(output, "_print_table_as_text") as mock_print_table:
        output.print_table(table)
        mock_print_table.assert_called_once_with(table)


def test_delegated_methods():
    """Test methods that delegate to other modules."""
    output = get_output()

    # Test tree
    with patch("chuk_term.ui.formatters.format_tree") as mock_tree:
        mock_tree.return_value = "tree"
        output.tree({"root": {}})
        mock_tree.assert_called()

    # Test json
    with patch("chuk_term.ui.formatters.format_json") as mock_json:
        mock_json.return_value = "json"
        output.json({"key": "val"})
        mock_json.assert_called()

    # Test code
    with patch("chuk_term.ui.code.display_code") as mock_code:
        output.code("print('hello')")
        mock_code.assert_called()


def test_confirm_and_prompt():
    """Test user input methods."""
    output = get_output()

    # Confirm with various inputs
    with patch("builtins.input", return_value="y"):
        assert output.confirm("Continue?")

    with patch("builtins.input", return_value="n"):
        assert not output.confirm("Continue?")

    with patch("builtins.input", return_value=""):
        assert output.confirm("Continue?", default=True)

    # Prompt
    with patch("builtins.input", return_value="answer"):
        assert output.prompt("Question?") == "answer"

    with patch("builtins.input", return_value=""):
        assert output.prompt("Question?", default="default") == "default"


def test_convenience_functions():
    """Test module-level convenience functions."""
    from chuk_term.ui.output import clear, command, debug, error, hint, info, rule, status, success, tip, warning

    output = get_output()

    with patch.object(output, "info") as mock:
        info("test")
        mock.assert_called_with("test")

    with patch.object(output, "success") as mock:
        success("test")
        mock.assert_called_with("test")

    with patch.object(output, "warning") as mock:
        warning("test")
        mock.assert_called_with("test")

    with patch.object(output, "error") as mock:
        error("test")
        mock.assert_called_with("test")

    with patch.object(output, "debug") as mock:
        debug("test")
        mock.assert_called_with("test")

    with patch.object(output, "tip") as mock:
        tip("test")
        mock.assert_called_with("test")

    with patch.object(output, "hint") as mock:
        hint("test")
        mock.assert_called_with("test")

    with patch.object(output, "command") as mock:
        command("test")
        mock.assert_called_with("test", "")

    with patch.object(output, "status") as mock:
        status("test")
        mock.assert_called_with("test")

    with patch.object(output, "clear") as mock:
        clear()
        mock.assert_called()

    with patch.object(output, "rule") as mock:
        rule("test")
        mock.assert_called_with("test")
