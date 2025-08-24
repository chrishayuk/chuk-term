# ChukTerm Project Context

## Project Overview
ChukTerm is a modern Python terminal library with a powerful CLI interface for building beautiful terminal applications. It provides rich UI components, theme support, and comprehensive terminal management utilities.

### 📚 Quick Documentation Links
- **[Getting Started Guide](docs/ui/GETTING_STARTED.md)** - Comprehensive guide with installation, examples, and patterns
- **[LLM Documentation](llms.txt)** - Optimized documentation following llmstxt.org specification
- **[API Reference](docs/ui/output.md)** - Complete API documentation
- **[Examples](examples/)** - Working code examples for all features

### 🚀 Quick Start for AI Agents
```python
from chuk_term.ui import output, ask, confirm

# Basic output
output.info("Processing request...")
output.success("✓ Task completed")
output.error("✗ Something went wrong")

# User interaction
name = ask("What's your name?")
if confirm("Continue?"):
    output.info(f"Hello, {name}!")
```
For more examples, see the [Getting Started Guide](docs/ui/GETTING_STARTED.md#quick-start).

## Key Features
- 🎨 **Rich UI Components**: Banners, prompts, formatters, and code display with syntax highlighting
- 🎯 **Centralized Output Management**: Consistent console output with multiple log levels (debug, info, success, warning, error, fatal)
- 🎭 **8 Built-in Themes**: default, dark, light, minimal, terminal, monokai, dracula, solarized
- 📝 **Code Display**: Syntax highlighting, diffs, code reviews, side-by-side comparisons
- 🔧 **Terminal Management**: Screen control, cursor management, hyperlinks, color detection
- 💬 **Interactive Prompts**: Text input, confirmations, number input, single/multi selection menus
- 📊 **Data Formatting**: Tables, trees, JSON, timestamps, structured output
- 🔄 **Asyncio Support**: Full async/await support with proper cleanup

## Installation

### Quick Install
```bash
# Using uv (recommended)
uv add chuk-term

# Using pip
pip install chuk-term

# From source for development
git clone https://github.com/yourusername/chuk-term.git
cd chuk-term
uv sync --dev  # or pip install -e ".[dev]"
```

For detailed installation instructions, see the [Getting Started Guide](docs/ui/GETTING_STARTED.md#installation).

## Development Environment
- **Python Version**: 3.10+ required
- **Package Manager**: uv (recommended) or pip
- **Dependencies**: click (CLI), rich (terminal formatting)
- **Dev Tools**: pytest, pytest-cov, ruff, mypy, black

## Project Structure
```
chuk-term/
├── src/chuk_term/          # Main package source
│   ├── __init__.py         # Package metadata
│   ├── cli.py              # CLI interface
│   └── ui/                 # UI components
│       ├── output.py       # Centralized output management (singleton)
│       ├── terminal.py     # Terminal control and detection
│       ├── theme.py        # Theme system (8 themes)
│       ├── prompts.py      # Interactive user prompts
│       ├── formatters.py   # Data formatting utilities
│       ├── code.py         # Code display with syntax highlighting
│       └── banners.py      # Banner and header displays
├── tests/                  # Comprehensive test suite
├── examples/               # Demo scripts for all features
├── docs/                   # Detailed documentation
│   ├── ui/
│   │   ├── GETTING_STARTED.md # 🚀 Quick start guide for developers/AI agents
│   │   ├── output.md      # Output system documentation
│   │   ├── terminal.md    # Terminal management guide
│   │   └── themes.md      # Theme system documentation
│   └── testing/
│       ├── UNIT_TESTING.md
│       └── TEST_COVERAGE.md
├── llms.txt               # 🤖 LLM-optimized documentation (llmstxt.org)
└── pyproject.toml         # Package configuration

```

## Common Commands

### Development Setup
⚙️ **[Full Installation Guide](docs/ui/GETTING_STARTED.md#installation)**
```bash
# Install with dev dependencies
make dev-install
# Or using uv directly:
uv sync --dev
```

### Testing
🧪 **[Testing Documentation](docs/testing/UNIT_TESTING.md)**
```bash
# Run all tests
make test

# Run tests with coverage report (current: 71%)
make test-cov

# Or using uv directly:
uv run pytest --cov=chuk_term
uv run pytest tests/ui/test_output.py -v
```

### Code Quality
🎯 **[Code Quality Standards](docs/testing/CODE_QUALITY.md)** | **[Best Practices](docs/testing/UNIT_TESTING.md#best-practices)**
```bash
# Run all checks (linting, formatting, type checking, tests)
make check

# Individual commands:
make lint       # Check code quality with ruff and black
make format     # Auto-fix formatting issues
make typecheck  # Run mypy type checking

# Or using uv directly:
uv run ruff check src/ tests/
uv run black --check src/ tests/
uv run mypy src/
```

### Running Examples
📂 **[Browse All Examples](examples/)**
```bash
# Run interactive demo
make demo

# Or run specific examples:
uv run python examples/ui_demo.py
uv run python examples/ui_code_demo.py
uv run python examples/ui_output_demo.py
uv run python examples/ui_terminal_demo.py
uv run python examples/ui_theme_independence.py
```

### CLI Usage
```bash
# Show library info
chuk-term info
chuk-term info --verbose

# Run interactive demo
make demo
# Or:
chuk-term demo

# Test with specific theme
chuk-term test --theme monokai
```

## Key Architecture Decisions

### Output System (Singleton)
📖 **[Full Output API Documentation](docs/ui/output.md)**
- Single `Output` instance manages all console output
- Automatically adapts to current theme
- Supports quiet/verbose modes
- Handles non-TTY environments gracefully

### Theme System
🎨 **[Complete Theme Documentation](docs/ui/themes.md)**
- **default/dark/light**: Full Rich formatting with colors and emojis
- **minimal**: Plain text without ANSI codes (for logging/CI)
- **terminal**: Basic ANSI colors only (for simple terminals)
- **monokai/dracula/solarized**: Popular color schemes
- Theme changes affect all output automatically

### Terminal Manager
🖥️ **[Terminal Management Guide](docs/ui/terminal.md)**
- Cross-platform support (Windows, macOS, Linux)
- Feature detection (color support, terminal size, etc.)
- Graceful degradation for unsupported features
- Comprehensive asyncio cleanup on exit

## Important Patterns

📚 **[See Getting Started Guide for More Examples](docs/ui/GETTING_STARTED.md#common-patterns-for-ai-agents)**

### Using the Output System
```python
from chuk_term.ui import output

# Different message levels
output.info("Processing...")
output.success("✓ Complete")
output.error("Failed")
output.warning("Check this")
output.debug("Details")  # Only in verbose mode
```

### Theme-Agnostic Code
Always write code that works with any theme:
```python
# GOOD - Let the system handle theme differences
ui.print_table(table)  # Automatically adapts to theme

# BAD - Don't check themes in application code
if theme.name == "minimal":
    print("plain text")
```

### Interactive Prompts
💬 **[Prompt Examples](docs/ui/GETTING_STARTED.md#user-interaction)**
```python
from chuk_term.ui import ask, confirm, select_from_list

name = ask("Name?")
if confirm("Continue?"):
    choice = select_from_list(["A", "B", "C"], "Pick one:")
```

## Testing Guidelines
🧪 **[Unit Testing Guide](docs/testing/UNIT_TESTING.md)** | **[Coverage Report](docs/testing/TEST_COVERAGE.md)**
- All modules have corresponding test files in `tests/`
- Current coverage: 71% (target: >80%)
- Test all themes and output modes
- Mock external dependencies (filesystem, terminal operations)
- Test both TTY and non-TTY environments

## Common Issues and Solutions

🔧 **[Troubleshooting Guide](docs/ui/GETTING_STARTED.md#error-recovery)**

### Import Errors
- Ensure running from project root
- Use `uv run` to execute scripts
- Check Python path includes `src/`

### Theme Not Applying
- Theme changes are global and immediate
- Some terminals may not support certain features
- Test with different terminal emulators

### Asyncio Cleanup
- Always call `restore_terminal()` on exit
- The system handles task cancellation automatically
- Cleanup is performed even on exceptions

## Code Style
📝 **[See Contributing Guidelines](CONTRIBUTING.md)**
- Line length: 120 characters
- Use type hints for all functions
- Follow PEP 8 with Black formatting
- Comprehensive docstrings for public APIs
- No direct print() calls - use output system

## Performance Considerations
- Output system is a singleton (no initialization overhead)
- Theme lookups are cached
- Terminal capabilities detected once and cached
- Rich console instances are reused

## Security Notes
- No external network calls
- No file system modifications outside explicit operations
- Input sanitization in prompts
- Safe handling of ANSI escape sequences

## Future Improvements (Potential)
- [ ] More themes (nord, gruvbox, etc.)
- [ ] Progress bars with time estimates
- [ ] Multi-column layouts
- [ ] Keyboard shortcut handling
- [ ] Configuration file support
- [ ] Plugin system for custom components
- [ ] Async prompt support
- [ ] Terminal multiplexer detection improvements

## Quick Debugging
🔍 **[Debug Tips in Getting Started](docs/ui/GETTING_STARTED.md#error-recovery)**
```python
# Check current theme
from chuk_term.ui.theme import get_theme
print(get_theme().name)

# Check terminal capabilities  
from chuk_term.ui.terminal import get_terminal_info
print(get_terminal_info())

# Enable verbose output
from chuk_term.ui.output import get_output
get_output().set_output_mode(verbose=True)
```

## Related Projects
- **Rich**: Terminal formatting library (main dependency)
- **Click**: CLI creation kit (used for CLI interface)
- **uv**: Fast Python package manager (recommended for development)

## Maintenance Notes
- Regular dependency updates via `uv lock --upgrade`
- Test on multiple terminals (iTerm2, Terminal.app, Windows Terminal, etc.)
- Maintain backward compatibility for Python 3.10+
- Keep documentation in sync with code changes

## 🤖 Important Guidelines for AI Agents

### Code Quality Requirements
When making changes to this codebase, you MUST:

1. **Run Code Quality Checks** - After making any code changes, always run:
   ```bash
   # Check linting (MUST pass before committing)
   uv run ruff check src/ tests/
   
   # Check formatting (MUST pass before committing)
   uv run black --check src/ tests/
   
   # Check type hints (MUST pass before committing)
   uv run mypy src/
   
   # Auto-fix issues if needed
   uv run ruff check --fix --unsafe-fixes src/ tests/
   uv run black src/ tests/
   ```

2. **Run Tests** - Verify your changes don't break existing functionality:
   ```bash
   # Run all tests
   make test
   
   # Run with coverage to ensure no regression
   make test-cov
   ```

3. **Complete Verification Command** - Use this single command to verify everything:
   ```bash
   # Run all checks (linting, formatting, type checking, and tests)
   make check
   # This runs: ruff, black, mypy, and pytest
   ```

### When to Run Checks
- **ALWAYS** after making code changes
- **BEFORE** suggesting code is complete
- **WHEN** the user asks you to "fix linting", "check types", or "check tests"
- **IF** you see import errors, type errors, or syntax issues

### Common Issues and Solutions
- **Unused imports (F401)**: Remove or add `# noqa: F401` if intentional
- **Unused arguments (ARG001/ARG002)**: Use `_` prefix or add `# noqa: ARG002` for test mocks
- **Line too long**: Keep lines under 120 characters
- **Formatting issues**: Run `uv run black src/ tests/` to auto-fix
- **Type errors**: Add type hints or use `# type: ignore` comments sparingly
- **Missing return type**: Add `-> None` for functions that don't return a value

### Test Coverage Target
- Current coverage: 71%
- Target coverage: >80%
- Never let coverage drop below current level

## Build and Publishing

### Building the Package
```bash
# Build distribution packages
make build
```

### Publishing to PyPI
📦 **[Full Publishing Guide](docs/PACKAGE_MANAGEMENT.md#publishing-chukterm)**
```bash
# Check PyPI credentials
make info

# Publish to TestPyPI first (recommended)
make publish-test

# Publish to PyPI
make publish
```

### Utility Commands
```bash
# Show project info and credential status
make info

# Clean build artifacts
make clean

# Deep clean everything
make clean-all

# Show all available commands
make help
```

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
ALWAYS run code quality checks (linting, formatting, type checking, tests) after making code changes.
Use `make check` to run all quality checks at once (ruff, black, mypy, pytest).