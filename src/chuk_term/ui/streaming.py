# src/chuk_term/ui/streaming.py
"""
Streaming message support for chuk-term.

Provides a way to display messages that update in real-time as content streams in,
then finalize with proper formatting.
"""
from __future__ import annotations

import time

from rich.console import Console, RenderableType
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from chuk_term.ui.theme import get_theme


class StreamingMessage:
    """
    A message that can be updated as content streams in.

    Usage:
        with StreamingMessage() as stream:
            stream.update("Hello")
            stream.update(" world")
            stream.update("!")
        # Automatically finalizes when context exits
    """

    def __init__(
        self,
        console: Console | None = None,
        title: str = "Assistant",
        show_elapsed: bool = True,
        refresh_per_second: int = 8,
    ):
        """
        Initialize a streaming message.

        Args:
            console: Rich console to use (creates one if None)
            title: Title for the message panel
            show_elapsed: Whether to show elapsed time
            refresh_per_second: Refresh rate for live updates (default 8fps for smoother streaming)
        """
        self.console = console or Console()
        self.title = title
        self.show_elapsed = show_elapsed
        self.refresh_per_second = refresh_per_second
        self.content = ""
        self.start_time: float | None = None
        self.live: Live | None = None
        self._theme = get_theme()
        self._finalized = False

    def __enter__(self):
        """Start the streaming display."""
        self.start_time = time.time()
        self.live = Live(
            self._create_panel(),
            console=self.console,
            refresh_per_second=self.refresh_per_second,
            transient=True,  # Will be replaced by final panel
        )
        self.live.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Finalize the streaming display."""
        if not self._finalized:
            self.finalize()

    def update(self, text: str):
        """
        Add text to the streaming message.

        Args:
            text: Text to append to the message
        """
        if self._finalized:
            return

        self.content += text
        if self.live:
            self.live.update(self._create_panel())

    def set_content(self, text: str):
        """
        Replace the entire content of the streaming message.

        Args:
            text: New complete text for the message
        """
        if self._finalized:
            return

        self.content = text
        if self.live:
            self.live.update(self._create_panel())

    def _create_panel(self, final: bool = False) -> Panel:
        """
        Create a panel for the current content.

        Args:
            final: Whether this is the final panel (uses Markdown rendering)

        Returns:
            Panel with the current content
        """
        # Get style from theme
        style_info = self._theme.get_component_style("assistant_message")

        # Prepare title
        title = self.title
        if not self._theme.should_show_icons() and title:
            import re

            title = re.sub(r"[^\x00-\x7F]+", "", title).strip()
            if not title:
                title = "Assistant"

        # Prepare subtitle with elapsed time
        subtitle = None
        if self.show_elapsed and self.start_time:
            elapsed = time.time() - self.start_time
            subtitle = f"Response time: {elapsed:.2f}s" if final else f"Streaming... {elapsed:.1f}s"

        # Create content
        content: RenderableType
        if final:
            # CRITICAL FIX: Ensure we use the full content, not truncated
            # Use Text with overflow handling for safety
            full_text = self.content or "[No Response]"

            # Debug logging for panel creation
            import logging

            logger = logging.getLogger(__name__)
            logger.debug(f"Panel creation: full_text length: {len(full_text)}")
            try:
                # Try Markdown first
                content = Markdown(full_text)
            except Exception:
                # Fall back to Text with explicit overflow handling
                content = Text(full_text, overflow="fold")
        else:
            # Use plain text during streaming for performance
            content = Text(self.content + "▌" if self.content else "▌", overflow="fold")  # Add cursor

        # Create panel with subtitle in footer if available
        # Use theme-driven border style
        border_style = style_info.get("border_style", "blue")

        # CRITICAL FIX: Don't rely on expand alone, ensure width is not constrained
        panel = Panel(
            content,
            title=title,
            border_style=border_style,
            expand=True,  # Expand to full terminal width
            width=None,  # Don't constrain width
        )

        # Rich Panel uses subtitle_align, not subtitle directly
        if subtitle:
            panel.subtitle = subtitle
            panel.subtitle_align = "right"

        return panel

    def finalize(self):
        """
        Finalize the streaming message with proper formatting.

        This stops the live display and shows the final formatted panel.
        """
        if self._finalized:
            return

        self._finalized = True

        if self.live:
            # Stop the live display
            self.live.stop()

            # CRITICAL FIX: Log content length for debugging
            import logging

            logger = logging.getLogger(__name__)
            logger.debug(f"Finalizing with content length: {len(self.content)}")

            # Show the final formatted panel with full content
            final_panel = self._create_panel(final=True)
            self.console.print(final_panel)


class StreamingAssistant:
    """
    Helper class for streaming assistant responses.

    This provides a simpler API specifically for assistant messages.
    """

    def __init__(self, console: Console | None = None):
        """Initialize the streaming assistant."""
        self.console = console or Console()
        self.stream: StreamingMessage | None = None

    def start(self) -> StreamingMessage:
        """Start streaming an assistant message."""
        self.stream = StreamingMessage(
            console=self.console,
            title="🤖 Assistant",
            show_elapsed=True,
        )
        self.stream.__enter__()
        return self.stream

    def update(self, text: str):
        """Update the streaming message."""
        if self.stream:
            self.stream.update(text)

    def finalize(self):
        """Finalize the streaming message."""
        if self.stream:
            self.stream.finalize()
            self.stream = None
