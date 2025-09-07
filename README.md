# ChukTerm

A modern terminal library with a powerful CLI interface for building beautiful terminal applications in Python.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Test Coverage](https://img.shields.io/badge/coverage-71%25-yellow.svg)](docs/testing/TEST_COVERAGE.md)
[![Tests](https://img.shields.io/badge/tests-351%20passed-green.svg)](docs/testing/UNIT_TESTING.md)

## ✨ Features

- 🎨 **Rich UI Components**: Banners, prompts, formatters, and code display with syntax highlighting
- 🎯 **Centralized Output Management**: Consistent console output with multiple log levels
- 🎭 **Theme Support**: 8 built-in themes including default, dark, light, minimal, terminal, monokai, dracula, and solarized
- 📝 **Code Display**: Syntax highlighting, diffs, code reviews, and side-by-side comparisons
- 🔧 **Terminal Management**: Screen control, cursor management, hyperlinks, and color detection
- 💬 **Interactive Prompts**: Text input, confirmations, number input, single/multi selection menus
- 📊 **Data Formatting**: Tables, trees, JSON, timestamps, and structured output
- 🌊 **Streaming Support**: Live-updating messages for real-time content streaming (LLM-style)
- 🤖 **AI-Friendly**: Designed for AI agents with comprehensive docs and consistent APIs
- 🔄 **Environment Adaptation**: Automatically adapts to TTY, CI, and NO_COLOR environments

## 📦 Installation

### Using uv (Recommended)

```bash
# Install as dependency
uv add chuk-term

# Install globally as tool
uv tool install chuk-term
```

### Using pip

```bash
# Install from PyPI
pip install chuk-term

# With development dependencies
pip install chuk-term[dev]
```

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/chuk-term.git
cd chuk-term

# Install with uv (recommended)
uv sync --dev

# Or with pip
pip install -e ".[dev]"

# Verify installation
chuk-term --version
```

For detailed installation instructions, see the [Getting Started Guide](docs/ui/GETTING_STARTED.md#installation).

## 🚀 Quick Start

### For AI Agents and LLMs

ChukTerm is designed to be AI-friendly. For comprehensive guidance:
- 📖 Read the [Getting Started Guide](docs/ui/GETTING_STARTED.md)
- 🤖 Check [llms.txt](llms.txt) for LLM-optimized documentation
- 📚 Browse [examples](examples/) for working code

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

### Streaming Messages (New!)

```python
from chuk_term.ui.streaming import StreamingMessage, StreamingAssistant
import time

# Basic streaming message
with StreamingMessage(title="🤖 Assistant") as stream:
    stream.update("Processing your request")
    time.sleep(0.5)
    stream.update("...")
    time.sleep(0.5)
    stream.update(" Done!")
# Automatically finalizes with Markdown rendering

# Using StreamingAssistant for simpler API
assistant = StreamingAssistant()
stream = assistant.start()
for word in "Hello from ChukTerm streaming!".split():
    assistant.update(word + " ")
    time.sleep(0.2)
assistant.finalize()
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

### Quick Start
- 🚀 **[Getting Started Guide](docs/ui/GETTING_STARTED.md)** - Installation, examples, and best practices
- 🤖 **[LLM Documentation](llms.txt)** - AI-optimized reference (llmstxt.org)
- 📂 **[Examples Directory](examples/)** - Working code examples

### Core Documentation
- [Output Management](docs/ui/output.md) - Centralized console output system
- [Terminal Management](docs/ui/terminal.md) - Terminal control and state management
- [Theme System](docs/ui/themes.md) - Theming and styling guide
- [Package Management](docs/PACKAGE_MANAGEMENT.md) - Using uv for dependency management
- [Unit Testing](docs/testing/UNIT_TESTING.md) - Testing guidelines and best practices
- [Test Coverage](docs/testing/TEST_COVERAGE.md) - Coverage requirements and reports
- [Code Quality](docs/testing/CODE_QUALITY.md) - Linting, formatting, and quality standards

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
| `ui_output_demo.py` | Output management features |
| `ui_terminal_demo.py` | Terminal control capabilities |
| `ui_theme_independence.py` | Theme system demonstration |
| **Streaming Demos** | |
| `ui_streaming_demo.py` | Advanced streaming UI capabilities |
| `ui_streaming_message_demo.py` | StreamingMessage and StreamingAssistant demos |
| `ui_streaming_practical_demo.py` | Real-world streaming use cases |
| `ui_streaming_quickstart.py` | Simple streaming examples to get started |
| `streaming_long_text_demo.py` | Token-by-token streaming with proper wrapping |
| **Other** | |
| `ui_quick_test.py` | Quick functionality test |

Run any example:
```bash
# Run the main demo
uv run python examples/ui_demo.py

# Try the streaming demos
uv run python examples/ui_streaming_quickstart.py
uv run python examples/ui_streaming_practical_demo.py
```

## 🏗️ Project Structure

```
chuk-term/
├── src/chuk_term/
│   ├── __init__.py        # Package metadata
│   ├── cli.py             # CLI interface
│   └── ui/                # UI components
│       ├── output.py      # Output management (singleton)
│       ├── terminal.py    # Terminal control
│       ├── theme.py       # Theme system (8 themes)
│       ├── prompts.py     # User prompts
│       ├── formatters.py  # Data formatters
│       ├── code.py        # Code display
│       ├── banners.py     # Banner displays
│       └── streaming.py   # Streaming message support
├── tests/                 # Test suite (351 tests)
├── examples/              # Example scripts
│   ├── ui_demo.py
│   ├── ui_streaming_*.py # Streaming demonstrations
│   └── ...
├── docs/                  # Documentation
│   └── ui/
│       └── GETTING_STARTED.md  # Quick start guide
├── llms.txt              # LLM-optimized docs
├── CLAUDE.md             # Project context
└── pyproject.toml        # Package configuration
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