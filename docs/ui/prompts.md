# Prompts and User Input

## Overview

ChukTerm provides a comprehensive set of interactive prompt utilities for gathering user input. These prompts are theme-aware, support both simple and complex input scenarios, and work across different platforms (Windows, macOS, Linux).

## Features

- **Text Input**: Simple text prompts with optional defaults and validation
- **Confirmations**: Yes/no questions with customizable defaults
- **Number Input**: Integer and float prompts with range validation
- **Selection Menus**: Single and multi-select from lists
- **Password Input**: Secure password entry with masking
- **Interactive Navigation**: Arrow key navigation for menus
- **Theme Integration**: Adapts to current theme settings
- **Platform Support**: Works on Windows, macOS, and Linux

## Basic Usage

### Import Functions

```python
from chuk_term.ui import (
    ask, confirm, ask_number, ask_float,
    select_from_list, multi_select_from_list,
    ask_password
)
```

### Text Input

```python
# Simple text prompt
name = ask("What's your name?")

# With default value
environment = ask("Environment", default="production")

# With validation
def validate_email(value):
    if "@" not in value:
        raise ValueError("Invalid email address")
    return value

email = ask("Email address", validator=validate_email)
```

### Confirmations

```python
# Simple yes/no
if confirm("Continue with deployment?"):
    deploy()

# With default value
if confirm("Delete file?", default=False):
    delete_file()

# Warning confirmation
if confirm("⚠️ This will delete all data. Continue?", default=False):
    delete_all_data()
```

### Number Input

```python
# Integer input
age = ask_number("How old are you?")

# With range validation
port = ask_number(
    "Port number",
    min_value=1024,
    max_value=65535,
    default=8080
)

# Float input
temperature = ask_float(
    "Temperature (°C)",
    min_value=-273.15,
    max_value=1000.0
)

# With step increments
percentage = ask_float(
    "Percentage",
    min_value=0.0,
    max_value=100.0,
    step=0.5
)
```

### Selection Menus

```python
# Single selection
theme = select_from_list(
    ["default", "dark", "light", "minimal", "terminal"],
    "Choose a theme:"
)

# With descriptions
options = [
    ("option1", "First option description"),
    ("option2", "Second option description"),
    ("option3", "Third option description")
]
choice = select_from_list(options, "Select an option:")

# Multi-selection
features = multi_select_from_list(
    ["logging", "monitoring", "caching", "authentication"],
    "Select features to enable:"
)
```

### Password Input

```python
# Basic password
password = ask_password("Enter password:")

# With confirmation
password = ask_password("New password:", confirm=True)

# With strength validation
def validate_strength(pwd):
    if len(pwd) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not any(c.isdigit() for c in pwd):
        raise ValueError("Password must contain at least one digit")
    return pwd

secure_password = ask_password(
    "Create password:",
    validator=validate_strength,
    confirm=True
)
```

## Advanced Features

### Custom Prompt Styles

```python
from chuk_term.ui.prompts import PromptStyle

# Use predefined styles
name = ask("Name:", style=PromptStyle.INFO)
confirm("Delete?", style=PromptStyle.WARNING)

# Custom style
custom = ask("Custom:", style="[bold magenta]")
```

### Interactive Key Navigation

```python
# Create interactive menu with arrow navigation
def interactive_menu():
    """Display menu with arrow key navigation."""
    options = [
        "🏠 Home",
        "📁 Files", 
        "⚙️ Settings",
        "❓ Help",
        "🚪 Exit"
    ]
    
    choice = select_from_list(
        options,
        "Main Menu",
        show_arrows=True,  # Show navigation hints
        allow_escape=True   # ESC to cancel
    )
    
    if choice:
        handle_menu_choice(choice)
```

### Validation Chains

```python
def validate_username(value):
    """Chain multiple validations."""
    # Check length
    if len(value) < 3:
        raise ValueError("Username too short (min 3 chars)")
    if len(value) > 20:
        raise ValueError("Username too long (max 20 chars)")
    
    # Check characters
    if not value.isalnum():
        raise ValueError("Username must be alphanumeric")
    
    # Check availability (mock)
    if value.lower() in ["admin", "root", "user"]:
        raise ValueError("Username already taken")
    
    return value

username = ask("Choose username:", validator=validate_username)
```

### Progress Prompts

```python
# Show progress while waiting for input
with ui.progress("Checking availability..."):
    username = ask("Username:")
    # Validation happens here
    check_username_availability(username)
```

