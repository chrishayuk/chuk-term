#!/usr/bin/env python3
"""
Streaming Quick Start

Simple examples to get started with streaming in chuk-term.
Copy and adapt these patterns for your own applications!

Usage:
    uv run examples/ui_streaming_quickstart.py
"""

import asyncio
import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_term.ui.output import info, rule, success
from chuk_term.ui.streaming import StreamingAssistant, StreamingMessage


def example_1_basic():
    """Example 1: Basic streaming message."""
    rule("Example 1: Basic Streaming", style="cyan")
    print()

    # Simplest way to stream a message
    with StreamingMessage() as stream:
        stream.update("Hello ")
        time.sleep(0.5)
        stream.update("world!")
        time.sleep(0.5)

    print()
    success("Message automatically finalized!")
    print()


def example_2_assistant():
    """Example 2: Using StreamingAssistant."""
    rule("Example 2: Streaming Assistant", style="green")
    print()

    # StreamingAssistant provides a simpler API
    assistant = StreamingAssistant()

    # Start streaming
    assistant.start()

    # Add content
    for word in ["This", "is", "a", "streaming", "assistant", "message!"]:
        assistant.update(word + " ")
        time.sleep(0.2)

    # Finalize
    assistant.finalize()

    print()
    success("Assistant message complete!")
    print()


def example_3_markdown():
    """Example 3: Streaming with Markdown."""
    rule("Example 3: Markdown Formatting", style="blue")
    print()

    with StreamingMessage(title="📝 Formatted Message") as stream:
        # Stream Markdown content
        content = """## Important Information

This message supports **Markdown** formatting:
- Bullet points
- *Italic text*
- **Bold text**
- `Code snippets`

Even code blocks:
```python
def hello():
    print("Hello, World!")
```
"""
        # Stream it character by character for effect
        for char in content:
            stream.update(char)
            time.sleep(0.01)

    print()
    success("Markdown rendered automatically on finalization!")
    print()


async def example_4_async():
    """Example 4: Async streaming."""
    rule("Example 4: Async Streaming", style="yellow")
    print()

    async def generate_content():
        """Simulate async content generation."""
        words = ["Async", "streaming", "is", "perfect", "for", "non-blocking", "I/O", "operations!"]
        for word in words:
            await asyncio.sleep(0.2)
            yield word + " "

    with StreamingMessage(title="⚡ Async Demo") as stream:
        async for chunk in generate_content():
            stream.update(chunk)

    print()
    success("Async streaming complete!")
    print()


def example_5_realtime():
    """Example 5: Real-time updates."""
    rule("Example 5: Real-time Updates", style="magenta")
    print()

    with StreamingMessage(title="📊 Live Data", show_elapsed=True) as stream:
        for i in range(5):
            # Use set_content to replace entire content
            stream.set_content(
                f"""
## Current Status

**Iteration:** {i + 1}/5
**Progress:** {"█" * (i + 1)}{"░" * (4 - i)}
**Status:** {"Processing..." if i < 4 else "Complete!"}
"""
            )
            time.sleep(0.5)

    print()
    success("Real-time updates complete!")
    print()


def example_6_error_handling():
    """Example 6: Error handling."""
    rule("Example 6: Error Handling", style="red")
    print()

    try:
        with StreamingMessage(title="⚠️ Error Demo") as stream:
            stream.update("Processing")
            time.sleep(0.3)
            stream.update("...")
            time.sleep(0.3)

            # Even if an error occurs, the message is finalized
            raise ValueError("Something went wrong!")

    except ValueError as e:
        print()
        info(f"Error caught: {e}")
        info("Note: Message was still properly finalized!")

    print()


def example_7_custom_title():
    """Example 7: Custom titles and timing."""
    rule("Example 7: Customization", style="cyan")
    print()

    # Customize title and disable elapsed time
    with StreamingMessage(title="🚀 Custom Title", show_elapsed=False) as stream:
        stream.update("You can customize:\n")
        time.sleep(0.5)
        stream.update("- The title\n")
        time.sleep(0.5)
        stream.update("- Whether to show elapsed time\n")
        time.sleep(0.5)
        stream.update("- And more!")
        time.sleep(0.5)

    print()
    success("Customization complete!")
    print()


async def main():
    """Run all examples."""
    info("🚀 Streaming Quick Start - Simple Examples")
    print()
    info("These examples show basic streaming patterns.")
    info("Press Enter after each example to continue...")
    print()
    input("Press Enter to start...")
    print()

    # Run examples
    examples = [
        ("Basic Streaming", example_1_basic),
        ("Streaming Assistant", example_2_assistant),
        ("Markdown Formatting", example_3_markdown),
        ("Async Streaming", lambda: asyncio.run(example_4_async())),
        ("Real-time Updates", example_5_realtime),
        ("Error Handling", example_6_error_handling),
        ("Customization", example_7_custom_title),
    ]

    for name, func in examples:
        try:
            if asyncio.iscoroutinefunction(func):
                await func()
            else:
                func()

            input("Press Enter for next example...")
            print()
        except KeyboardInterrupt:
            print("\nSkipping to next...")
            continue
        except Exception as e:
            print(f"Error in {name}: {e}")
            continue

    rule("✨ Quick Start Complete!", style="bold green")
    print()
    success("You've learned the basics of streaming in chuk-term!")
    print()
    info("Next steps:")
    print("  • Check ui_streaming_message_demo.py for more examples")
    print("  • See ui_streaming_practical_demo.py for real-world use cases")
    print("  • Read the StreamingMessage docstring for full API details")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
    sys.exit(0)
