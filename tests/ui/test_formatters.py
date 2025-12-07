"""Unit tests for formatters module."""

# ruff: noqa: ARG002

import json
from datetime import datetime, timedelta

import pytest

from chuk_term.ui.formatters import (
    format_diff,
    format_error,
    format_json,
    format_table,
    format_timestamp,
    format_tool_call,
    format_tool_result,
    format_tree,
)
from chuk_term.ui.theme import Theme, set_theme


@pytest.fixture
def minimal_theme():
    """Set minimal theme for testing."""
    theme = Theme("minimal")
    set_theme("minimal")
    return theme


@pytest.fixture
def default_theme():
    """Set default theme for testing."""
    theme = Theme("default")
    set_theme("default")
    return theme


class TestFormatToolCall:
    """Test tool call formatting."""

    def test_format_tool_call_minimal(self, minimal_theme):
        """Test tool call formatting in minimal theme."""
        result = format_tool_call(
            "test_tool", {"arg1": "value1", "arg2": 123}, include_description=True, description="Test tool description"
        )

        assert isinstance(result, str)
        assert "Tool: test_tool" in result
        assert "Test tool description" in result
        assert "arg1" in result
        assert "value1" in result

    def test_format_tool_call_rich(self, default_theme):
        """Test tool call formatting in rich theme."""
        result = format_tool_call("test_tool", {"arg1": "value1"}, include_description=False)

        # Should return Markdown object for rich themes
        assert hasattr(result, "markup")  # Markdown has markup attribute

    def test_format_tool_call_no_arguments(self, minimal_theme):
        """Test tool call with no arguments."""
        result = format_tool_call("test_tool", {})

        assert "Tool: test_tool" in result
        assert "No arguments" in result


class TestFormatToolResult:
    """Test tool result formatting."""

    def test_format_tool_result_success(self, minimal_theme):
        """Test successful tool result formatting."""
        result = format_tool_result({"data": "test"}, success=True, execution_time=1.23)

        assert isinstance(result, str)
        assert "Success" in result
        assert "1.23s" in result
        assert "data" in result

    def test_format_tool_result_failure(self, minimal_theme):
        """Test failed tool result formatting."""
        result = format_tool_result("Error message", success=False)

        assert isinstance(result, str)
        assert "Failed" in result
        assert "Error message" in result

    def test_format_tool_result_rich(self, default_theme):
        """Test tool result in rich theme."""
        result = format_tool_result({"status": "ok"}, success=True, execution_time=0.5)

        # Rich themes return Text or Markdown
        assert result is not None


class TestFormatError:
    """Test error formatting."""

    def test_format_error_basic(self, minimal_theme):
        """Test basic error formatting."""
        error = ValueError("Test error")
        result = format_error(error)

        assert isinstance(result, str)
        assert "Error: ValueError" in result
        assert "Test error" in result

    def test_format_error_with_context(self, minimal_theme):
        """Test error with context."""
        error = RuntimeError("Failed")
        result = format_error(error, context="During processing", suggestions=["Check input", "Retry operation"])

        assert "Context: During processing" in result
        assert "Suggestions:" in result
        assert "Check input" in result
        assert "Retry operation" in result

    def test_format_error_with_traceback(self, minimal_theme):
        """Test error with traceback."""
        try:
            raise Exception("Test exception")
        except Exception as e:
            result = format_error(e, include_traceback=True)

            assert "Traceback:" in result
            assert "Test exception" in result


class TestFormatJson:
    """Test JSON formatting."""

    def test_format_json_basic(self, minimal_theme):
        """Test basic JSON formatting."""
        data = {"key": "value", "number": 42}
        result = format_json(data)

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["key"] == "value"
        assert parsed["number"] == 42

    def test_format_json_with_title(self, minimal_theme):
        """Test JSON with title."""
        data = {"test": True}
        result = format_json(data, title="Test JSON")

        assert "Test JSON" in result
        assert "test" in result

    def test_format_json_syntax_highlight(self, default_theme):
        """Test JSON with syntax highlighting."""
        data = {"highlighted": True}
        result = format_json(data, syntax_highlight=True)

        # Rich theme returns Syntax object
        assert hasattr(result, "lexer")  # Syntax objects have lexer

    def test_format_json_invalid_data(self, minimal_theme):
        """Test JSON formatting with non-serializable data."""

        # Create non-serializable object
        class NonSerializable:
            pass

        # Should handle gracefully with default=str
        result = format_json({"obj": NonSerializable()})
        assert isinstance(result, str)