## Theme Adaptation

Prompts automatically adapt to the current theme:

### Default/Dark/Light Themes
- Full color support with Rich formatting
- Styled prompts with borders and icons
- Interactive highlighting in menus
- Emoji indicators

### Minimal Theme
- Plain text prompts without colors
- Simple text-based menus
- No emoji or special characters
- Basic input/output

### Terminal Theme
- Basic ANSI colors only
- ASCII characters for indicators
- Simple formatting
- Compatible with legacy terminals

```python
from chuk_term.ui.theme import set_theme

# Minimal theme - plain text
set_theme("minimal")
name = ask("Name:")  # Plain: "Name: "

# Default theme - styled
set_theme("default")
name = ask("Name:")  # Styled: "[cyan]Name:[/cyan] "
```

## Platform-Specific Behavior

### Key Input Detection

The prompt system handles platform differences transparently:

```python
# Windows
# Uses msvcrt for key detection
# Handles special keys like arrows

# Unix/Linux/macOS  
# Uses termios for raw terminal mode
# Handles ANSI escape sequences

# Fallback
# Uses standard input when terminal features unavailable
```

### Special Keys

| Key | Windows | Unix/macOS | Function |
|-----|---------|------------|----------|
| ↑ | Up Arrow | ESC[A | Previous option |
| ↓ | Down Arrow | ESC[B | Next option |
| ← | Left Arrow | ESC[D | Cancel/Back |
| → | Right Arrow | ESC[C | Select/Forward |
| Enter | \r | \n | Confirm selection |
| Space | (space) | (space) | Toggle selection |
| Escape | ESC | ESC | Cancel operation |
| Tab | \t | \t | Next field |

## Error Handling

### Validation Errors

```python
def safe_number_input():
    """Handle validation errors gracefully."""
    while True:
        try:
            value = ask_number(
                "Enter port (1024-65535):",
                min_value=1024,
                max_value=65535
            )
            return value
        except ValueError as e:
            ui.error(f"Invalid input: {e}")
            if not confirm("Try again?"):
                return None
```

### Interrupt Handling

```python
try:
    name = ask("Name:")
except KeyboardInterrupt:
    ui.warning("\nInput cancelled")
    return None
except EOFError:
    ui.warning("\nEnd of input")
    return None
```

## Best Practices

### 1. Provide Clear Prompts

```python
# ✅ GOOD - Clear and specific
port = ask_number("Enter server port (1024-65535):", 
                  min_value=1024, max_value=65535)

# ❌ BAD - Vague
number = ask_number("Number:")
```

### 2. Use Appropriate Input Types

```python
# ✅ GOOD - Use specific prompt types
age = ask_number("Age:", min_value=0, max_value=150)
agree = confirm("Accept terms?")
rating = ask_float("Rating (0-5):", min_value=0, max_value=5)

# ❌ BAD - Using text for everything
age = ask("Age:")  # No validation
agree = ask("Accept? (yes/no)")  # Should use confirm
```

### 3. Provide Defaults When Appropriate

```python
# ✅ GOOD - Sensible defaults
env = ask("Environment:", default="development")
port = ask_number("Port:", default=8080)
verbose = confirm("Enable verbose output?", default=False)

# ❌ BAD - No defaults for common values
env = ask("Environment:")  # User must type every time
```

### 4. Validate Input Early

```python
# ✅ GOOD - Validate immediately
def validate_path(path):
    if not os.path.exists(path):
        raise ValueError(f"Path does not exist: {path}")
    return path

file_path = ask("File path:", validator=validate_path)

# ❌ BAD - Validate later
file_path = ask("File path:")
# ... much later ...
if not os.path.exists(file_path):
    print("Invalid path!")
```

### 5. Handle Cancellation Gracefully

```python
# ✅ GOOD - Allow user to cancel
choice = select_from_list(
    options,
    "Select option (ESC to cancel):",
    allow_escape=True
)
if choice is None:
    ui.info("Operation cancelled")
    return

# ❌ BAD - Force user to choose
while True:
    choice = select_from_list(options, "You must choose:")
    # No way to cancel
```

## Examples

### Configuration Wizard

```python
def configuration_wizard():
    """Interactive configuration setup."""
    ui.rule("Configuration Wizard")
    
    # Basic settings
    config = {}
    
    config['name'] = ask("Project name:")
    config['version'] = ask("Version:", default="1.0.0")
    
    # Environment selection
    config['env'] = select_from_list(
        ["development", "staging", "production"],
        "Environment:"
    )
    
    # Database configuration
    if confirm("Configure database?", default=True):
        config['db_host'] = ask("Database host:", default="localhost")
        config['db_port'] = ask_number("Database port:", default=5432)
        config['db_name'] = ask("Database name:")
        config['db_user'] = ask("Database user:")
        config['db_pass'] = ask_password("Database password:")
    
    # Feature selection
    features = multi_select_from_list(
        ["caching", "monitoring", "logging", "authentication"],
        "Enable features:"
    )
    config['features'] = features
    
    # Confirmation
    ui.panel(f"Configuration:\n{json.dumps(config, indent=2)}")
    
    if confirm("Save configuration?", default=True):
        save_config(config)
        ui.success("✓ Configuration saved")
    else:
        ui.warning("Configuration discarded")
```

### Interactive CLI Menu

```python
def main_menu():
    """Main application menu."""
    while True:
        ui.clear()
        ui.rule("ChukTerm Demo")
        
        options = [
            ("themes", "🎨 Theme Switcher"),
            ("output", "📝 Output Demo"),
            ("terminal", "🖥️ Terminal Features"),
            ("code", "💻 Code Display"),
            ("config", "⚙️ Configuration"),
            ("exit", "🚪 Exit")
        ]
        
        choice = select_from_list(
            options,
            "Select an option:",
            show_descriptions=True
        )
        
        if choice == "exit" or choice is None:
            if confirm("Exit application?", default=True):
                ui.info("Goodbye!")
                break
        else:
            handle_menu_option(choice)
```

## Testing Prompts

### Unit Testing

```python
import pytest
from unittest.mock import patch, MagicMock

def test_ask_with_default():
    """Test ask prompt with default value."""
    with patch('chuk_term.ui.prompts.Prompt.ask') as mock_ask:
        mock_ask.return_value = "test"
        
        result = ask("Name:", default="default")
        assert result == "test"
        mock_ask.assert_called_once()

def test_confirm_yes():
    """Test confirmation with yes response."""
    with patch('chuk_term.ui.prompts.Confirm.ask') as mock_confirm:
        mock_confirm.return_value = True
        
        result = confirm("Continue?")
        assert result is True

@patch('chuk_term.ui.prompts._get_key')
def test_menu_navigation(mock_get_key):
    """Test menu arrow key navigation."""
    # Simulate: down, down, enter
    mock_get_key.side_effect = ['down', 'down', 'enter']
    
    options = ["Option 1", "Option 2", "Option 3"]
    # Would select "Option 3"
```

### Integration Testing

```python
def test_prompt_theme_adaptation():
    """Test prompts adapt to theme changes."""
    from chuk_term.ui.theme import set_theme
    
    # Test with each theme
    for theme in ["default", "minimal", "terminal"]:
        set_theme(theme)
        # Mock input and verify output format
        # differs based on theme
```

## Module Reference

### Core Functions

| Function | Description | Returns |
|----------|-------------|---------|
| `ask(prompt, default, validator)` | Text input prompt | `str` |
| `confirm(prompt, default)` | Yes/no confirmation | `bool` |
| `ask_number(prompt, min, max, default)` | Integer input | `int` |
| `ask_float(prompt, min, max, default)` | Float input | `float` |
| `select_from_list(options, prompt)` | Single selection | `str` or `None` |
| `multi_select_from_list(options, prompt)` | Multiple selection | `list[str]` |
| `ask_password(prompt, confirm)` | Password input | `str` |

### Classes

| Class | Description |
|-------|-------------|
| `PromptStyle` | Predefined prompt styles |
| `Validator` | Base class for custom validators |

### Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `PromptStyle.DEFAULT` | `"[bold cyan]"` | Default prompt style |
| `PromptStyle.WARNING` | `"[bold yellow]"` | Warning prompts |
| `PromptStyle.ERROR` | `"[bold red]"` | Error prompts |
| `PromptStyle.SUCCESS` | `"[bold green]"` | Success prompts |
| `PromptStyle.INFO` | `"[bold blue]"` | Info prompts |

## Related Documentation

- [Output System](./output.md) - Output management that prompts integrate with
- [Theme System](./themes.md) - How prompts adapt to themes
- [Terminal Management](./terminal.md) - Terminal features used by prompts
- [Unit Testing](../testing/UNIT_TESTING.md) - Testing prompt interactions