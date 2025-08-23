# Formatters and Data Display

## Overview

ChukTerm's formatters module provides consistent formatting utilities for various content types. These formatters are theme-aware and automatically adapt their output based on the current theme, ensuring content looks great in rich terminals while degrading gracefully for minimal or legacy environments.

## Features

- **Tool Call Formatting**: Display tool/function invocations clearly
- **Error Formatting**: Consistent error display with tracebacks
- **JSON Formatting**: Pretty-print JSON with syntax highlighting
- **Table Creation**: Build and format data tables
- **Tree Structures**: Display hierarchical data
- **Markdown Rendering**: Rich markdown display
- **Timestamp Formatting**: Consistent date/time display
- **File Size Formatting**: Human-readable file sizes
- **Duration Formatting**: Human-readable time durations

## Basic Usage

### Import Formatters

```python
from chuk_term.ui.formatters import (
    format_tool_call,
    format_error,
    format_json,
    format_table,
    format_tree,
    format_markdown,
    format_timestamp,
    format_file_size,
    format_duration
)
```

## Tool Call Formatting

Format tool or function invocations for display:

```python
from chuk_term.ui.formatters import format_tool_call

# Basic tool call
content = format_tool_call(
    tool_name="database_query",
    arguments={"query": "SELECT * FROM users", "limit": 10}
)
ui.print(content)

# With description
content = format_tool_call(
    tool_name="send_email",
    arguments={
        "to": "user@example.com",
        "subject": "Hello",
        "body": "Message content"
    },
    include_description=True,
    description="Send an email message to the specified recipient"
)
ui.print(content)
```

### Output by Theme

**Default/Dark/Light Themes:**
```markdown
**Tool:** `database_query`

**Arguments:**
```json
{
  "query": "SELECT * FROM users",
  "limit": 10
}
```
```

**Minimal/Terminal Themes:**
```
Tool: database_query
  Arguments:
    {
      "query": "SELECT * FROM users",
      "limit": 10
    }
```

## Error Formatting

Format errors and exceptions consistently:

```python
from chuk_term.ui.formatters import format_error

try:
    risky_operation()
except Exception as e:
    # Format with traceback
    error_display = format_error(e, include_traceback=True)
    ui.print(error_display)
    
    # Format without traceback
    simple_error = format_error(e, include_traceback=False)
    ui.error(simple_error)

# Custom error formatting
error_content = format_error(
    ValueError("Invalid input"),
    title="Input Validation Error",
    include_traceback=False,
    suggestions=[
        "Check input format",
        "Ensure values are within range",
        "Review documentation"
    ]
)
```

## JSON Formatting

Pretty-print JSON data with optional syntax highlighting:

```python
from chuk_term.ui.formatters import format_json

data = {
    "name": "ChukTerm",
    "version": "1.0.0",
    "features": ["themes", "prompts", "formatting"],
    "config": {
        "theme": "default",
        "verbose": False
    }
}

# Basic formatting
formatted = format_json(data)
ui.print(formatted)

# With custom indentation
formatted = format_json(data, indent=4)

# Compact format
compact = format_json(data, compact=True)

# With syntax highlighting control
highlighted = format_json(data, syntax_highlight=True)
```

### Output Examples

**Rich Terminal (with highlighting):**
- Syntax colored JSON
- Proper indentation
- Key highlighting

**Minimal Theme:**
- Plain text JSON
- Clean indentation
- No colors

## Table Formatting

Create and format data tables:

```python
from chuk_term.ui.formatters import format_table

# Simple table from list of dicts
data = [
    {"name": "Alice", "age": 30, "role": "Developer"},
    {"name": "Bob", "age": 25, "role": "Designer"},
    {"name": "Charlie", "age": 35, "role": "Manager"}
]

table = format_table(
    data,
    title="Team Members",
    show_header=True,
    show_lines=True
)
ui.print(table)

# Custom columns
table = format_table(
    data,
    columns=["name", "role"],  # Only show these columns
    column_names={"name": "Name", "role": "Position"},  # Custom headers
    title="Staff Directory"
)

# From list of lists
data = [
    ["Product A", 100, "$10.00"],
    ["Product B", 50, "$20.00"],
    ["Product C", 75, "$15.00"]
]

table = format_table(
    data,
    headers=["Product", "Quantity", "Price"],
    title="Inventory",
    show_footer=True,
    footer=["Total", 225, "$45.00"]
)
```

### Table Styles by Theme

**Default/Dark/Light:**
- Rich borders and styling
- Colored headers
- Row separators optional

