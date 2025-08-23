# ChukTerm Project Context

## Project Overview
ChukTerm is a modern Python terminal library with a powerful CLI interface for building beautiful terminal applications. It provides rich UI components, theme support, and comprehensive terminal management utilities.

## Key Features
- 🎨 **Rich UI Components**: Banners, prompts, formatters, and code display with syntax highlighting
- 🎯 **Centralized Output Management**: Consistent console output with multiple log levels (debug, info, success, warning, error, fatal)
- 🎭 **8 Built-in Themes**: default, dark, light, minimal, terminal, monokai, dracula, solarized
- 📝 **Code Display**: Syntax highlighting, diffs, code reviews, side-by-side comparisons
- 🔧 **Terminal Management**: Screen control, cursor management, hyperlinks, color detection
- 💬 **Interactive Prompts**: Text input, confirmations, number input, single/multi selection menus
- 📊 **Data Formatting**: Tables, trees, JSON, timestamps, structured output
- 🔄 **Asyncio Support**: Full async/await support with proper cleanup

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
│   │   ├── output.md      # Output system documentation
│   │   ├── terminal.md    # Terminal management guide
│   │   └── themes.md      # Theme system documentation
│   └── testing/
│       ├── UNIT_TESTING.md
│       └── TEST_COVERAGE.md
└── pyproject.toml         # Package configuration

```

## Common Commands

### Development Setup
```bash
# Install with dev dependencies
uv sync --dev

# Install pre-commit hooks
pre-commit install
```

### Testing
```bash
# Run all tests with coverage
uv run pytest --cov=chuk_term

# Run specific test file
uv run pytest tests/ui/test_output.py -v

# Generate coverage report
uv run pytest --cov=chuk_term --cov-report=html
```

### Code Quality
```bash
# Linting
uv run ruff check src/ tests/

# Auto-fix linting issues
uv run ruff check --fix src/ tests/

# Format code
uv run black src/ tests/

# Type checking
uv run mypy src/

# Run all checks (if Makefile exists)
make check
```

### Running Examples
```bash
# UI components demo
uv run python examples/ui_demo.py

# Code display demo
uv run python examples/ui_code_demo.py

# Output system demo
uv run python examples/ui_output_demo.py

# Terminal management demo
uv run python examples/ui_terminal_demo.py

# Theme demonstration
uv run python examples/ui_theme_independence.py
```

### CLI Usage
```bash
# Show library info
chuk-term info
chuk-term info --verbose

# Run interactive demo
chuk-term demo

# Test with specific theme
chuk-term test --theme monokai
```

## Key Architecture Decisions

### Output System (Singleton)
- Single `Output` instance manages all console output
- Automatically adapts to current theme
- Supports quiet/verbose modes
- Handles non-TTY environments gracefully

### Theme System
- **default/dark/light**: Full Rich formatting with colors and emojis
- **minimal**: Plain text without ANSI codes (for logging/CI)
- **terminal**: Basic ANSI colors only (for simple terminals)
- **monokai/dracula/solarized**: Popular color schemes
- Theme changes affect all output automatically

### Terminal Manager
- Cross-platform support (Windows, macOS, Linux)
- Feature detection (color support, terminal size, etc.)
- Graceful degradation for unsupported features
- Comprehensive asyncio cleanup on exit

## Important Patterns

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
```python
from chuk_term.ui import ask, confirm, select_from_list

name = ask("Name?")
if confirm("Continue?"):
    choice = select_from_list(["A", "B", "C"], "Pick one:")
```

## Testing Guidelines
- All modules have corresponding test files in `tests/`
- Aim for >95% code coverage
- Test all themes and output modes
- Mock external dependencies (filesystem, terminal operations)
- Test both TTY and non-TTY environments

## Common Issues and Solutions

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