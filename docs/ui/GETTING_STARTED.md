# Getting Started with ChukTerm UI

A quick guide for AI agents and developers to start using ChukTerm's terminal UI components.

## Installation

### Option 1: Using uv (Recommended)
[uv](https://github.com/astral-sh/uv) is a fast Python package manager that's recommended for development:

```bash
# Install as a dependency
uv add chuk-term

# Or install globally
uv tool install chuk-term
```

### Option 2: Using pip
Traditional installation with pip:

```bash
# Install from PyPI
pip install chuk-term

# Or install with specific extras
pip install chuk-term[dev]  # Include development dependencies
```

### Option 3: From Source (Development)
Clone and install for development:

```bash
# Clone the repository
git clone https://github.com/yourusername/chuk-term.git
cd chuk-term

# Install with uv (recommended for development)
uv sync --dev  # Installs all dependencies including dev

# Or install with pip
pip install -e ".[dev]"  # Editable install with dev dependencies

# Verify installation
chuk-term --version
```

### Verify Installation
After installation, verify everything is working:

```bash
# Check CLI is available
chuk-term --version

# Run the demo
chuk-term demo

# Test the installation
chuk-term test
```

### System Requirements
- **Python**: 3.10 or higher
- **OS**: Windows, macOS, Linux
- **Terminal**: Any terminal with ANSI color support (most modern terminals)

### Optional Dependencies
For development and testing:

```bash
# Using uv (automatically installed with --dev)
uv add --dev pytest pytest-cov ruff black mypy

# Using pip
pip install pytest pytest-cov ruff black mypy
```

## Quick Start

```python
from chuk_term.ui import output

# Basic output messages
output.info("Processing your request...")
output.success("✓ Task completed successfully")
output.warning("⚠ Check this important note")
output.error("✗ Something went wrong")

# Interactive prompts
from chuk_term.ui import ask, confirm, select_from_list

name = ask("What's your name?")
if confirm("Ready to continue?"):
    choice = select_from_list(["Option A", "Option B", "Option C"], "Choose one:")
    output.info(f"You selected: {choice}")
```

## Core Concepts

### 1. The Output System (Singleton)
The output system is your main interface for terminal output. It's a singleton that automatically adapts to the current theme.

```python
from chuk_term.ui import output

# Different message levels
output.debug("Debug info")      # Only shown in verbose mode
output.info("Information")      # Standard info message
output.success("Success!")      # Success confirmation
output.warning("Warning!")      # Important warning
output.error("Error!")          # Error message
output.fatal("Fatal error!")    # Fatal error (goes to stderr)

# Special formatting
output.tip("💡 Pro tip: Use themes for better output")
output.hint("Try using --verbose for more details")
output.command("git status")    # Suggest a command
output.status("Processing...")  # Status update
```

### 2. Themes
ChukTerm includes 8 built-in themes that automatically adapt output:

```python
from chuk_term.ui import set_theme, get_theme

# Available themes
themes = ["default", "dark", "light", "minimal", "terminal", 
          "monokai", "dracula", "solarized"]

# Change theme
set_theme("minimal")  # Plain text, no colors or emojis
set_theme("terminal") # Basic ANSI colors only
set_theme("default")  # Full Rich formatting with colors and emojis

# Check current theme
current = get_theme()
print(f"Current theme: {current.name}")
```

### 3. User Interaction
Interactive prompts for user input:

```python
from chuk_term.ui import ask, confirm, ask_number, select_from_list, select_multiple

# Text input
name = ask("Enter your name:", default="Anonymous")
password = ask("Enter password:", password=True)

# Confirmation
if confirm("Delete file?", default=False):
    output.info("File deleted")

# Number input
age = ask_number("Enter your age:", min_value=0, max_value=120)

# Single selection
option = select_from_list(
    ["Python", "JavaScript", "Go", "Rust"],
    "Choose your language:",
    default="Python"
)

# Multiple selection
selected = select_multiple(
    ["Feature A", "Feature B", "Feature C"],
    "Select features to enable:",
    min_selections=1
)
```

## Common Patterns for AI Agents

### Pattern 1: Task Execution with Feedback
```python
from chuk_term.ui import output, progress

# Show what you're doing
output.info("🔍 Analyzing codebase...")

# Use progress for longer operations
with output.progress("Processing files..."):
    # Your processing code here
    process_files()

output.success("✓ Analysis complete!")

# Show results
output.print_table(results_table)
```

### Pattern 2: Error Handling with User Feedback
```python
from chuk_term.ui import output, confirm

try:
    # Attempt operation
    output.info("Attempting to connect to API...")
    connect_to_api()
    output.success("✓ Connected successfully")
    
except ConnectionError as e:
    output.error(f"✗ Connection failed: {e}")
    
    if confirm("Would you like to retry?"):
        # Retry logic
        pass
    else:
        output.info("Operation cancelled")
```

### Pattern 3: Displaying Code and Diffs
```python
from chuk_term.ui import display_code, display_diff

# Show code with syntax highlighting
code = """
def hello_world():
    print("Hello, World!")
"""
display_code(code, language="python", title="example.py")

# Show a diff
original = "Hello World"
modified = "Hello ChukTerm!"
display_diff(original, modified, title="Changes")
```

### Pattern 4: Streaming Messages for Real-Time Updates
```python
from chuk_term.ui.streaming import StreamingMessage, StreamingAssistant
import asyncio

# Basic streaming message
with StreamingMessage(title="🤖 Processing") as stream:
    stream.update("Analyzing data")
    # Simulate processing
    stream.update("...")
    stream.update(" Complete!")

# Using StreamingAssistant for LLM-style responses
async def stream_response():
    assistant = StreamingAssistant()
    stream = assistant.start()
    
    # Simulate token streaming
    response = "I'll help you understand streaming in ChukTerm."
    for word in response.split():
        assistant.update(word + " ")
        await asyncio.sleep(0.1)
    
    assistant.finalize()

# Run async example
asyncio.run(stream_response())
```

### Pattern 5: Structured Data Display
```python
from chuk_term.ui import output

# Tables
data = [
    {"name": "Alice", "age": 30, "role": "Developer"},
    {"name": "Bob", "age": 25, "role": "Designer"}
]
output.print_table(data, title="Team Members")

# JSON data
config = {"theme": "default", "verbose": True}
output.json(config, title="Configuration")

# Tree structure
tree_data = {
    "project": {
        "src": ["main.py", "utils.py"],
        "tests": ["test_main.py"],
        "docs": ["README.md"]
    }
}
output.tree(tree_data, title="Project Structure")

# Key-value pairs
output.kvpairs({
    "Status": "Active",
    "Version": "1.0.0",
    "Author": "AI Agent"
})
```

### Pattern 5: Working with Themes
```python
from chuk_term.ui import output, set_theme

# Adapt to user environment
def setup_output(no_color=False, simple=False):
    if no_color or simple:
        set_theme("minimal")  # Plain text
    elif not sys.stdout.isatty():
        set_theme("minimal")  # Not a terminal
    else:
        set_theme("default")  # Full features

# Check theme capabilities
from chuk_term.ui import get_theme

theme = get_theme()
if theme.is_minimal():
    # Use simple output
    output.print("Processing...")
else:
    # Use rich output
    output.info("🚀 Processing with style...")
```

## Best Practices for AI Agents

### 1. Always Provide Feedback
```python
# Good - User knows what's happening
output.info("Searching for Python files...")
files = find_python_files()
output.success(f"Found {len(files)} Python files")

# Bad - Silent operation
files = find_python_files()  # User doesn't know what's happening
```

### 2. Use Appropriate Message Levels
```python
# Use the right level for the message
output.debug("Detailed trace info")      # Development/debugging
output.info("Starting process...")        # General information
output.success("✓ Task completed")        # Successful completion
output.warning("⚠ Deprecated feature")    # Important warnings
output.error("✗ Failed to connect")       # Recoverable errors
output.fatal("💀 Critical failure")        # Unrecoverable errors
```

### 3. Handle Non-TTY Environments
```python
import sys
from chuk_term.ui import set_theme, output

# Automatically adapt to environment
if not sys.stdout.isatty():
    # Running in pipe, CI, or non-interactive environment
    set_theme("minimal")
    
output.info("This adapts to any environment")
```

### 4. Group Related Output
```python
from chuk_term.ui import output

# Use rules to separate sections
output.rule("Configuration")
output.kvpairs(config_dict)

output.rule("Results")
output.print_table(results)

output.rule("Next Steps")
output.info("1. Review the results")
output.info("2. Make necessary adjustments")
output.info("3. Run the process again")
```

### 5. Progressive Disclosure
```python
from chuk_term.ui import output, confirm

# Start with summary
output.success("✓ Found 42 issues")

# Ask before showing details
if confirm("Show detailed results?"):
    output.print_table(detailed_results)
else:
    output.info("Run with --verbose to see details anytime")
```

## Advanced Features

### Custom Progress Indicators
```python
from chuk_term.ui import output

# Simple progress context
with output.progress("Installing dependencies..."):
    install_dependencies()

# Loading indicator for unknown duration
with output.loading("Waiting for response..."):
    response = wait_for_api()
```

### Markdown Rendering
```python
from chuk_term.ui import output

markdown_text = """
# Results Summary

## Key Findings
- **Performance**: Improved by 40%
- **Memory Usage**: Reduced by 20%
- **Test Coverage**: Increased to 95%

## Recommendations
1. Continue monitoring performance
2. Add more integration tests
3. Update documentation
"""

output.markdown(markdown_text)
```

### Terminal Management
```python
from chuk_term.ui import clear_screen, set_terminal_title, bell

# Clear the screen
clear_screen()

# Set terminal title (useful for long-running tasks)
set_terminal_title("ChukTerm - Processing...")

# Alert user when done
bell()  # Terminal bell sound
output.success("✓ Task completed!")
```

### Working with Code
```python
from chuk_term.ui import display_code, display_code_review, format_code_snippet

# Display code with line numbers
display_code(code_string, language="python", line_numbers=True)

# Code review with issues
issues = [
    {"line": 5, "type": "error", "message": "Undefined variable"},
    {"line": 10, "type": "warning", "message": "Unused import"}
]
display_code_review(code_string, issues, title="Code Review")

# Inline code snippets
output.info(f"Run {format_code_snippet('pip install chuk-term')} to install")
```

## Environment Variables

ChukTerm respects standard environment variables:

- `NO_COLOR` - Disable colors (sets minimal theme)
- `FORCE_COLOR` - Force color output even in non-TTY
- `TERM` - Terminal type detection
- `CI` - Detected as CI environment (uses minimal theme)

## Error Recovery

```python
from chuk_term.ui import output, confirm, ask

def safe_operation():
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            output.info(f"Attempt {attempt + 1}/{max_retries}")
            perform_operation()
            output.success("✓ Operation successful")
            return True
            
        except Exception as e:
            output.error(f"✗ Attempt failed: {e}")
            
            if attempt < max_retries - 1:
                if not confirm("Retry?", default=True):
                    break
            else:
                output.fatal("Maximum retries exceeded")
                
    return False
```

## Complete Example: AI Agent Task

```python
#!/usr/bin/env python3
"""Example: AI agent performing a code analysis task."""

from chuk_term.ui import (
    output, set_theme, ask, confirm, 
    select_from_list, display_code
)
import sys

def main():
    # Setup based on environment
    if not sys.stdout.isatty():
        set_theme("minimal")
    
    # Greet user
    output.rule("🤖 AI Code Analyzer")
    output.info("Welcome to the AI-powered code analysis tool")
    
    # Get user input
    language = select_from_list(
        ["Python", "JavaScript", "Go", "Auto-detect"],
        "Select programming language:",
        default="Auto-detect"
    )
    
    # Show progress
    output.info("🔍 Analyzing codebase...")
    with output.progress("Scanning files..."):
        files = scan_files(language)
    
    output.success(f"✓ Found {len(files)} files to analyze")
    
    # Analyze with feedback
    issues = []
    with output.progress("Analyzing code quality..."):
        for file in files:
            file_issues = analyze_file(file)
            issues.extend(file_issues)
    
    # Present results
    output.rule("📊 Analysis Results")
    
    if issues:
        output.warning(f"Found {len(issues)} issues")
        
        # Summary table
        summary = summarize_issues(issues)
        output.print_table(summary, title="Issues by Type")
        
        # Ask for details
        if confirm("Show detailed issues?"):
            for issue in issues[:10]:  # First 10
                output.rule()
                display_code(
                    issue['code'],
                    language=language.lower(),
                    title=f"{issue['file']}:{issue['line']}"
                )
                output.error(f"Issue: {issue['message']}")
                
            if len(issues) > 10:
                output.info(f"... and {len(issues) - 10} more issues")
    else:
        output.success("✓ No issues found! Your code looks great! 🎉")
    
    # Suggest next steps
    output.rule("💡 Next Steps")
    output.tip("Run with --fix to automatically fix issues")
    output.tip("Use --verbose for more detailed analysis")
    
    # Clean exit
    output.info("Analysis complete. Have a great day! 👋")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        output.warning("\n⚠ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        output.fatal(f"Unexpected error: {e}")
        sys.exit(1)
```

## Related Documentation

- **[Themes Guide](./themes.md)** - Detailed theme system documentation
- **[Output System](./output.md)** - Complete output API reference  
- **[Terminal Management](./terminal.md)** - Terminal control features
- **[Testing Guide](../testing/UNIT_TESTING.md)** - Testing UI components
- **[API Reference](../../README.md)** - Complete API documentation

## Quick Reference Card

```python
# Import everything you need
from chuk_term.ui import (
    # Output
    output, get_output,
    
    # Themes
    set_theme, get_theme,
    
    # Prompts
    ask, confirm, ask_number,
    select_from_list, select_multiple,
    
    # Code display
    display_code, display_diff,
    display_code_review,
    
    # Terminal
    clear_screen, bell,
    set_terminal_title,
    
    # Formatters
    format_timestamp, format_code_snippet
)

# Message levels
output.debug()    # Verbose only
output.info()     # Information
output.success()  # Success
output.warning()  # Warning  
output.error()    # Error
output.fatal()    # Fatal error

# Data display
output.print_table()  # Tables
output.json()         # JSON
output.tree()         # Tree structure
output.kvpairs()      # Key-value pairs
output.markdown()     # Markdown

# Themes
"default"   # Full features
"minimal"   # Plain text
"terminal"  # Basic colors
"dark"      # Dark mode
"light"     # Light mode
"monokai"   # Monokai colors
"dracula"   # Dracula theme
"solarized" # Solarized
```

## Tips for AI Agents

1. **Start Simple**: Use `output.info()` and `output.success()` for basic feedback
2. **Be Informative**: Always tell users what you're doing
3. **Handle Errors Gracefully**: Use try/except with clear error messages
4. **Respect User Preferences**: Check for NO_COLOR, CI environments
5. **Progressive Enhancement**: Start with minimal, add rich features when available
6. **Test All Themes**: Ensure your output works with all 8 themes
7. **Use Semantic Levels**: Choose the right message level (info, warning, error)
8. **Group Related Output**: Use rules and sections for clarity
9. **Provide Context**: Show progress for long operations
10. **Be Concise**: Don't overwhelm users with too much output
11. **Follow Code Quality Standards**: Check [Code Quality Guide](../testing/CODE_QUALITY.md) for linting and formatting

---

*Happy coding! If you have questions, check the detailed documentation linked above or explore the [examples directory](../../examples/).*