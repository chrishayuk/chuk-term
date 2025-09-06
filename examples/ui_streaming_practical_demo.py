#!/usr/bin/env python3
"""
Practical Streaming Demo

Real-world examples of streaming in action:
- API response streaming
- File processing with progress
- Log streaming
- Chat application simulation
- Database query results

Usage:
    uv run examples/ui_streaming_practical_demo.py
"""

import asyncio
import random
import sys
import time
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn
from rich.table import Table

from chuk_term.ui.output import clear, error, get_output, info, rule, success, warning
from chuk_term.ui.prompts import ask
from chuk_term.ui.streaming import StreamingAssistant, StreamingMessage


class PracticalStreamingDemo:
    """Practical streaming demonstrations."""

    def __init__(self):
        self.ui = get_output()
        self.console = Console()

    async def demo_api_streaming(self):
        """Simulate streaming API responses."""
        clear()
        rule("🌐 API Response Streaming", style="bold blue")
        print()

        info("Simulating OpenAI-style API streaming...")
        print()

        # Simulate user question
        question = "Explain quantum computing in simple terms"
        self.ui.user_message(question)
        print()

        async def stream_api_response() -> AsyncIterator[str]:
            """Simulate streaming from an API."""
            response = """Quantum computing is a revolutionary approach to computation that leverages quantum mechanics principles.

## Key Concepts:

**Qubits vs Bits:**
- Classical computers use bits (0 or 1)
- Quantum computers use qubits (can be 0, 1, or both simultaneously)

**Superposition:**
Think of it like a coin spinning in the air - it's both heads and tails until it lands. Qubits can exist in multiple states at once.

**Entanglement:**
When qubits become connected, measuring one instantly affects the other, regardless of distance. Einstein called this "spooky action at a distance."

**Quantum Advantage:**
For certain problems, quantum computers can:
- Factor large numbers exponentially faster
- Simulate molecular interactions for drug discovery
- Optimize complex logistics problems
- Enhance machine learning algorithms

## Real-World Applications:
1. **Cryptography** - Breaking and creating unbreakable codes
2. **Drug Discovery** - Simulating molecular interactions
3. **Financial Modeling** - Optimizing portfolios and risk analysis
4. **Weather Prediction** - Processing vast amounts of data
5. **Artificial Intelligence** - Enhancing machine learning

The technology is still emerging, but it promises to solve problems that would take classical computers millions of years!"""

            # Simulate token-by-token streaming
            words = response.split()
            for word in words:
                # Simulate variable network latency
                delay = random.uniform(0.01, 0.05)
                await asyncio.sleep(delay)
                yield word + " "

        # Stream the response
        with StreamingMessage(title="🤖 AI Assistant", show_elapsed=True) as stream:
            async for chunk in stream_api_response():
                stream.update(chunk)

        print()
        success("API response streamed successfully!")

        # Show token statistics
        print()
        info("Response Statistics:")
        print("  • Response time: 3.2s")
        print("  • Tokens generated: 287")
        print("  • Tokens/second: 89.7")

    async def demo_file_processing(self):
        """Demonstrate file processing with streaming progress."""
        clear()
        rule("📁 File Processing Stream", style="bold green")
        print()

        info("Processing large dataset with streaming updates...")
        print()

        # Simulate file processing
        total_files = 50
        processed = 0

        with StreamingMessage(title="📊 Processing Files", show_elapsed=True) as stream:
            for i in range(total_files):
                processed = i + 1

                # Update with current status
                status = f"""## File Processing Status

**Progress:** {processed}/{total_files} files ({processed*100//total_files}%)
**Current File:** data_{i+1:03d}.csv
**Records Processed:** {(i+1) * 1234:,}
**Errors:** {0 if i < 45 else i-44}

### Recent Activity:
"""

                # Add recent files
                start = max(0, i - 4)
                for j in range(start, i + 1):
                    status += f"✓ data_{j+1:03d}.csv - Processed successfully\n"

                stream.set_content(status)
                await asyncio.sleep(0.1)

        print()
        success(f"Processed {total_files} files successfully!")

        # Show summary
        print()
        table = Table(title="Processing Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right")

        table.add_row("Total Files", str(total_files))
        table.add_row("Successful", "45")
        table.add_row("Failed", "5")
        table.add_row("Total Records", "61,700")
        table.add_row("Processing Time", "5.2s")
        table.add_row("Average Speed", "9.6 files/sec")

        self.console.print(table)

    async def demo_log_streaming(self):
        """Simulate streaming logs from a service."""
        clear()
        rule("📜 Live Log Streaming", style="bold yellow")
        print()

        info("Streaming logs from application service...")
        print()

        log_levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
        log_messages = [
            "Server started on port 8080",
            "Database connection established",
            "Incoming request from 192.168.1.100",
            "Processing user authentication",
            "Cache miss for key: user_123",
            "Query executed in 45ms",
            "Response sent successfully",
            "Memory usage: 256MB",
            "Active connections: 42",
            "Background job started",
            "Email queued for delivery",
            "Rate limit check passed",
            "Session validated",
            "Data synchronized",
            "Health check completed",
        ]

        with StreamingMessage(title="🔍 Application Logs", show_elapsed=False) as stream:
            logs = ""
            for _i in range(20):
                # Generate random log entry
                timestamp = time.strftime("%H:%M:%S")
                level = random.choice(log_levels)
                message = random.choice(log_messages)

                # Color code by level
                if level == "ERROR":
                    log_line = f"[red][{timestamp}] {level:8} {message}[/red]\n"
                elif level == "WARNING":
                    log_line = f"[yellow][{timestamp}] {level:8} {message}[/yellow]\n"
                elif level == "DEBUG":
                    log_line = f"[dim][{timestamp}] {level:8} {message}[/dim]\n"
                else:
                    log_line = f"[{timestamp}] {level:8} {message}\n"

                logs += log_line

                # Keep only last 10 lines for display
                lines = logs.split("\n")
                if len(lines) > 11:
                    logs = "\n".join(lines[-11:])

                stream.set_content(logs)
                await asyncio.sleep(0.3)

        print()
        success("Log streaming complete!")

    async def demo_chat_application(self):
        """Simulate a chat application with streaming."""
        clear()
        rule("💬 Chat Application", style="bold magenta")
        print()

        info("Interactive chat with streaming responses...")
        print()

        # Get user input
        user_msg = ask("You: ") or "Hello, how are you?"
        print()

        # Display user message
        self.ui.user_message(user_msg)
        print()

        # Generate appropriate response based on input
        if "weather" in user_msg.lower():
            response = """I'd be happy to help with weather information!

## Current Weather
**Location:** San Francisco, CA
**Temperature:** 68°F (20°C)
**Conditions:** Partly cloudy
**Humidity:** 65%
**Wind:** 12 mph West

## Forecast
- **Today:** High 72°F, Low 58°F
- **Tomorrow:** Sunny, High 75°F
- **Weekend:** Chance of rain on Saturday

Stay prepared and have a great day!"""
        elif "help" in user_msg.lower():
            response = """I'm here to help! Here are some things I can assist with:

## Available Commands:
- **Weather** - Get current weather and forecasts
- **News** - Latest headlines and updates
- **Calculate** - Perform mathematical operations
- **Translate** - Translate text between languages
- **Define** - Dictionary definitions and explanations

Just ask me anything and I'll do my best to help!"""
        else:
            response = """Thanks for your message! I'm doing well and ready to assist you.

I'm an AI assistant that can help with a variety of tasks:
- Answer questions
- Provide information
- Help with analysis
- Offer suggestions

What would you like to know or discuss today?"""

        # Stream the response
        assistant = StreamingAssistant()
        assistant.start()

        # Simulate thinking
        for _ in range(3):
            await asyncio.sleep(0.3)

        # Stream response character by character
        for char in response:
            assistant.update(char)
            await asyncio.sleep(0.01)

        assistant.finalize()

        print()
        success("Chat response delivered!")

    async def demo_database_streaming(self):
        """Simulate streaming database query results."""
        clear()
        rule("🗄️ Database Query Streaming", style="bold cyan")
        print()

        info("Executing large database query with streaming results...")
        print()

        # Simulate query execution
        query = """SELECT * FROM users
WHERE created_at > '2024-01-01'
ORDER BY created_at DESC
LIMIT 1000"""

        self.ui.code(query, language="sql", title="Query")
        print()

        async def stream_query_results() -> AsyncIterator[list[dict[str, Any]]]:
            """Simulate streaming query results in batches."""
            batch_size = 10
            total_batches = 10

            for batch_num in range(total_batches):
                # Simulate fetching a batch
                await asyncio.sleep(0.2)

                # Generate batch data
                batch = []
                for i in range(batch_size):
                    record_id = batch_num * batch_size + i + 1
                    batch.append(
                        {
                            "id": record_id,
                            "username": f"user_{record_id:04d}",
                            "email": f"user{record_id}@example.com",
                            "created": f"2024-{(record_id % 12)+1:02d}-{(record_id % 28)+1:02d}",
                        }
                    )

                yield batch

        with StreamingMessage(title="📊 Query Results", show_elapsed=True) as stream:
            all_results = []

            async for batch in stream_query_results():
                all_results.extend(batch)

                # Update streaming display
                content = f"""## Query Progress

**Records Retrieved:** {len(all_results)}
**Last Record ID:** {all_results[-1]['id']}
**Batches Processed:** {len(all_results) // 10}

### Sample Records:
"""
                # Show last 5 records
                for record in all_results[-5:]:
                    content += f"• {record['username']} - {record['email']}\n"

                stream.set_content(content)

        print()
        success(f"Query complete! Retrieved {len(all_results)} records")

        # Show summary table
        print()
        table = Table(title="Query Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right")

        table.add_row("Total Records", "100")
        table.add_row("Execution Time", "2.1s")
        table.add_row("Records/Second", "47.6")
        table.add_row("Memory Used", "1.2 MB")

        self.console.print(table)

    async def demo_multi_stream_dashboard(self):
        """Demonstrate multiple concurrent streams (dashboard)."""
        clear()
        rule("📊 Multi-Stream Dashboard", style="bold green")
        print()

        info("Simulating dashboard with multiple streaming data sources...")
        print()

        # Create multiple streaming displays
        duration = 10
        start_time = time.time()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console,
            transient=True,
        ) as progress:

            # Add tasks
            cpu_task = progress.add_task("[cyan]CPU Usage", total=100)
            mem_task = progress.add_task("[green]Memory", total=100)
            net_task = progress.add_task("[yellow]Network", total=100)
            disk_task = progress.add_task("[magenta]Disk I/O", total=100)

            while time.time() - start_time < duration:
                # Update each metric
                progress.update(cpu_task, completed=random.randint(20, 80))
                progress.update(mem_task, completed=random.randint(40, 70))
                progress.update(net_task, completed=random.randint(10, 90))
                progress.update(disk_task, completed=random.randint(5, 50))

                await asyncio.sleep(0.2)

        print()
        success("Dashboard streaming complete!")

        # Show final summary
        print()
        info("System Summary:")
        print("  • Average CPU: 52%")
        print("  • Average Memory: 58%")
        print("  • Network Traffic: 2.4 GB")
        print("  • Disk Operations: 1,247")

    async def run(self):
        """Run the practical streaming demos."""
        demos = [
            ("API Response Streaming", self.demo_api_streaming),
            ("File Processing Progress", self.demo_file_processing),
            ("Live Log Streaming", self.demo_log_streaming),
            ("Chat Application", self.demo_chat_application),
            ("Database Query Results", self.demo_database_streaming),
            ("Multi-Stream Dashboard", self.demo_multi_stream_dashboard),
        ]

        while True:
            clear()
            rule("🚀 Practical Streaming Examples", style="bold cyan")
            print()

            self.ui.panel(
                """
These demos show real-world streaming use cases:

• **API Responses** - Stream tokens from LLM APIs
• **File Processing** - Show progress while processing files
• **Log Streaming** - Display logs as they're generated
• **Chat Interface** - Interactive chat with streaming
• **Database Queries** - Stream large query results
• **Dashboards** - Multiple concurrent data streams

Each example demonstrates practical patterns you can use!
            """,
                title="Overview",
                style="cyan",
            )

            print()
            print("[bold cyan]Choose a demo:[/bold cyan]")
            for i, (name, _) in enumerate(demos, 1):
                print(f"  [{i}] {name}")
            print("  [0] Exit")
            print()

            try:
                choice = input("Enter choice (0-6): ").strip()
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
                error(f"Demo error: {e}")
                await asyncio.sleep(2)


async def main():
    """Main entry point."""
    try:
        demo = PracticalStreamingDemo()
        await demo.run()

        print()
        success("Thanks for exploring practical streaming examples!")

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        error(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
    sys.exit(0)
