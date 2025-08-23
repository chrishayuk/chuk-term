# UI Theme Management

## Overview

ChukTerm features a comprehensive theme system that controls the visual appearance of all UI components. The theme system is designed to be **internally managed** - application code doesn't need to be theme-aware, as all theme handling happens automatically within the UI components.

## Available Themes

ChukTerm includes eight built-in themes:

### 1. **Default Theme**
- **Colors**: Standard terminal colors with cyan/blue/magenta accents
- **Icons**: Full emoji and symbol support (💬, 🤖, 🔧, ✓, ✗)
- **Decorations**: Rich boxes, panels, and formatting
- **Use Case**: Modern terminals with full Unicode support

### 2. **Dark Theme**
- **Colors**: Bright variants optimized for dark backgrounds
- **Icons**: Full emoji and symbol support
- **Decorations**: Enhanced contrast for dark terminals
- **Use Case**: Dark terminal backgrounds

### 3. **Light Theme**
- **Colors**: Dark variants optimized for light backgrounds
- **Icons**: Full emoji and symbol support
- **Decorations**: Adjusted contrast for light terminals
- **Use Case**: Light terminal backgrounds

### 4. **Minimal Theme**
- **Colors**: No colors - plain white text only
- **Icons**: No emojis - basic ASCII characters (-, >, [x])
- **Decorations**: No boxes or panels - plain text output
- **Use Case**: Compatibility mode, screen readers, or logging

### 5. **Terminal Theme**
- **Colors**: Basic ANSI colors only (8-color palette)
- **Icons**: No emojis - basic ASCII characters
- **Decorations**: Simple boxes using ASCII characters
- **Use Case**: Legacy terminals or SSH sessions

### 6. **Monokai Theme**
- **Colors**: Popular dark theme with purple/green/yellow palette
- **Icons**: Full emoji and symbol support
- **Decorations**: Rich formatting with Monokai color scheme
- **Use Case**: Developers familiar with Monokai from editors

### 7. **Dracula Theme**
- **Colors**: Gothic dark theme with pink/purple/cyan palette
- **Icons**: Full emoji and symbol support
- **Decorations**: Rich formatting with Dracula color scheme
- **Use Case**: Dark theme enthusiasts, night-time coding

### 8. **Solarized Theme**
- **Colors**: Low contrast palette designed for long viewing sessions
- **Icons**: Full emoji and symbol support
- **Decorations**: Rich formatting with Solarized colors
- **Use Case**: Reduced eye strain, professional environments

## Theme Architecture

### Core Components

#### `Theme` Class (`src/chuk_term/ui/theme.py`)
The main theme class that combines colors, icons, and styles:

```python
from chuk_term.ui.theme import Theme, set_theme, get_theme

# Set a theme globally
set_theme("minimal")

# Get the current theme
theme = get_theme()

# Access theme properties
print(theme.name)           # "minimal"
print(theme.colors.success) # Color for success messages
print(theme.icons.check)    # Icon for checkmarks
```

#### `ColorScheme` Class
Defines color mappings for different UI elements:

```python
@dataclass
class ColorScheme:
    # Status colors
    success: str = "green"
    error: str = "red"
    warning: str = "yellow"
    info: str = "cyan"
    
    # Text styles
    normal: str = "white"
    emphasis: str = "bold"
    
    # UI element colors
    primary: str = "cyan"
    secondary: str = "blue"
    accent: str = "magenta"
    
    # Semantic colors
    user: str = "yellow"
    assistant: str = "blue"
    tool: str = "magenta"
```

#### `Icons` Class
Defines icons and symbols used in the UI:

```python
@dataclass
class Icons:
    # Status icons
    success: str = "✓"
    error: str = "✗"
    warning: str = "⚠"
    
    # Mode indicators
    chat: str = "💬"
    interactive: str = "⚡"
    
    # Special
    robot: str = "🤖"
    user: str = "👤"
    tool: str = "🔧"
```

## Using Themes

### Setting a Theme

Themes can be set programmatically or through command-line options:

```python
# In Python code
from chuk_term.ui.theme import set_theme

# Set theme at application start
set_theme("dark")

# Change theme during runtime
set_theme("minimal")
```

```bash
# Via CLI
chuk-term test --theme monokai

# Via environment variable
export CHUK_TERM_THEME=minimal
python my_app.py
```

### Theme-Agnostic Code

The key principle is that **application code should not check themes**. UI components handle theme differences internally:

