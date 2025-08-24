# tests/ui/test_additional_coverage.py
"""
Additional tests to improve coverage for UI modules.
"""
from __future__ import annotations

from chuk_term.ui import get_output
from chuk_term.ui.theme import Theme


class TestOutputAdditional:
    """Additional output tests for coverage."""

    def test_output_tip(self, capsys):
        """Test tip output."""
        output = get_output()
        output.tip("This is a tip")
        captured = capsys.readouterr()
        assert "This is a tip" in captured.out

    def test_output_hint(self, capsys):
        """Test hint output."""
        output = get_output()
        output.hint("This is a hint")
        captured = capsys.readouterr()
        assert "This is a hint" in captured.out

    def test_output_command(self, capsys):
        """Test command output."""
        output = get_output()
        output.command("ls -la", "List files")
        captured = capsys.readouterr()
        assert "ls -la" in captured.out

    def test_output_status(self, capsys):
        """Test status output."""
        output = get_output()
        output.status("Processing...")
        captured = capsys.readouterr()
        assert "Processing..." in captured.out

    def test_output_fatal(self):
        """Test fatal output."""
        output = get_output()
        # Just test that it doesn't crash - output goes through Rich console
        output.fatal("Fatal error!")

    def test_output_user_message(self, capsys):
        """Test user message output."""
        output = get_output()
        output.user_message("User input here")
        captured = capsys.readouterr()
        assert "User" in captured.out or "input" in captured.out

    def test_output_assistant_message(self, capsys):
        """Test assistant message output."""
        output = get_output()
        output.assistant_message("Assistant response", elapsed=1.5)
        captured = capsys.readouterr()
        assert "Assistant" in captured.out or "response" in captured.out

    def test_output_tool_call(self, capsys):
        """Test tool call output."""
        output = get_output()
        output.tool_call("search", {"query": "test"})
        captured = capsys.readouterr()
        assert "search" in captured.out or "query" in captured.out

    def test_output_tree(self, capsys):
        """Test tree output."""
        output = get_output()
        data = {"root": {"child1": "value1", "child2": "value2"}}
        output.tree(data, title="Test Tree")
        captured = capsys.readouterr()
        assert "root" in captured.out or "Test Tree" in captured.out

    def test_output_list_items(self, capsys):
        """Test list items output."""
        output = get_output()
        items = ["item1", "item2", "item3"]
        output.list_items(items, style="bullet")
        captured = capsys.readouterr()
        assert "item1" in captured.out

    def test_output_json(self, capsys):
        """Test JSON output."""
        output = get_output()
        data = {"key": "value", "number": 42}
        output.json(data)
        captured = capsys.readouterr()
        assert "key" in captured.out or "42" in captured.out

    def test_output_code(self, capsys):
        """Test code output."""
        output = get_output()
        code = "def test():\n    return True"
        output.code(code, language="python")
        captured = capsys.readouterr()
        assert "def" in captured.out or "test" in captured.out

    def test_output_kvpairs(self, capsys):
        """Test key-value pairs output."""
        output = get_output()
        data = {"name": "test", "value": 123}
        output.kvpairs(data)
        captured = capsys.readouterr()
        assert "name" in captured.out or "123" in captured.out

    def test_output_columns(self, capsys):
        """Test columns output."""
        output = get_output()
        data = [["a", "b"], ["c", "d"]]
        headers = ["Col1", "Col2"]
        output.columns(data, headers=headers)
        captured = capsys.readouterr()
        assert "Col1" in captured.out or "a" in captured.out

    def test_output_clear(self):
        """Test clear screen."""
        output = get_output()
        # Just test that it doesn't crash
        output.clear()

    def test_output_rule(self, capsys):
        """Test rule output."""
        output = get_output()
        output.rule("Section Title")
        captured = capsys.readouterr()
        assert "Section Title" in captured.out

    def test_output_quiet_mode(self, capsys):
        """Test quiet mode suppresses normal output."""
        output = get_output()
        output.set_output_mode(quiet=True)
        output.info("Should not appear")
        output.set_output_mode(quiet=False)  # Reset
        captured = capsys.readouterr()
        assert "Should not appear" not in captured.out

    def test_output_verbose_mode(self, capsys):
        """Test verbose mode shows debug output."""
        output = get_output()
        output.set_output_mode(verbose=True)
        output.debug("Debug message")
        output.set_output_mode(verbose=False)  # Reset
        captured = capsys.readouterr()
        assert "Debug message" in captured.out

    def test_output_panel_minimal_theme(self, capsys):
        """Test panel in minimal theme."""
        output = get_output()
        output.set_theme(Theme("minimal"))
        output.panel("Panel content", title="Title")
        output.set_theme(Theme("default"))  # Reset
        captured = capsys.readouterr()
        assert "Panel content" in captured.out

    def test_output_markdown(self, capsys):
        """Test markdown output."""
        output = get_output()
        output.markdown("# Header\n\nText content")
        captured = capsys.readouterr()
        assert "Header" in captured.out or "Text content" in captured.out

    def test_output_progress_context(self):
        """Test progress context manager."""
        output = get_output()
        with output.progress("Processing...") as progress:
            assert progress is not None

    def test_output_loading_context(self):
        """Test loading context manager."""
        output = get_output()
        with output.loading("Loading...") as loading:
            assert loading is not None