**Minimal:**
- Plain text alignment
- Simple ASCII borders
- No colors

**Terminal:**
- Basic box drawing characters
- Simple ANSI colors if supported

## Tree Structures

Display hierarchical data as trees:

```python
from chuk_term.ui.formatters import format_tree

# Simple tree from dict
data = {
    "project": {
        "src": {
            "main.py": "file",
            "utils.py": "file",
            "modules": {
                "auth.py": "file",
                "database.py": "file"
            }
        },
        "tests": {
            "test_main.py": "file",
            "test_utils.py": "file"
        },
        "README.md": "file"
    }
}

tree = format_tree(data, title="Project Structure")
ui.print(tree)

# Custom tree with icons
tree = format_tree(
    data,
    title="📁 Project Files",
    show_icons=True,
    expand_all=True
)

# Tree from paths
paths = [
    "src/main.py",
    "src/utils.py",
    "src/modules/auth.py",
    "tests/test_main.py",
    "README.md"
]

tree = format_tree_from_paths(paths, title="File List")
```

## Markdown Formatting

Render markdown content with appropriate styling:

```python
from chuk_term.ui.formatters import format_markdown

markdown_text = """
# Project Setup

## Requirements
- Python 3.10+
- pip or uv

## Installation
1. Clone the repository
2. Run `pip install -e .`
3. Start developing!

**Note:** This is a *development* version.
"""

# Format markdown
formatted = format_markdown(markdown_text)
ui.print(formatted)

# With code blocks
markdown_with_code = """
## Example Code

```python
def hello_world():
    print("Hello from ChukTerm!")
```

Run with: `python main.py`
"""

formatted = format_markdown(markdown_with_code, syntax_highlight=True)
```

## Timestamp Formatting

Format dates and times consistently:

```python
from chuk_term.ui.formatters import format_timestamp
from datetime import datetime

# Current time
now = datetime.now()

# Default format
formatted = format_timestamp(now)
# Output: "2024-01-20 14:30:45"

# Custom format
formatted = format_timestamp(now, format="%B %d, %Y at %I:%M %p")
# Output: "January 20, 2024 at 02:30 PM"

# Relative time
formatted = format_timestamp(now, relative=True)
# Output: "2 minutes ago" or "in 3 hours"

# ISO format
formatted = format_timestamp(now, iso=True)
# Output: "2024-01-20T14:30:45.123456"
```

## File Size Formatting

Convert bytes to human-readable sizes:

```python
from chuk_term.ui.formatters import format_file_size

# Basic usage
size = format_file_size(1024)  # "1.0 KB"
size = format_file_size(1048576)  # "1.0 MB"
size = format_file_size(1073741824)  # "1.0 GB"

# With precision control
size = format_file_size(1536, precision=2)  # "1.50 KB"

# Binary vs decimal
size = format_file_size(1000, binary=False)  # "1.0 KB" (1000 bytes)
size = format_file_size(1024, binary=True)   # "1.0 KiB" (1024 bytes)

# With full words
size = format_file_size(2048, full_words=True)  # "2.0 Kilobytes"
```

## Duration Formatting

Format time durations in human-readable format:

```python
from chuk_term.ui.formatters import format_duration

# Seconds to readable format
duration = format_duration(90)  # "1 minute 30 seconds"
duration = format_duration(3661)  # "1 hour 1 minute"
duration = format_duration(86400)  # "1 day"

# Abbreviated format
duration = format_duration(90, abbreviated=True)  # "1m 30s"

# Precise format
duration = format_duration(90.5, precise=True)  # "1 minute 30.5 seconds"

# From timedelta
from datetime import timedelta
td = timedelta(hours=2, minutes=30)
duration = format_duration(td)  # "2 hours 30 minutes"
```

## Advanced Formatting

### Custom Formatters

Create custom formatters for specific data types:

```python
def format_user_profile(user: dict) -> Table | str:
    """Format user profile data."""
    theme = get_theme()
    
    if theme.is_minimal():
        # Plain text for minimal theme
        lines = [
            f"User: {user['name']}",
            f"Email: {user['email']}",
            f"Role: {user['role']}",
            f"Joined: {user['joined_date']}"
        ]
        return "\n".join(lines)
    
    # Rich table for other themes
    table = Table(title="User Profile", show_header=False)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Name", user['name'])
    table.add_row("Email", user['email'])
    table.add_row("Role", user['role'])
    table.add_row("Joined", user['joined_date'])
    
    return table
```

### Composite Formatting