#### ✅ Good - Theme-Agnostic Code
```python
from chuk_term.ui import output, display_code, display_diff

# Just use the components - they handle themes internally
output.success("Operation completed!")
display_code(my_code, "python", title="Example")
display_diff(old_code, new_code, title="Changes")
```

#### ❌ Bad - Theme-Aware Code
```python
# Don't do this!
theme = get_theme()
if theme.name == "minimal":
    print(f"Code: {code}")
else:
    console.print(Syntax(code, "python"))
```

## Theme Features

### Automatic Degradation

UI components automatically adapt based on the theme:

| Feature | Default | Dark | Light | Minimal | Terminal | Monokai | Dracula | Solarized |
|---------|---------|------|-------|---------|----------|---------|---------|-----------|
| **Colors** | ✅ Full | ✅ Full | ✅ Full | ❌ None | ✅ Basic | ✅ Full | ✅ Full | ✅ Full |
| **Emojis** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Boxes/Panels** | ✅ Rich | ✅ Rich | ✅ Rich | ❌ None | ✅ Simple | ✅ Rich | ✅ Rich | ✅ Rich |
| **Syntax Highlighting** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ✅ Basic | ✅ Yes | ✅ Yes | ✅ Yes |
| **Markdown Rendering** | ✅ Full | ✅ Full | ✅ Full | ❌ Plain | ✅ Basic | ✅ Full | ✅ Full | ✅ Full |
| **Progress Bars** | ✅ Rich | ✅ Rich | ✅ Rich | ❌ Text | ✅ Simple | ✅ Rich | ✅ Rich | ✅ Rich |

### Theme Helper Methods

Themes provide helper methods for checking capabilities:

```python
theme = get_theme()

# Check theme capabilities
if theme.is_minimal():
    # Theme has no decorations
    pass

if theme.should_show_banners():
    # Theme supports decorative banners
    pass

if theme.should_show_icons():
    # Theme supports emojis/icons
    pass

if theme.should_show_boxes():
    # Theme supports boxes/panels
    pass
```

## Examples

### Example 1: Running Demo Scripts

The repository includes several demo scripts that showcase UI and terminal capabilities. Following our package management guidelines, use `uv run` to execute them:

```bash
# Interactive UI demo with theme switching
uv run python examples/ui_demo.py

# Quick test of all UI components
uv run python examples/ui_quick_test.py

# Code-focused UI demo
uv run python examples/ui_code_demo.py

# Theme independence demonstration
uv run python examples/ui_theme_independence.py

# Terminal management demo
uv run python examples/ui_terminal_demo.py

# Output system demo
uv run python examples/ui_output_demo.py

# Streaming output demo
uv run python examples/ui_streaming_demo.py
```

### Example 2: Theme Switching in Code

```python
from chuk_term.ui.theme import set_theme, get_theme
from chuk_term.ui.output import get_output

ui = get_output()

# Try different themes
for theme_name in ["default", "minimal", "terminal", "monokai", "dracula"]:
    set_theme(theme_name)
    ui.info(f"Using {theme_name} theme")
    ui.success("Success message")
    ui.error("Error message")
    ui.rule()
```

### Example 3: Custom Theme Creation

```python
from chuk_term.ui.theme import Theme, ColorScheme, Icons, use_theme

# Create a custom color scheme
class CustomColorScheme(ColorScheme):
    def __init__(self):
        super().__init__(
            success="bright_green",
            error="bright_red",
            primary="bright_cyan",
            accent="bright_magenta"
        )

# Create a custom theme
custom_theme = Theme("custom")
custom_theme.colors = CustomColorScheme()

# Use the custom theme
use_theme(custom_theme)
```

## Component-Specific Styling

Different UI components receive theme-appropriate styling:

### User Messages
- **Default/Dark/Light/Monokai/Dracula/Solarized**: Colored border with emoji icon (👤 You)
- **Minimal**: Plain text with "You:" prefix
- **Terminal**: Simple border with "You:" label

### Assistant Messages
- **Default/Dark/Light/Monokai/Dracula/Solarized**: Colored border with robot emoji (🤖 Assistant)
- **Minimal**: Plain text with "Assistant:" prefix
- **Terminal**: Simple border with "Assistant:" label

### Tool Calls
- **Default/Dark/Light/Monokai/Dracula/Solarized**: Colored panel with tool emoji (🔧 Tool Invocation)
- **Minimal**: Plain text with tool name and arguments
- **Terminal**: Simple box with tool information

