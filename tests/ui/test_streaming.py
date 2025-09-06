"""
Tests for the streaming module.
"""

import time
from unittest.mock import Mock, patch

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from chuk_term.ui.streaming import StreamingAssistant, StreamingMessage
from chuk_term.ui.theme import set_theme


class TestStreamingMessage:
    """Test StreamingMessage class."""

    def test_initialization(self):
        """Test StreamingMessage initialization."""
        msg = StreamingMessage()
        assert msg.title == "Assistant"
        assert msg.show_elapsed is True
        assert msg.content == ""
        assert msg.start_time is None
        assert msg.live is None
        assert msg._finalized is False

    def test_initialization_with_params(self):
        """Test StreamingMessage initialization with custom parameters."""
        console = Console()
        msg = StreamingMessage(
            console=console,
            title="Custom Title",
            show_elapsed=False,
        )
        assert msg.console == console
        assert msg.title == "Custom Title"
        assert msg.show_elapsed is False

    def test_context_manager_enter(self):
        """Test StreamingMessage context manager enter."""
        msg = StreamingMessage()
        with patch.object(Live, "start") as mock_start:
            returned = msg.__enter__()
            assert returned == msg
            assert msg.start_time is not None
            assert msg.live is not None
            mock_start.assert_called_once()

    def test_context_manager_exit(self):
        """Test StreamingMessage context manager exit."""
        msg = StreamingMessage()
        msg.start_time = time.time()
        msg.live = Mock(spec=Live)

        with patch.object(msg, "finalize") as mock_finalize:
            msg.__exit__(None, None, None)
            mock_finalize.assert_called_once()

    def test_context_manager_exit_already_finalized(self):
        """Test context manager exit when already finalized."""
        msg = StreamingMessage()
        msg._finalized = True

        with patch.object(msg, "finalize") as mock_finalize:
            msg.__exit__(None, None, None)
            mock_finalize.assert_not_called()

    def test_update(self):
        """Test updating streaming message."""
        msg = StreamingMessage()
        msg.live = Mock(spec=Live)

        msg.update("Hello ")
        assert msg.content == "Hello "
        msg.live.update.assert_called()

        msg.update("world!")
        assert msg.content == "Hello world!"
        assert msg.live.update.call_count == 2

    def test_update_when_finalized(self):
        """Test update does nothing when finalized."""
        msg = StreamingMessage()
        msg._finalized = True
        msg.live = Mock(spec=Live)

        msg.update("test")
        assert msg.content == ""
        msg.live.update.assert_not_called()

    def test_set_content(self):
        """Test setting entire content."""
        msg = StreamingMessage()
        msg.live = Mock(spec=Live)

        msg.set_content("New content")
        assert msg.content == "New content"
        msg.live.update.assert_called()

        msg.set_content("Replaced")
        assert msg.content == "Replaced"
        assert msg.live.update.call_count == 2

    def test_set_content_when_finalized(self):
        """Test set_content does nothing when finalized."""
        msg = StreamingMessage()
        msg._finalized = True
        msg.live = Mock(spec=Live)

        msg.set_content("test")
        assert msg.content == ""
        msg.live.update.assert_not_called()

    def test_create_panel_streaming(self):
        """Test creating panel during streaming."""
        msg = StreamingMessage()
        msg.content = "Test content"
        msg.start_time = time.time()

        panel = msg._create_panel(final=False)
        assert isinstance(panel, Panel)
        assert isinstance(panel.renderable, Text)
        # Should have cursor during streaming
        assert "▌" in panel.renderable.plain

    def test_create_panel_final(self):
        """Test creating final panel with Markdown."""
        msg = StreamingMessage()
        msg.content = "# Test\n\nContent"
        msg.start_time = time.time()

        panel = msg._create_panel(final=True)
        assert isinstance(panel, Panel)
        assert isinstance(panel.renderable, Markdown)

    def test_create_panel_final_markdown_error(self):
        """Test fallback to Text when Markdown fails."""
        msg = StreamingMessage()
        msg.content = "Test"
        msg.start_time = time.time()

        with patch("chuk_term.ui.streaming.Markdown", side_effect=Exception("Markdown error")):
            panel = msg._create_panel(final=True)
            assert isinstance(panel, Panel)
            assert isinstance(panel.renderable, Text)

    def test_create_panel_no_content(self):
        """Test creating panel with no content."""
        msg = StreamingMessage()
        msg.content = ""

        panel = msg._create_panel(final=True)
        assert isinstance(panel, Panel)
        # Should show [No Response] when empty
        if isinstance(panel.renderable, Text):
            assert "[No Response]" in panel.renderable.plain

    def test_create_panel_minimal_theme(self):
        """Test panel creation with minimal theme."""
        set_theme("minimal")
        msg = StreamingMessage(title="🤖 Test")
        msg.content = "Test"

        panel = msg._create_panel()
        # Minimal theme should strip emojis
        assert panel.title == "Test" or panel.title == "Assistant"

        set_theme("default")  # Reset

    def test_create_panel_with_elapsed_time(self):
        """Test panel with elapsed time display."""
        msg = StreamingMessage(show_elapsed=True)
        msg.content = "Test"
        msg.start_time = time.time() - 2.5  # 2.5 seconds ago

        panel = msg._create_panel(final=False)
        assert panel.subtitle is not None
        assert "Streaming" in panel.subtitle

        panel = msg._create_panel(final=True)
        assert panel.subtitle is not None
        assert "Response time" in panel.subtitle

    def test_create_panel_no_elapsed_time(self):
        """Test panel without elapsed time."""
        msg = StreamingMessage(show_elapsed=False)
        msg.content = "Test"
        msg.start_time = time.time()

        panel = msg._create_panel()
        assert panel.subtitle is None

    def test_finalize(self):
        """Test finalizing the streaming message."""
        msg = StreamingMessage()
        msg.start_time = time.time()
        msg.content = "Test content"
        msg.live = Mock(spec=Live)
        msg.console = Mock(spec=Console)

        msg.finalize()

        assert msg._finalized is True
        msg.live.stop.assert_called_once()
        msg.console.print.assert_called_once()

        # Should be a Panel
        call_args = msg.console.print.call_args[0]
        assert isinstance(call_args[0], Panel)

    def test_finalize_already_finalized(self):
        """Test finalize does nothing if already finalized."""
        msg = StreamingMessage()
        msg._finalized = True
        msg.live = Mock(spec=Live)
        msg.console = Mock(spec=Console)

        msg.finalize()

        msg.live.stop.assert_not_called()
        msg.console.print.assert_not_called()

    def test_finalize_no_live(self):
        """Test finalize when live is None."""
        msg = StreamingMessage()
        msg.console = Mock(spec=Console)

        msg.finalize()
        assert msg._finalized is True
        # Should not crash

    def test_full_context_manager_flow(self):
        """Test complete context manager flow."""
        with StreamingMessage() as stream:
            assert stream.start_time is not None
            assert stream.live is not None
            assert not stream._finalized

            stream.update("Hello ")
            stream.update("world!")
            assert stream.content == "Hello world!"

        # After context exit, should be finalized
        assert stream._finalized