Combine multiple formatters for complex displays:

```python
def format_api_response(response: dict) -> Panel:
    """Format API response with multiple components."""
    from rich.panel import Panel
    from rich.layout import Layout
    
    # Format status
    status = Text(f"Status: {response['status']}", style="green")
    
    # Format headers as table
    headers_table = format_table(
        response['headers'],
        title="Headers",
        show_lines=False
    )
    
    # Format body as JSON
    body_json = format_json(response['body'])
    
    # Combine in layout
    layout = Layout()
    layout.split_column(
        Layout(status, size=1),
        Layout(headers_table, size=5),
        Layout(body_json)
    )
    
    return Panel(layout, title="API Response")
```

## Theme Adaptation

All formatters automatically adapt to the current theme:

```python
from chuk_term.ui.theme import set_theme

data = {"key": "value", "number": 42}

# Rich formatting with colors
set_theme("default")
formatted = format_json(data)  # Colored, syntax highlighted

# Plain text formatting
set_theme("minimal")
formatted = format_json(data)  # Plain text, no colors

# Basic ANSI formatting
set_theme("terminal")
formatted = format_json(data)  # Basic colors if supported
```

## Performance Considerations

### Large Data Sets

```python
# For large tables, use pagination
def format_large_table(data: list, page_size: int = 20):
    """Format large table with pagination."""
    for i in range(0, len(data), page_size):
        page = data[i:i + page_size]
        table = format_table(
            page,
            title=f"Results (Page {i//page_size + 1})"
        )
        ui.print(table)
        if i + page_size < len(data):
            if not confirm("Show next page?"):
                break
```

### Caching Formatted Output

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def format_cached_json(json_str: str) -> str:
    """Cache formatted JSON for repeated display."""
    data = json.loads(json_str)
    return format_json(data)
```

## Testing Formatters

```python
import pytest
from chuk_term.ui.formatters import format_json, format_table

def test_json_formatting():
    """Test JSON formatter with different inputs."""
    # Test with dict
    data = {"key": "value"}
    result = format_json(data)
    assert "key" in str(result)
    assert "value" in str(result)
    
    # Test with list
    data = [1, 2, 3]
    result = format_json(data)
    assert "1" in str(result)

def test_table_formatting():
    """Test table formatter."""
    data = [{"a": 1, "b": 2}]
    table = format_table(data)
    # Verify table structure based on theme
```

## Best Practices

### 1. Use Appropriate Formatters

```python
# ✅ GOOD - Use specific formatters
ui.print(format_json(data))  # For JSON
ui.print(format_table(rows))  # For tabular data
ui.print(format_error(e))  # For errors

# ❌ BAD - Generic string conversion
ui.print(str(data))  # No formatting
ui.print(json.dumps(data))  # No syntax highlighting
```

### 2. Handle Theme Differences

```python
# ✅ GOOD - Let formatters handle themes
formatted = format_json(data)
ui.print(formatted)  # Automatically theme-aware

# ❌ BAD - Manual theme checking
if theme == "minimal":
    print(json.dumps(data))
else:
    print(Syntax(json.dumps(data), "json"))
```

### 3. Provide Context

```python
# ✅ GOOD - Include titles and descriptions
table = format_table(data, title="Search Results")
json_out = format_json(config, title="Current Configuration")

# ❌ BAD - No context
table = format_table(data)
json_out = format_json(config)
```

## Module Reference

### Core Functions

| Function | Description | Returns |
|----------|-------------|---------|
| `format_tool_call()` | Format tool/function calls | `Markdown` or `str` |
| `format_error()` | Format exceptions with traceback | `Panel` or `str` |
| `format_json()` | Pretty-print JSON data | `Syntax` or `str` |
| `format_table()` | Create formatted tables | `Table` or `str` |
| `format_tree()` | Create tree structures | `Tree` or `str` |
| `format_markdown()` | Render markdown content | `Markdown` or `str` |
| `format_timestamp()` | Format dates/times | `str` |
| `format_file_size()` | Human-readable file sizes | `str` |
| `format_duration()` | Human-readable durations | `str` |

### Parameters

Most formatters accept these common parameters:

- `title`: Optional title for the formatted output
- `style`: Color/style for rich terminals
- `theme_override`: Override current theme for this format

## Related Documentation

- [Output System](./output.md) - Where formatted content is displayed
- [Theme System](./themes.md) - How formatters adapt to themes
- [Code Display](./code.md) - Specialized code formatting
- [Tables and Trees](./terminal.md) - Terminal capabilities for formatting