class TestFormatTable:
    """Test table formatting."""

    def test_format_table_basic(self, minimal_theme):
        """Test basic table formatting."""
        data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
        result = format_table(data)

        assert isinstance(result, str)
        assert "Alice" in result
        assert "Bob" in result
        assert "30" in result
        assert "25" in result

    def test_format_table_with_title(self, minimal_theme):
        """Test table with title."""
        data = [{"col1": "val1"}]
        result = format_table(data, title="Test Table")

        assert "Test Table" in result
        assert "col1" in result
        assert "val1" in result

    def test_format_table_specific_columns(self, minimal_theme):
        """Test table with specific columns."""
        data = [{"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6}]
        result = format_table(data, columns=["a", "c"])

        assert "1" in result
        assert "3" in result
        assert "4" in result
        assert "6" in result
        # Column b should not appear
        assert "b" not in result

    def test_format_table_max_rows(self, minimal_theme):
        """Test table with max rows limit."""
        data = [{"n": i} for i in range(10)]
        result = format_table(data, max_rows=3)

        assert "showing 3 of 10 rows" in result.lower()

    def test_format_table_empty(self, minimal_theme):
        """Test empty table."""
        result = format_table([])
        assert "No data" in result


class TestFormatTree:
    """Test tree formatting."""

    def test_format_tree_basic(self, minimal_theme):
        """Test basic tree formatting."""
        data = {"root": {"child1": "value1", "child2": {"grandchild": "value2"}}}
        result = format_tree(data)

        assert isinstance(result, str)
        assert "root" in result
        assert "child1" in result
        assert "value1" in result
        assert "grandchild" in result

    def test_format_tree_with_title(self, minimal_theme):
        """Test tree with title."""
        data = {"node": "value"}
        result = format_tree(data, title="Test Tree")

        assert "Test Tree" in result
        assert "node" in result

    def test_format_tree_max_depth(self, minimal_theme):
        """Test tree with max depth."""
        data = {"level1": {"level2": {"level3": {"level4": "deep"}}}}
        result = format_tree(data, max_depth=2)

        assert "level1" in result
        assert "level2" in result
        assert "..." in result  # Truncation indicator

    def test_format_tree_with_lists(self, minimal_theme):
        """Test tree with list values."""
        data = {"items": ["a", "b", "c"], "nested": {"more": ["x", "y"]}}
        result = format_tree(data)

        assert "[0]" in result
        assert "[1]" in result
        assert "a" in result
        assert "b" in result


class TestFormatTimestamp:
    """Test timestamp formatting."""

    def test_format_timestamp_current(self):
        """Test formatting current timestamp."""
        result = format_timestamp()

        # Should contain date and time
        assert "-" in result  # Date separator
        assert ":" in result  # Time separator

    def test_format_timestamp_date_only(self):
        """Test date-only formatting."""
        dt = datetime(2024, 1, 15, 10, 30, 45)
        result = format_timestamp(dt, include_time=False)

        assert "2024-01-15" in result
        assert "10:30" not in result

    def test_format_timestamp_time_only(self):
        """Test time-only formatting."""
        dt = datetime(2024, 1, 15, 10, 30, 45)
        result = format_timestamp(dt, include_date=False)

        assert "10:30:45" in result
        assert "2024" not in result

    def test_format_timestamp_relative(self):
        """Test relative timestamp formatting."""
        # Test various time deltas
        now = datetime.now()

        # 30 seconds ago
        dt = now - timedelta(seconds=30)
        result = format_timestamp(dt, relative=True)
        assert "30 seconds ago" in result

        # 5 minutes ago
        dt = now - timedelta(minutes=5)
        result = format_timestamp(dt, relative=True)
        assert "5 minute" in result

        # 2 hours ago
        dt = now - timedelta(hours=2)
        result = format_timestamp(dt, relative=True)
        assert "2 hour" in result

        # 3 days ago
        dt = now - timedelta(days=3)
        result = format_timestamp(dt, relative=True)
        assert "3 day" in result


class TestFormatDiff:
    """Test diff formatting."""

    def test_format_diff_basic(self, minimal_theme):
        """Test basic diff formatting."""
        old = "line1\nline2\nline3"
        new = "line1\nmodified\nline3"

        result = format_diff(old, new)

        assert isinstance(result, str)
        assert "-line2" in result or "line2" in result
        assert "+modified" in result or "modified" in result

    def test_format_diff_with_title(self, minimal_theme):
        """Test diff with title."""
        old = "original"
        new = "changed"

        result = format_diff(old, new, title="Changes")

        assert "Changes" in result

    def test_format_diff_rich(self, default_theme):
        """Test diff in rich theme."""
        old = "foo"
        new = "bar"

        result = format_diff(old, new)

        # Rich theme returns Syntax object
        assert hasattr(result, "lexer")


class TestAdditionalCoverage:
    """Additional tests for complete coverage."""

    def test_format_tool_call_json_error_minimal(self, minimal_theme):
        """Test tool call with non-serializable arguments in minimal theme."""
        # Mock json.dumps to raise an exception
        from unittest.mock import patch

        with patch("chuk_term.ui.formatters.json.dumps", side_effect=Exception("Mock error")):
            result = format_tool_call("test_tool", {"arg": "value"})
            assert isinstance(result, str)
            assert "Tool: test_tool" in result

    def test_format_tool_call_json_error_rich(self, default_theme):
        """Test tool call with non-serializable arguments in rich theme."""
        # Mock json.dumps to raise an exception
        from unittest.mock import patch

        with patch("chuk_term.ui.formatters.json.dumps", side_effect=Exception("Mock error")):
            result = format_tool_call("test_tool", {"arg": "value"})
            assert result is not None

    def test_format_tool_call_with_description_rich(self, default_theme):
        """Test tool call with description in rich theme."""
        result = format_tool_call(
            "test_tool", {"arg": "value"}, include_description=True, description="This is a test tool"
        )
        assert hasattr(result, "markup")  # Markdown object

    def test_format_tool_call_no_args_rich(self, default_theme):
        """Test tool call with no arguments in rich theme."""
        result = format_tool_call("test_tool", {})
        assert hasattr(result, "markup")  # Markdown object

    def test_format_tool_result_non_dict_minimal(self, minimal_theme):
        """Test tool result with non-dict/list result in minimal theme."""
        result = format_tool_result("Simple string result", success=True)
        assert "Success" in result
        assert "Simple string result" in result

    def test_format_tool_result_json_error_minimal(self, minimal_theme):
        """Test tool result with non-serializable dict in minimal theme."""

        class NonSerializable:
            pass

        # dict with non-serializable value should fallback to str()
        result = format_tool_result({"obj": NonSerializable()}, success=True)
        assert isinstance(result, str)

    def test_format_tool_result_json_error_rich(self, default_theme):
        """Test tool result with non-serializable dict in rich theme."""

        class NonSerializable:
            pass

        # dict with non-serializable value should fallback to str()
        result = format_tool_result({"obj": NonSerializable()}, success=True)
        assert result is not None

    def test_format_tool_result_non_dict_rich(self, default_theme):
        """Test tool result with non-dict result in rich theme."""
        result = format_tool_result("Plain text result", success=False)
        assert result is not None

    def test_format_error_rich_full(self, default_theme):
        """Test error formatting in rich theme with all features."""
        try:
            raise ValueError("Test error in rich mode")
        except Exception as e:
            result = format_error(
                e,
                include_traceback=True,
                context="Testing rich theme error formatting",
                suggestions=["Try this", "Or try that"],
            )
            assert result is not None

    def test_format_error_rich_basic(self, default_theme):
        """Test basic error formatting in rich theme."""
        error = RuntimeError("Simple error")
        result = format_error(error)
        assert result is not None

    def test_format_json_error_handling(self, minimal_theme):
        """Test JSON formatting with truly non-serializable data."""

        class BadObject:
            def __repr__(self):
                raise Exception("Cannot represent")

            def __str__(self):
                raise Exception("Cannot stringify")

        # This should trigger the exception handler
        result = format_json(BadObject())
        assert "Error formatting JSON" in result

    def test_format_json_error_handling_rich(self, default_theme):
        """Test JSON formatting error in rich theme."""

        class BadObject:
            def __repr__(self):
                raise Exception("Cannot represent")

            def __str__(self):
                raise Exception("Cannot stringify")

        result = format_json(BadObject())
        assert result is not None

    def test_format_json_no_highlight_with_title(self, default_theme):
        """Test JSON without syntax highlighting but with title in rich theme."""
        data = {"test": "value"}
        result = format_json(data, syntax_highlight=False, title="Test Data")
        assert hasattr(result, "markup")  # Markdown object

    def test_format_json_no_highlight_no_title(self, default_theme):
        """Test JSON without syntax highlighting or title in rich theme."""
        data = {"simple": "data"}
        result = format_json(data, syntax_highlight=False)
        assert hasattr(result, "markup")  # Markdown object

    def test_format_table_empty_rich(self, default_theme):
        """Test empty table in rich theme."""
        from rich.table import Table

        result = format_table([])
        assert isinstance(result, Table)

    def test_format_table_empty_with_title_rich(self, default_theme):
        """Test empty table with title in rich theme."""
        from rich.table import Table

        result = format_table([], title="Empty Table")
        assert isinstance(result, Table)

    def test_format_table_rich_with_max_rows(self, default_theme):
        """Test table with max_rows in rich theme."""
        from rich.table import Table

        data = [{"id": i, "name": f"Item {i}"} for i in range(10)]
        result = format_table(data, max_rows=5)
        assert isinstance(result, Table)

    def test_format_table_rich_with_title(self, default_theme):
        """Test table with title in rich theme."""
        from rich.table import Table

        data = [{"col1": "val1", "col2": "val2"}]
        result = format_table(data, title="Test Table")
        assert isinstance(result, Table)

    def test_format_table_terminal_with_unicode(self):
        """Test table in terminal theme with unicode symbols."""
        set_theme("minimal")
        data = [{"status": "✓", "result": "✗", "marker": "●"}]
        result = format_table(data)
        assert "OK" in result or "X" in result or "*" in result

    def test_format_tree_rich(self, default_theme):
        """Test tree formatting in rich theme."""
        from rich.tree import Tree

        data = {"root": {"child": "value"}}
        result = format_tree(data)
        assert isinstance(result, Tree)

    def test_format_tree_rich_with_lists(self, default_theme):
        """Test tree with lists in rich theme."""
        from rich.tree import Tree

        data = {"items": ["a", "b"], "nested": {"more": ["x", "y"]}}
        result = format_tree(data)
        assert isinstance(result, Tree)

    def test_format_tree_rich_max_depth(self, default_theme):
        """Test tree with max depth in rich theme."""
        from rich.tree import Tree

        data = {"level1": {"level2": {"level3": "deep"}}}
        result = format_tree(data, max_depth=2)
        assert isinstance(result, Tree)

    def test_format_tree_rich_with_title(self, default_theme):
        """Test tree with title in rich theme."""
        from rich.tree import Tree

        data = {"node": "value"}
        result = format_tree(data, title="Custom Title")
        assert isinstance(result, Tree)

    def test_format_tree_rich_nested_dicts(self, default_theme):
        """Test tree with deeply nested dicts in rich theme."""
        from rich.tree import Tree

        data = {"a": {"b": {"c": {"d": "value"}}}}
        result = format_tree(data)
        assert isinstance(result, Tree)

    def test_format_tree_rich_mixed_types(self, default_theme):
        """Test tree with mixed types in rich theme."""
        from rich.tree import Tree

        data = {"string": "value", "number": 42, "nested": {"list": [1, 2, 3]}}
        result = format_tree(data)
        assert isinstance(result, Tree)

    def test_format_tree_terminal_theme(self):
        """Test tree formatting in terminal theme."""
        set_theme("terminal")
        data = {"root": {"child": "value"}}
        result = format_tree(data)
        assert isinstance(result, str)
        assert "root" in result

    def test_format_tree_rich_with_scalar_values(self, default_theme):
        """Test tree with scalar values in rich theme."""
        from rich.tree import Tree

        data = {"key1": "string", "key2": 123, "key3": True}
        result = format_tree(data)
        assert isinstance(result, Tree)

    def test_format_tree_rich_list_with_scalars(self, default_theme):
        """Test tree with list of scalar values in rich theme."""
        from rich.tree import Tree

        data = ["item1", "item2", "item3"]
        result = format_tree(data)
        assert isinstance(result, Tree)

    def test_format_tree_minimal_with_scalar(self):
        """Test tree with scalar value in minimal theme."""
        set_theme("minimal")
        data = "just a string"
        result = format_tree(data)
        assert isinstance(result, str)

    def test_format_tree_minimal_list_with_nested(self):
        """Test tree with nested list in minimal theme."""
        set_theme("minimal")
        data = [{"nested": "dict"}, ["nested", "list"]]
        result = format_tree(data)
        assert isinstance(result, str)
        assert "[0]" in result
        assert "[1]" in result
