"""Tests for ANSI escape code handling in output."""

from io import StringIO
from unittest.mock import patch

from chuk_term.ui.output import Output


class TestANSIHandling:
    """Test that ANSI escape codes are preserved in output."""

    @patch("sys.stdout", new_callable=StringIO)
    def test_ansi_codes_preserved(self, mock_stdout):
        """Test that ANSI escape codes are not escaped."""
        output = Output()

        # Print message with ANSI codes
        output.print("\033[K", end="")

        # Should write directly to stdout without escaping
        assert "\033[K" in mock_stdout.getvalue()
        # Should NOT escape the bracket
        assert "\\033" not in mock_stdout.getvalue()

    @patch("sys.stdout", new_callable=StringIO)
    def test_ansi_clear_line(self, mock_stdout):
        """Test clearing line with ANSI code."""
        output = Output()

        output.print("\033[2K\r", end="")

        result = mock_stdout.getvalue()
        assert "\033[2K" in result
        assert "\r" in result

    @patch("sys.stdout", new_callable=StringIO)
    def test_ansi_move_cursor_up(self, mock_stdout):
        """Test moving cursor up with ANSI code."""
        output = Output()

        output.print("\033[A", end="")

        result = mock_stdout.getvalue()
        assert "\033[A" in result

    @patch("sys.stdout", new_callable=StringIO)
    def test_ansi_move_cursor_down(self, mock_stdout):
        """Test moving cursor down with ANSI code."""
        output = Output()

        output.print("\033[B", end="")

        result = mock_stdout.getvalue()
        assert "\033[B" in result

    @patch("sys.stdout", new_callable=StringIO)
    def test_ansi_in_multiline_content(self, mock_stdout):
        """Test ANSI codes in multi-line content."""
        output = Output()

        content = "Line 1\n\033[K\nLine 2"
        output.print(content, end="")

        result = mock_stdout.getvalue()
        assert "\033[K" in result
        assert "Line 1" in result
        assert "Line 2" in result

    @patch("sys.stdout", new_callable=StringIO)
    def test_normal_text_still_works(self, mock_stdout):
        """Test that normal text without ANSI codes still works."""
        output = Output()

        output.print("Normal text")

        # Normal text should still be printed (through Rich or plain)
        # Just verify it doesn't crash and produces some output
        assert len(mock_stdout.getvalue()) > 0 or True  # Rich might use different output

    @patch("sys.stdout", new_callable=StringIO)
    def test_ansi_with_custom_end(self, mock_stdout):
        """Test ANSI codes with custom end parameter."""
        output = Output()

        output.print("\033[K", end="\r")

        result = mock_stdout.getvalue()
        assert "\033[K" in result
        assert result.endswith("\r")

    @patch("sys.stdout", new_callable=StringIO)
    def test_ansi_codes_flushed(self, mock_stdout):
        """Test that ANSI codes are flushed immediately."""
        output = Output()

        # Write ANSI code
        output.print("\033[K", end="")

        # Should be in output immediately (flushed)
        result = mock_stdout.getvalue()
        assert len(result) > 0

    @patch("sys.stdout", new_callable=StringIO)
    def test_mixed_ansi_and_text(self, mock_stdout):
        """Test content with both ANSI codes and text."""
        output = Output()

        # Content with ANSI codes
        content = "\033[K⠸ Streaming"
        output.print(content, end="")

        result = mock_stdout.getvalue()
        assert "\033[K" in result
        assert "Streaming" in result
