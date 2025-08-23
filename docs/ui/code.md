# Code Display and Syntax Highlighting

## Overview

ChukTerm's code module provides advanced code display capabilities with syntax highlighting, diffs, code reviews, and side-by-side comparisons. All features are theme-aware and automatically adapt from rich highlighting in modern terminals to plain text in minimal environments.

## Features

- **Syntax Highlighting**: 100+ language support via Pygments
- **Diff Display**: Show code changes with additions/deletions
- **Code Review**: Display code with inline comments
- **Side-by-Side Comparison**: Compare two code versions
- **Line Numbers**: Optional line number display
- **Code Folding**: Collapse/expand code sections
- **Theme Integration**: Adapts to current UI theme
- **Copy Support**: Easy code copying in supported terminals

## Basic Usage

### Display Code with Syntax Highlighting

```python
from chuk_term.ui import display_code

# Basic code display
code = '''def hello_world():
    """A simple greeting function."""
    print("Hello from ChukTerm!")
    return True'''

display_code(code, language="python")

# With title and line numbers
display_code(
    code,
    language="python",
    title="Example Function",
    line_numbers=True,
    start_line=1
)

# With specific theme
display_code(
    code,
    language="python",
    code_theme="monokai"  # Syntax theme, not UI theme
)
```

### Supported Languages

Common languages with full syntax support:
- Python, JavaScript, TypeScript, Java, C/C++, C#
- Go, Rust, Swift, Kotlin, Scala
- HTML, CSS, SCSS, JSON, XML, YAML
- SQL, Shell/Bash, PowerShell
- Markdown, reStructuredText
- 100+ more via Pygments

## Diff Display

Show code changes with visual diff:

```python
from chuk_term.ui import display_diff

old_code = '''def greet(name):
    print(f"Hello {name}")
    return'''

new_code = '''def greet(name, title=""):
    greeting = f"Hello {title} {name}".strip()
    print(greeting)
    return greeting'''

# Display diff
display_diff(
    old_text=old_code,
    new_text=new_code,
    title="Function Enhancement",
    language="python",
    context_lines=3
)
```

### Diff Formats

```python
# Unified diff format (default)
display_diff(old, new, format="unified")

# Side-by-side diff
display_diff(old, new, format="side_by_side")

# Inline diff with changes highlighted
display_diff(old, new, format="inline")

# GitHub-style diff
display_diff(old, new, format="github")
```

## Code Review Display

Show code with review comments:

```python
from chuk_term.ui import display_code_review

code = '''def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total'''

reviews = [
    {
        "line": 2,
        "comment": "Consider using sum() with generator expression",
        "severity": "suggestion"
    },
    {
        "line": 4,
        "comment": "Add validation for negative quantities",
        "severity": "warning"
    }
]

display_code_review(
    code=code,
    reviews=reviews,
    language="python",
    title="Code Review: calculate_total()"
)
```

### Review Severity Levels

- `"suggestion"`: Improvement suggestions (blue)
- `"warning"`: Potential issues (yellow)
- `"error"`: Must fix issues (red)
- `"info"`: Informational notes (cyan)

## Side-by-Side Comparison

Compare two code versions:

```python
from chuk_term.ui import display_code_comparison

version1 = '''function process(data) {
    console.log(data);
    return data;
}'''

version2 = '''function process(data) {
    if (!data) {
        throw new Error("Data required");
    }
    console.log("Processing:", data);
    return processData(data);
}'''

display_code_comparison(
    left_code=version1,
    right_code=version2,
    left_title="Original",
    right_title="Updated",
    language="javascript",
    highlight_changes=True
)
```

## Advanced Features

### Code Folding

Display code with collapsible sections:

```python
from chuk_term.ui import display_foldable_code

code = '''class UserManager:
    """Manages user operations."""
    
    def __init__(self):
        # ... initialization code ...
        pass
    
    def create_user(self, username, email):
        # ... user creation logic ...
        pass
    
    def delete_user(self, user_id):
        # ... user deletion logic ...
        pass'''

display_foldable_code(
    code,
    language="python",
    collapsed_sections=["__init__", "delete_user"],
    title="UserManager Class"
)
```

