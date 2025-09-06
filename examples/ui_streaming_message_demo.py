#!/usr/bin/env python3
"""
Streaming Message Demo

Demonstrates the StreamingMessage and StreamingAssistant classes
for creating live-updating messages with automatic finalization.

Usage:
    uv run examples/ui_streaming_message_demo.py
"""

import asyncio
import sys
import time
from collections.abc import AsyncIterator
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


from chuk_term.ui.output import clear, get_output, info, rule, success, warning
from chuk_term.ui.streaming import StreamingAssistant, StreamingMessage
from chuk_term.ui.theme import set_theme


async def demo_basic_streaming():
    """Basic streaming message example."""
    clear()
    rule("📝 Basic Streaming Message", style="bold blue")
    print()

    info("Demonstrating basic streaming message with automatic finalization...")
    print()

    # Use StreamingMessage as a context manager
    with StreamingMessage(title="🤖 Assistant") as stream:
        # Simulate streaming content
        messages = [
            "Hello! ",
            "I'm processing your request",
            "...\n\n",
            "Let me help you with that. ",
            "Here's what I found:\n\n",
            "## Key Points\n",
            "1. First important point\n",
            "2. Second important point\n",
            "3. Third important point\n\n",
            "That's the complete analysis!",
        ]

        for msg in messages:
            stream.update(msg)
            time.sleep(0.3)  # Simulate network delay

    # Message is automatically finalized when context exits
    print()
    success("Message finalized with Markdown rendering!")


async def demo_streaming_assistant():
    """Demonstrate the StreamingAssistant helper."""
    clear()
    rule("🤖 Streaming Assistant", style="bold cyan")
    print()

    info("Using StreamingAssistant for simpler API...")
    print()

    assistant = StreamingAssistant()

    # Start streaming
    assistant.start()

    # Simulate LLM response
    response = """I'll help you understand streaming in chuk-term.

## What is Streaming?

Streaming allows you to display content progressively as it arrives,
rather than waiting for the complete response. This creates a more
interactive and responsive user experience.

### Benefits:
- **Immediate feedback** - Users see content as soon as it's available
- **Better UX** - No long waits for complete responses
- **Memory efficient** - Process data in chunks
- **Real-time updates** - Perfect for live data

### Implementation Details:
The `StreamingMessage` class provides:
1. Live updating display during streaming
2. Automatic Markdown rendering on completion
3. Elapsed time tracking
4. Theme-aware styling

This creates a polished, professional streaming experience!"""

    # Stream character by character
    for char in response:
        assistant.update(char)
        await asyncio.sleep(0.01)  # Simulate typing speed

    # Finalize the message
    assistant.finalize()

    print()
    success("Assistant message complete with full formatting!")


async def demo_async_generator_streaming():
    """Demonstrate streaming with async generators (LLM-style)."""
    clear()
    rule("🚀 Async Generator Streaming", style="bold green")
    print()

    info("Simulating LLM API with async generator...")
    print()

    async def generate_llm_response() -> AsyncIterator[str]:
        """Simulate an LLM API that yields chunks."""
        chunks = [
            "I'll explain ",
            "how async generators ",
            "work with streaming.\n\n",
            "## Async Generators\n\n",
            "Async generators are perfect for ",
            "streaming because they:\n",
            "- Yield values asynchronously\n",
            "- Handle backpressure naturally\n",
            "- Integrate with `async`/`await`\n\n",
            "### Example Code:\n",
            "```python\n",
            "async def stream_data():\n",
            "    async for chunk in api.generate():\n",
            "        yield process(chunk)\n",
            "```\n\n",
            "This pattern enables efficient, ",
            "non-blocking streaming!",
        ]

        for chunk in chunks:
            # Simulate network latency
            await asyncio.sleep(0.1)
            yield chunk

    # Stream the response
    with StreamingMessage(title="🤖 LLM Response") as stream:
        async for chunk in generate_llm_response():
            stream.update(chunk)

    print()
    success("Async generator streaming complete!")


async def demo_multiple_streams():
    """Demonstrate multiple streaming messages."""
    clear()
    rule("🔄 Multiple Streaming Messages", style="bold yellow")
    print()

    info("Showing multiple streaming messages in sequence...")
    print()

    # First message
    with StreamingMessage(title="📊 Data Analysis") as stream:
        stream.update("Analyzing dataset...")
        await asyncio.sleep(0.5)
        stream.update("\nFound 1,234 records")
        await asyncio.sleep(0.5)
        stream.update("\nProcessing complete!")
        await asyncio.sleep(0.5)

    print()

    # Second message
    with StreamingMessage(title="🔍 Search Results") as stream:
        stream.update("Searching database...")
        await asyncio.sleep(0.5)
        stream.update("\n\n## Results\n")
        await asyncio.sleep(0.3)
        stream.update("- Item 1: Important finding\n")
        await asyncio.sleep(0.3)
        stream.update("- Item 2: Another result\n")
        await asyncio.sleep(0.3)
        stream.update("- Item 3: Final item")
        await asyncio.sleep(0.5)

    print()
    success("Multiple messages streamed successfully!")