class TestStreamingAssistant:
    """Test StreamingAssistant class."""

    def test_initialization(self):
        """Test StreamingAssistant initialization."""
        assistant = StreamingAssistant()
        assert assistant.stream is None
        assert assistant.console is not None

    def test_initialization_with_console(self):
        """Test initialization with custom console."""
        console = Console()
        assistant = StreamingAssistant(console=console)
        assert assistant.console == console

    def test_start(self):
        """Test starting a streaming message."""
        assistant = StreamingAssistant()

        with patch.object(StreamingMessage, "__enter__", return_value=None) as mock_enter:
            stream = assistant.start()

            assert assistant.stream is not None
            assert isinstance(stream, StreamingMessage)
            assert stream.title == "🤖 Assistant"
            assert stream.show_elapsed is True
            mock_enter.assert_called_once()

    def test_update(self):
        """Test updating the streaming message."""
        assistant = StreamingAssistant()
        assistant.stream = Mock(spec=StreamingMessage)

        assistant.update("Test text")
        assistant.stream.update.assert_called_once_with("Test text")

    def test_update_no_stream(self):
        """Test update when no stream is active."""
        assistant = StreamingAssistant()
        assistant.update("Test")  # Should not crash

    def test_finalize(self):
        """Test finalizing the streaming message."""
        assistant = StreamingAssistant()
        mock_stream = Mock(spec=StreamingMessage)
        assistant.stream = mock_stream

        assistant.finalize()

        mock_stream.finalize.assert_called_once()
        assert assistant.stream is None

    def test_finalize_no_stream(self):
        """Test finalize when no stream is active."""
        assistant = StreamingAssistant()
        assistant.finalize()  # Should not crash

    def test_full_flow(self):
        """Test complete StreamingAssistant flow."""
        assistant = StreamingAssistant()

        # Start streaming
        stream = assistant.start()
        assert stream is not None
        assert assistant.stream == stream

        # Update content
        assistant.update("Hello ")
        assistant.update("world!")
        assert assistant.stream.content == "Hello world!"

        # Finalize
        with patch.object(assistant.stream, "finalize") as mock_finalize:
            assistant.finalize()
            mock_finalize.assert_called_once()
            assert assistant.stream is None


class TestIntegration:
    """Integration tests for streaming functionality."""

    def test_theme_switching(self):
        """Test streaming works with different themes."""
        themes = ["default", "minimal", "terminal", "dark", "light"]

        for theme_name in themes:
            set_theme(theme_name)

            with StreamingMessage(title="Test") as stream:
                stream.update("Testing theme: ")
                stream.update(theme_name)
                assert stream.content == f"Testing theme: {theme_name}"

        set_theme("default")  # Reset

    def test_empty_content_handling(self):
        """Test handling of empty content."""
        with StreamingMessage() as stream:
            # Don't add any content
            pass

        # Should handle empty content gracefully
        assert stream._finalized

    def test_long_content(self):
        """Test handling of long content."""
        long_text = "x" * 10000

        with StreamingMessage() as stream:
            stream.update(long_text)
            assert stream.content == long_text

    def test_multiline_content(self):
        """Test handling of multiline content."""
        content = """# Header

## Subheader

- Item 1
- Item 2
- Item 3

```python
def test():
    pass
```"""

        with StreamingMessage() as stream:
            # Update with the full content at once
            stream.update(content)
            assert stream.content == content

    def test_unicode_content(self):
        """Test handling of Unicode content."""
        unicode_text = "Hello 世界 🌍 émoji"

        with StreamingMessage() as stream:
            stream.update(unicode_text)
            assert stream.content == unicode_text

    def test_rapid_updates(self):
        """Test rapid successive updates."""
        with StreamingMessage() as stream:
            for i in range(100):
                stream.update(str(i))

            expected = "".join(str(i) for i in range(100))
            assert stream.content == expected

    def test_set_content_replacement(self):
        """Test content replacement with set_content."""
        with StreamingMessage() as stream:
            stream.update("Initial content")
            assert stream.content == "Initial content"

            stream.set_content("Replaced content")
            assert stream.content == "Replaced content"

            stream.update(" + more")
            assert stream.content == "Replaced content + more"