### Code Snippets with Context

Show code snippets with surrounding context:

```python
from chuk_term.ui import display_code_snippet

# Show specific lines with context
display_code_snippet(
    file_path="src/main.py",
    start_line=45,
    end_line=52,
    context_lines=3,  # Show 3 lines before/after
    highlight_lines=[47, 48],  # Highlight specific lines
    title="Error Location"
)
```

### Multi-File Display

Display multiple related files:

```python
from chuk_term.ui import display_code_files

files = [
    {
        "path": "src/models/user.py",
        "language": "python",
        "highlights": [15, 16, 20]
    },
    {
        "path": "src/controllers/auth.py",
        "language": "python",
        "highlights": [30, 31]
    }
]

display_code_files(
    files,
    title="Related Changes",
    collapsed=False
)
```

## Theme Adaptation

Code display adapts to the current UI theme:

### Default/Dark/Light Themes
- Full syntax highlighting with colors
- Box borders and decorations
- Line numbers with styling
- Rich diff visualization

### Minimal Theme
- Plain text code blocks
- Simple line prefixes for diffs
- No colors or decorations
- ASCII characters only

### Terminal Theme
- Basic ANSI colors if available
- Simple box drawing characters
- Reduced decoration
- Compatible with legacy terminals

```python
from chuk_term.ui.theme import set_theme

code = "print('Hello World')"

# Rich display
set_theme("default")
display_code(code, "python")  # Full syntax highlighting

# Plain display
set_theme("minimal")
display_code(code, "python")  # Plain text: print('Hello World')
```

## Syntax Themes

Independent of UI themes, you can choose syntax highlighting themes:

```python
# Popular syntax themes
display_code(code, language="python", code_theme="monokai")
display_code(code, language="python", code_theme="dracula")
display_code(code, language="python", code_theme="solarized-dark")
display_code(code, language="python", code_theme="github")
display_code(code, language="python", code_theme="vs")
```

Available syntax themes:
- `monokai` - Popular dark theme
- `dracula` - Gothic dark theme
- `solarized-dark` / `solarized-light` - Low contrast
- `github` - GitHub style
- `vs` - Visual Studio style
- `material` - Material design
- `nord` - Nord color scheme
- Many more via Pygments

## Code Export

Export code displays to various formats:

```python
from chuk_term.ui import export_code

# Export to HTML
html = export_code(
    code,
    language="python",
    format="html",
    include_styles=True
)

# Export to RTF (for word processors)
rtf = export_code(
    code,
    language="python",
    format="rtf"
)

# Export to LaTeX
latex = export_code(
    code,
    language="python",
    format="latex"
)

# Export to image (requires Pillow)
export_code(
    code,
    language="python",
    format="png",
    output_path="code.png"
)
```

## Interactive Features

### Code Selection

Enable code selection in supported terminals:

```python
display_code(
    code,
    language="python",
    selectable=True,  # Allow text selection
    copy_button=True   # Show copy button if supported
)
```

### Code Execution

Display code with execution results:

```python
from chuk_term.ui import display_code_with_output

code = '''
numbers = [1, 2, 3, 4, 5]
squared = [n**2 for n in numbers]
print(f"Original: {numbers}")
print(f"Squared: {squared}")
'''

output = '''Original: [1, 2, 3, 4, 5]
Squared: [1, 4, 9, 16, 25]'''

display_code_with_output(
    code=code,
    output=output,
    language="python",
    title="List Comprehension Example"
)
```

## Performance Optimization

### Large Files

Handle large code files efficiently:

```python
from chuk_term.ui import display_large_code

# Stream large files
display_large_code(
    file_path="large_file.py",
    chunk_size=100,  # Lines per chunk
    interactive=True  # Allow navigation
)

# With search
display_large_code(
    file_path="large_file.py",
    search_term="def ",
    highlight_matches=True
)
```