async def demo_error_handling():
    """Demonstrate error handling during streaming."""
    clear()
    rule("⚠️ Error Handling in Streaming", style="bold red")
    print()

    info("Demonstrating graceful error handling...")
    print()

    try:
        with StreamingMessage(title="⚡ Processing") as stream:
            stream.update("Starting process...")
            await asyncio.sleep(0.5)
            stream.update("\nStep 1: Complete ✓")
            await asyncio.sleep(0.5)
            stream.update("\nStep 2: In progress...")
            await asyncio.sleep(0.5)

            # Simulate an error
            raise ValueError("Simulated error during streaming!")

    except ValueError as e:
        print()
        warning(f"Error handled: {e}")
        print("Note: The streaming message was still finalized properly!")

    print()
    success("Error handling demonstration complete!")


async def demo_theme_adaptation():
    """Demonstrate how streaming adapts to different themes."""
    clear()
    rule("🎨 Theme Adaptation", style="bold magenta")
    print()

    info("Showing how streaming adapts to different themes...")
    print()

    themes = ["default", "minimal", "terminal"]

    for theme_name in themes:
        set_theme(theme_name)
        print(f"\n[bold]Theme: {theme_name}[/bold]")
        print()

        with StreamingMessage(title="🎭 Theme Demo") as stream:
            stream.update(f"This is how streaming looks in **{theme_name}** theme.\n")
            await asyncio.sleep(0.3)
            stream.update("Notice how the styling adapts automatically!")
            await asyncio.sleep(0.5)

        print()

    # Reset to default theme
    set_theme("default")
    success("Theme adaptation demonstration complete!")


async def demo_real_time_updates():
    """Demonstrate real-time data updates in streaming."""
    clear()
    rule("📡 Real-Time Updates", style="bold cyan")
    print()

    info("Simulating real-time data streaming...")
    print()

    with StreamingMessage(title="📈 Live Metrics", show_elapsed=True) as stream:
        for i in range(10):
            # Build metrics string
            metrics = f"""## System Metrics (Update {i+1}/10)

**CPU Usage:** {20 + i*3}%
**Memory:** {40 + i*2}%
**Network:** {10 + i*5} Mbps
**Active Users:** {100 + i*10}

Status: {"🟢 Healthy" if i < 7 else "🟡 Warning"}"""

            # Replace entire content with set_content
            stream.set_content(metrics)
            await asyncio.sleep(0.5)

    print()
    success("Real-time streaming complete!")


async def demo_code_streaming():
    """Demonstrate streaming code generation."""
    clear()
    rule("💻 Code Generation Streaming", style="bold green")
    print()

    info("Simulating code generation with streaming...")
    print()

    with StreamingMessage(title="🔧 Generating Code") as stream:
        # Simulate progressive code generation
        code_parts = [
            "```python\n",
            "def fibonacci(n):\n",
            '    """Generate Fibonacci sequence."""\n',
            "    if n <= 0:\n",
            "        return []\n",
            "    elif n == 1:\n",
            "        return [0]\n",
            "    elif n == 2:\n",
            "        return [0, 1]\n",
            "    \n",
            "    sequence = [0, 1]\n",
            "    for i in range(2, n):\n",
            "        next_num = sequence[-1] + sequence[-2]\n",
            "        sequence.append(next_num)\n",
            "    \n",
            "    return sequence\n",
            "```\n\n",
            "This function generates the first `n` numbers ",
            "in the Fibonacci sequence efficiently!",
        ]

        for part in code_parts:
            stream.update(part)
            await asyncio.sleep(0.2)

    print()
    success("Code generation complete with syntax highlighting!")


async def main():
    """Main demo runner."""
    ui = get_output()

    demos = [
        ("Basic Streaming Message", demo_basic_streaming),
        ("Streaming Assistant", demo_streaming_assistant),
        ("Async Generator Streaming", demo_async_generator_streaming),
        ("Multiple Streams", demo_multiple_streams),
        ("Error Handling", demo_error_handling),
        ("Theme Adaptation", demo_theme_adaptation),
        ("Real-Time Updates", demo_real_time_updates),
        ("Code Generation", demo_code_streaming),
    ]

    while True:
        clear()
        rule("🌊 Streaming Message Demos", style="bold cyan")
        print()

        print("[bold cyan]Choose a demo:[/bold cyan]")
        for i, (name, _) in enumerate(demos, 1):
            print(f"  [{i}] {name}")
        print("  [0] Exit")
        print()

        try:
            choice = input("Enter choice (0-8): ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if choice == "0":
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(demos):
                await demos[idx][1]()
                print()
                input("Press Enter to continue...")
            else:
                warning("Invalid choice. Please try again.")
                await asyncio.sleep(1)
        except ValueError:
            warning("Please enter a number.")
            await asyncio.sleep(1)
        except Exception as e:
            ui.error(f"Error: {e}")
            await asyncio.sleep(2)

    print()
    success("Thank you for exploring streaming messages!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
    sys.exit(0)