### Code Display
- **Default/Dark/Light/Monokai/Dracula/Solarized**: Syntax highlighting with line numbers
- **Minimal**: Plain text code block
- **Terminal**: Basic highlighting if supported

## Best Practices

### 1. Let UI Components Handle Themes
Never check theme names in application code. UI components know how to render themselves appropriately.

### 2. Use Semantic Methods
Instead of checking colors directly, use semantic methods:
```python
output.success("Done!")     # Green in default, plain in minimal
output.error("Failed!")     # Red in default, plain in minimal
output.info("Processing...") # Cyan in default, plain in minimal
```

### 3. Tables and Rich Components
Always create Rich components normally - the UI system handles conversion:
```python
# ✅ CORRECT - Theme-agnostic
from rich.table import Table

table = Table(title="Results")
table.add_column("Name")
table.add_column("Status")
table.add_row("Test 1", "✅ Passed")

ui.print_table(table)  # Automatically handles all themes

# ❌ WRONG - Don't check themes
if theme.name == "minimal":
    print("Name      Status")
    print("Test 1    Passed")
else:
    # Create Rich table...
```

The `print_table` method automatically:
- Displays Rich formatting for default/dark/light/monokai/dracula/solarized themes
- Converts to aligned plain text for minimal theme
- Converts to simple ASCII for terminal theme

### 4. Test Across Themes
Use the demo scripts to test your UI across all themes:
```bash
# Test all themes automatically
uv run python examples/ui_theme_independence.py

# Test terminal integration
uv run python examples/ui_terminal_demo.py
```

## Theme Configuration

### Global Theme Setting
The theme is set globally and affects all UI components:

```python
from chuk_term.ui.theme import set_theme

# At application start
set_theme("minimal")  # All UI components now use minimal theme
```

### Theme Persistence
Theme settings can be persisted using environment variables:
```bash
# Set default theme
export CHUK_TERM_THEME=monokai

# All ChukTerm applications will use this theme
python my_app.py
```

## Troubleshooting

### Issue: Emojis Not Displaying
- **Solution**: Switch to `minimal` or `terminal` theme
- **Command**: `set_theme("minimal")`

### Issue: Colors Not Showing
- **Cause**: Terminal doesn't support colors
- **Solution**: Use `minimal` theme for plain text

### Issue: Boxes/Borders Corrupted
- **Cause**: Terminal doesn't support Unicode
- **Solution**: Use `terminal` theme for ASCII-only output

### Issue: Output Too Verbose
- **Solution**: `minimal` theme removes all decorations

## Theme Color Palettes

### Monokai
- Background: `#272822`
- Foreground: `#F8F8F2`
- Red: `#F92672`
- Green: `#A6E22E`
- Yellow: `#F4BF75`
- Blue: `#66D9EF`
- Magenta: `#AE81FF`
- Cyan: `#A1EFE4`

### Dracula
- Background: `#282A36`
- Foreground: `#F8F8F2`
- Red: `#FF5555`
- Green: `#50FA7B`
- Yellow: `#F1FA8C`
- Blue: `#6272A4`
- Magenta: `#FF79C6`
- Cyan: `#8BE9FD`

### Solarized
- Background: `#002B36` (dark) / `#FDF6E3` (light)
- Foreground: `#839496`
- Red: `#DC322F`
- Green: `#859900`
- Yellow: `#B58900`
- Blue: `#268BD2`
- Magenta: `#D33682`
- Cyan: `#2AA198`

## Future Enhancements

Planned theme system improvements:

1. **Custom Theme Loading**: Load themes from YAML/JSON files
2. **Theme Detection**: Auto-detect terminal capabilities
3. **Per-Component Overrides**: Override theme for specific components
4. **Theme Inheritance**: Create themes that extend existing ones
5. **Dynamic Theme Switching**: Change themes without restart
6. **Terminal Capability Detection**: Automatically choose best theme
7. **Additional Themes**: Nord, Gruvbox, One Dark, Material themes

## Related Documentation

- [Output System](./output.md) - Detailed output system documentation
- [Terminal Management](./terminal.md) - Terminal control and detection
- [Prompts and Input](./prompts.md) - Interactive prompt system
- [Code Display](./code.md) - Code rendering and syntax highlighting
- [Formatters](./formatters.md) - Data formatting utilities
- [Banners](./banners.md) - Banner and header displays