### Caching

Cache highlighted code for repeated display:

```python
from functools import lru_cache
from chuk_term.ui import get_highlighted_code

@lru_cache(maxsize=50)
def get_cached_highlight(code: str, language: str) -> str:
    """Cache syntax highlighting results."""
    return get_highlighted_code(code, language)
```

## Examples

### Complete Code Review Interface

```python
def code_review_interface(file_path: str, reviews: list):
    """Display an interactive code review interface."""
    from chuk_term.ui import display_code_review, ask, select_from_list
    
    # Load code
    with open(file_path) as f:
        code = f.read()
    
    # Display with reviews
    display_code_review(
        code=code,
        reviews=reviews,
        language="python",
        title=f"Review: {file_path}"
    )
    
    # Interactive review options
    action = select_from_list(
        ["Add Comment", "Mark Resolved", "Next File", "Exit"],
        "Review Action:"
    )
    
    if action == "Add Comment":
        line = ask_number("Line number:")
        comment = ask("Comment:")
        severity = select_from_list(
            ["suggestion", "warning", "error"],
            "Severity:"
        )
        add_review_comment(line, comment, severity)
```

### Diff Viewer

```python
def diff_viewer(file1: str, file2: str):
    """Compare two files with interactive diff viewing."""
    with open(file1) as f:
        content1 = f.read()
    with open(file2) as f:
        content2 = f.read()
    
    # Show different diff formats
    formats = ["unified", "side_by_side", "inline", "github"]
    
    for fmt in formats:
        ui.clear()
        ui.rule(f"Diff Format: {fmt}")
        
        display_diff(
            old_text=content1,
            new_text=content2,
            format=fmt,
            title=f"{file1} → {file2}"
        )
        
        if not confirm("Try next format?"):
            break
```

## Testing

```python
import pytest
from chuk_term.ui.code import display_code, display_diff

def test_code_display():
    """Test basic code display."""
    code = "print('test')"
    # Should not raise
    display_code(code, language="python")

def test_diff_display():
    """Test diff display."""
    old = "line1\nline2"
    new = "line1\nline2\nline3"
    # Should show addition
    display_diff(old, new)

def test_theme_adaptation():
    """Test code adapts to themes."""
    from chuk_term.ui.theme import set_theme
    
    code = "test code"
    for theme in ["default", "minimal", "terminal"]:
        set_theme(theme)
        display_code(code, "python")
        # Verify output differs by theme
```

## Best Practices

### 1. Specify Language

```python
# ✅ GOOD - Specify language for highlighting
display_code(code, language="python")

# ❌ BAD - No language specified
display_code(code)  # No syntax highlighting
```

### 2. Use Appropriate Display Method

```python
# ✅ GOOD - Use specific methods
display_diff(old, new)  # For diffs
display_code_review(code, reviews)  # For reviews

# ❌ BAD - Generic display
print(code)  # No formatting
```

### 3. Handle File Reading Errors

```python
# ✅ GOOD - Handle errors
try:
    with open(file_path) as f:
        code = f.read()
    display_code(code, language="python")
except FileNotFoundError:
    ui.error(f"File not found: {file_path}")
```

## Module Reference

### Core Functions

| Function | Description |
|----------|-------------|
| `display_code()` | Display code with syntax highlighting |
| `display_diff()` | Show code differences |
| `display_code_review()` | Display code with review comments |
| `display_code_comparison()` | Side-by-side code comparison |
| `display_code_snippet()` | Show code excerpt with context |
| `display_foldable_code()` | Code with collapsible sections |
| `display_code_with_output()` | Code with execution results |
| `export_code()` | Export code to various formats |

## Related Documentation

- [Output System](./output.md) - Where code is displayed
- [Theme System](./themes.md) - How code display adapts to themes
- [Formatters](./formatters.md) - General formatting utilities
- [Terminal Management](./terminal.md) - Terminal capabilities for code display