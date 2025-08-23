# ChukTerm

A modern terminal library with a powerful CLI interface for building beautiful terminal applications in Python.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🎨 **Rich UI Components**: Banners, prompts, formatters, and code display with syntax highlighting
- 🎯 **Centralized Output Management**: Consistent console output with multiple log levels
- 🎭 **Theme Support**: 7+ built-in themes including monokai, dracula, solarized, minimal, and terminal
- 📝 **Code Display**: Syntax highlighting, diffs, code reviews, and side-by-side comparisons
- 🔧 **Terminal Management**: Screen control, cursor management, hyperlinks, and color detection
- 💬 **Interactive Prompts**: Text input, confirmations, number input, single/multi selection menus
- 📊 **Data Formatting**: Tables, trees, JSON, timestamps, and structured output

## 📦 Installation

### Using uv (Recommended)

```bash
# Install the package
uv add chuk-term

# Install for development
git clone https://github.com/yourusername/chuk-term.git
cd chuk-term
uv sync --dev
```

### Using pip

```bash
# Install from PyPI (when published)
pip install chuk-term

# Install from source
git clone https://github.com/yourusername/chuk-term.git
cd chuk-term
pip install -e ".[dev]"
```

## 🚀 Quick Start

### Basic Output

```python
from chuk_term.ui import output

# Different message types
output.success("✓ Operation completed successfully")
output.error("✗ An error occurred")
output.warning("⚠ This needs attention")
output.info("ℹ Information message")
output.debug("🔍 Debug information")

# Special formatting
output.tip("💡 Pro tip: Use themes for better visuals")
output.hint("This is a subtle hint")
output.command("git commit -m 'Initial commit'")
```

### Interactive Prompts

```python
from chuk_term.ui import ask, confirm, select_from_list, ask_number

# Get user input
name = ask("What's your name?")
age = ask_number("How old are you?", min_value=0, max_value=150)

# Confirmation
if confirm("Would you like to continue?"):
    output.success("Great! Let's proceed...")

# Selection menu
theme = select_from_list(
    ["default", "dark", "light", "minimal", "terminal"],
    "Choose a theme:"
)
```

### Display Code with Syntax Highlighting

```python
from chuk_term.ui import display_code, display_diff

# Show code with syntax highlighting
code = '''def hello_world():
    print("Hello from ChukTerm!")
    return True'''

display_code(code, language="python", title="Example Function")

# Show a diff
display_diff(
    old_text="Hello World",
    new_text="Hello ChukTerm!",
    title="Changes"
)
```

### Theme Support

```python
from chuk_term.ui import output
from chuk_term.ui.theme import set_theme, get_theme

# Set a theme
set_theme("monokai")  # or dracula, solarized, minimal, terminal

# Get current theme
current = get_theme()
output.info(f"Using theme: {current.name}")
```

## 🖥️ CLI Usage

ChukTerm includes a CLI for testing and demonstrating features:

```bash
# Show library information
chuk-term info
chuk-term info --verbose

# Run interactive demo
chuk-term demo

# Run a command with theming
chuk-term run "ls -la"

# Test with specific theme
chuk-term test --theme monokai
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/chuk-term.git
cd chuk-term

# Install with dev dependencies using uv
uv sync --dev

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests with coverage
uv run pytest --cov=chuk_term

# Run specific test file
uv run pytest tests/ui/test_output.py

# Run with verbose output
uv run pytest -v
```

### Code Quality

```bash
# Run linting
uv run ruff check src/ tests/

# Auto-fix linting issues
uv run ruff check --fix src/ tests/

# Format code
uv run black src/ tests/

# Type checking
uv run mypy src/

# Run all checks
make check
```

### Available Make Commands

```bash
make help        # Show all available commands
make dev         # Install for development
make test        # Run tests with coverage
make lint        # Run linting checks
make format      # Format code
make clean       # Remove build artifacts
```

## 📚 Documentation

### Core Documentation
- [Output Management](docs/ui/output.md) - Centralized console output system
- [Terminal Management](docs/ui/terminal.md) - Terminal control and state management
- [Theme System](docs/ui/themes.md) - Theming and styling guide
- [Package Management](docs/PACKAGE_MANAGEMENT.md) - Using uv for dependency management
- [Unit Testing](docs/testing/UNIT_TESTING.md) - Testing guidelines and best practices
- [Test Coverage](docs/testing/TEST_COVERAGE.md) - Coverage requirements and reports

### API Reference

#### Output Levels
- `output.debug()` - Debug information (only in verbose mode)
- `output.info()` - Informational messages
- `output.success()` - Success confirmations
- `output.warning()` - Warning messages
- `output.error()` - Error messages (non-fatal)
- `output.fatal()` - Fatal errors (exits program)

#### Themes
- **default** - Balanced colors, good for most terminals
- **dark** - High contrast on dark backgrounds
- **light** - Optimized for light terminals
- **minimal** - Plain text, no colors or icons
- **terminal** - Basic ANSI colors only
- **monokai** - Popular dark theme
- **dracula** - Gothic dark theme
- **solarized** - Low contrast, easy on eyes

## 📁 Examples

The [examples](examples/) directory contains demonstration scripts:

| File | Description |
|------|-------------|
| `ui_demo.py` | Comprehensive UI component showcase |
| `ui_code_demo.py` | Code display and syntax highlighting |
| `ui_streaming_demo.py` | Streaming and real-time output |
| `ui_theme_independence.py` | Theme system demonstration |
| `ui_output_demo.py` | Output management features |
| `ui_terminal_demo.py` | Terminal control capabilities |
| `ui_quick_test.py` | Quick functionality test |

Run any example:
```bash
uv run python examples/ui_demo.py
```

## 🏗️ Project Structure

```
chuk-term/
├── src/chuk_term/
│   ├── __init__.py        # Package metadata
│   ├── cli.py             # CLI interface
│   └── ui/                # UI components
│       ├── output.py      # Output management
│       ├── terminal.py    # Terminal control
│       ├── theme.py       # Theme system
│       ├── prompts.py     # User prompts
│       ├── formatters.py  # Data formatters
│       ├── code.py        # Code display
│       └── banners.py     # Banner displays
├── tests/                 # Test suite
├── examples/              # Example scripts
├── docs/                  # Documentation
└── pyproject.toml         # Package configuration
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`uv run pytest`)
5. Commit with a descriptive message
6. Push to your fork
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Package management by [uv](https://github.com/astral-sh/uv)
- Testing with [pytest](https://pytest.org/)

## 📮 Support

- 📫 Report issues at [GitHub Issues](https://github.com/yourusername/chuk-term/issues)
- 💬 Discuss at [GitHub Discussions](https://github.com/yourusername/chuk-term/discussions)
- 📖 Read docs at [GitHub Wiki](https://github.com/yourusername/chuk-term/wiki)