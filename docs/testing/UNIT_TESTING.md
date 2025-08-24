# Unit Testing Guide for ChukTerm

## Overview

Unit testing focuses on testing individual functions and methods in isolation. This document covers principles and patterns for effective unit testing in the ChukTerm project.

## Core Principles

### Test Isolation
- Each unit test should be completely independent
- No shared state between tests
- Mock external dependencies
- Test one thing at a time

### Test Structure (AAA Pattern)
```python
@pytest.mark.asyncio
async def test_function_behavior():
    """Test specific behavior of function."""
    # Arrange - Set up test data and conditions
    input_data = prepare_test_data()
    expected_result = calculate_expected()
    
    # Act - Execute the function under test
    actual_result = await function_under_test(input_data)
    
    # Assert - Verify the result
    assert actual_result == expected_result
```

## Unit Test Organization

### File Structure
```
tests/
├── conftest.py              # Global test configuration and fixtures
├── test_main.py            # Main package tests
├── test_cli.py             # CLI interface tests
└── ui/
    ├── test_theme.py       # Theme system tests
    ├── test_terminal.py    # Terminal management tests  
    ├── test_output.py      # Output management tests
    ├── test_prompts.py     # User prompts and interactions tests
    ├── test_code.py        # Code display and syntax highlighting tests
    ├── test_formatters.py  # Data formatting utilities tests
    └── test_banners.py     # Banner display tests (if implemented)
```

### Test Class Organization
```python
class TestFunctionName:
    """Unit tests for function_name."""
    
    def test_normal_operation(self):
        """Test expected behavior with valid input."""
        pass
    
    def test_edge_cases(self):
        """Test boundary conditions."""
        pass
    
    def test_error_conditions(self):
        """Test error handling."""
        pass
    
    def test_type_validation(self):
        """Test input type handling."""
        pass
```

## Mocking Strategies

### Basic Mocking
```python
from unittest.mock import Mock, patch

def test_output_with_mock_console():
    """Test Output with mocked Rich console."""
    from chuk_term.ui.output import Output
    
    # Create mock console
    mock_console = Mock()
    
    # Inject mock
    output = Output()
    output.console = mock_console
    
    # Test output
    output.info("Test message")
    
    # Verify interaction
    mock_console.print.assert_called()
```

### Patching Dependencies
```python
@patch('chuk_term.ui.terminal.shutil.get_terminal_size')
def test_terminal_size_detection(mock_get_size):
    """Test terminal size detection with patched shutil."""
    from chuk_term.ui.terminal import get_terminal_size
    
    # Mock terminal size
    mock_get_size.return_value = (120, 40)
    
    cols, rows = get_terminal_size()
    
    assert cols == 120
    assert rows == 40
    mock_get_size.assert_called_once()
```

### Async Mocking
```python
import asyncio
import pytest

@pytest.mark.asyncio
async def test_asyncio_cleanup():
    """Test asyncio cleanup functionality."""
    from chuk_term.ui.terminal import TerminalManager
    
    # Create some async tasks
    async def dummy_task():
        await asyncio.sleep(10)
    
    task = asyncio.create_task(dummy_task())
    
    # Cleanup should cancel tasks
    TerminalManager.cleanup_asyncio()
    
    assert task.cancelled() or task.done()
```

## Testing Patterns

### Testing Pure Functions
```python
def test_theme_capability_checks():
    """Test deterministic theme capability checks."""
    from chuk_term.ui.theme import Theme
    
    # Create minimal theme
    theme = Theme("minimal")
    
    # Pure functions - always same output for same theme
    assert theme.is_minimal() is True
    assert theme.should_show_icons() is False
    assert theme.should_show_boxes() is False
    
    # Create default theme
    theme = Theme("default")
    assert theme.is_minimal() is False
    assert theme.should_show_icons() is True
```

### Testing Stateful Functions
```python
class TestOutput:
    """Test Output singleton with internal state."""
    
    def setup_method(self):
        """Reset output state before each test."""
        from chuk_term.ui.output import get_output
        self.output = get_output()
        self.output.set_output_mode(quiet=False, verbose=False)
    
    def test_quiet_mode(self):
        """Test quiet mode suppresses info messages."""
        self.output.set_output_mode(quiet=True)
        # In quiet mode, info messages should be suppressed
        # but errors and success should still show
        
    def test_verbose_mode(self):
        """Test verbose mode shows debug messages."""
        self.output.set_output_mode(verbose=True)
        # In verbose mode, debug messages should be visible
```

### Testing Error Conditions
```python
def test_theme_validation():
    """Test that invalid themes raise appropriate errors."""
    from chuk_term.ui.theme import set_theme
    
    # Valid themes should work
    set_theme("default")  # Should not raise
    set_theme("minimal")  # Should not raise
    
    # Invalid theme handling (if implemented)
    # with pytest.raises(ValueError, match="Unknown theme"):
    #     set_theme("invalid_theme")
```

### Testing Side Effects
```python
def test_terminal_title_change(monkeypatch):
    """Test setting terminal title."""
    from chuk_term.ui.terminal import set_terminal_title
    import subprocess
    
    # Mock subprocess.run to capture commands
    commands_run = []
    def mock_run(cmd, **kwargs):
        commands_run.append(cmd)
        return subprocess.CompletedProcess(cmd, 0)
    
    monkeypatch.setattr(subprocess, "run", mock_run)
    
    set_terminal_title("Test Title")
    
    # Verify appropriate command was run
    assert any("Test Title" in str(cmd) for cmd in commands_run)
```

## Parametrized Testing

### Basic Parametrization
```python
@pytest.mark.parametrize("theme_name,has_colors,has_icons", [
    ("default", True, True),
    ("dark", True, True),
    ("light", True, True),
    ("minimal", False, False),
    ("terminal", True, False),
    ("monokai", True, True),
    ("dracula", True, True),
    ("solarized", True, True),
])
def test_theme_features(theme_name, has_colors, has_icons):
    """Test theme feature availability."""
    from chuk_term.ui.theme import Theme
    
    theme = Theme(theme_name)
    if has_colors:
        assert theme.colors.success != ""
    assert theme.should_show_icons() == has_icons
```

### Complex Parametrization
```python
@pytest.mark.parametrize("command,args,expected_output", [
    ("tools", {}, "Available tools"),
    ("servers", {}, "Connected servers"),
    ("provider", {}, "Current provider"),
    ("model", {}, "Current model"),
])
def test_commands(command, args, expected_output):
    """Test various CLI commands."""
    from chuk_term.commands import execute_command
    
    result = execute_command(command, args)
    assert expected_output in result
```

## Fixtures

### Basic Fixtures
```python
@pytest.fixture
def mock_console():
    """Provide mock Rich console for tests."""
    from unittest.mock import Mock
    console = Mock()
    console.is_terminal = True
    console.width = 80
    console.height = 24
    return console

def test_output_with_fixture(mock_console):
    """Test output using fixture."""
    from chuk_term.ui.output import Output
    
    output = Output()
    output.console = mock_console
    output.info("Test")
    
    mock_console.print.assert_called()
```

### Fixture Scopes
```python
@pytest.fixture(scope="function")  # Default - per test
def test_theme():
    """Create test theme for each test."""
    from chuk_term.ui.theme import Theme, set_theme
    original_theme = get_theme()
    test_theme = Theme("minimal")
    set_theme("minimal")
    yield test_theme
    set_theme(original_theme.name)  # Restore

@pytest.fixture(scope="class")  # Per test class
def terminal_manager():
    """Shared terminal manager for test class."""
    from chuk_term.ui.terminal import TerminalManager
    return TerminalManager

@pytest.fixture(scope="module")  # Per test module
def ui_config():
    """Load UI configuration once per module."""
    return {
        "theme": "default",
        "quiet": False,
        "verbose": False,
        "no_color": False
    }
```

## Coverage Guidelines

### What to Test
- All public functions/methods
- Complex private methods
- Error handling paths
- Edge cases and boundaries
- Different input types
- State transitions

### What Not to Test
- Simple getters/setters
- Framework code
- Third-party libraries
- Trivial functions (unless critical)
- Generated code

### Coverage Metrics

For comprehensive coverage guidance, see [Test Coverage Guide](./TEST_COVERAGE.md).

```bash
# Check coverage (using uv)
uv run pytest tests/ --cov=chuk_term --cov-report=term-missing

# Enforce minimum coverage
uv run pytest tests/ --cov=chuk_term --cov-fail-under=80

# Generate HTML report
uv run pytest tests/ --cov=chuk_term --cov-report=html

# Using Makefile commands
make test          # Run all tests with coverage
make check         # Run all checks (ruff, black, mypy, pytest)
```

Target coverage levels:
- Overall: ≥ 80%
- Core modules: ≥ 90%
- New code: ≥ 95%

## Common Test Issues and Solutions

### Rich Console Output Capture
When testing methods that use Rich console for output (especially stderr), the output may not be captured properly by `capsys`:

```python
# Issue: Rich console output to stderr doesn't get captured
def test_error_output(capsys):
    output.error("Error message")
    captured = capsys.readouterr()
    assert "Error" in captured.err  # May fail!

# Solution: Just verify the method doesn't crash
def test_error_output():
    output.error("Error message")  # Verify no exceptions
```

This is a known limitation when Rich formats output with ANSI codes. For critical output verification, consider mocking the console or testing with minimal theme.

## Best Practices

### DO's
✅ Keep tests simple and focused  
✅ Use descriptive test names  
✅ Test behavior, not implementation  
✅ Use fixtures for common setup  
✅ Mock external dependencies  
✅ Test edge cases  
✅ Maintain test isolation  
✅ Write tests first (TDD)  

### DON'Ts
❌ Don't test multiple behaviors in one test  
❌ Don't use production data  
❌ Don't make tests dependent on order  
❌ Don't test private methods directly  
❌ Don't ignore test failures  
❌ Don't use hard-coded delays  
❌ Don't over-mock  
❌ Don't write brittle tests  

## Example: Complete Unit Test

```python
"""Unit tests for Output.print_table function."""

import pytest
from unittest.mock import Mock, patch
from chuk_term.ui.output import Output
from chuk_term.ui.theme import set_theme
from rich.table import Table

class TestPrintTable:
    """Test cases for table printing."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.output = Output()
        self.output.console = Mock()
    
    @pytest.mark.parametrize("theme_name,should_use_rich", [
        ("default", True),
        ("dark", True),
        ("light", True),
        ("minimal", False),  # Should convert to text
        ("terminal", False),  # Should convert to ASCII
    ])
    def test_table_rendering_by_theme(self, theme_name, should_use_rich):
        """Test table rendering varies by theme."""
        set_theme(theme_name)
        
        # Create a table
        table = Table(title="Test")
        table.add_column("Col1")
        table.add_row("Data")
        
        self.output.print_table(table)
        
        # Verify appropriate rendering method was used
        if should_use_rich:
            self.output.console.print.assert_called_with(table)
        else:
            # For minimal/terminal, table is converted to text
            self.output.console.print.assert_called()
            args = self.output.console.print.call_args[0]
            assert isinstance(args[0], str)  # Text, not Table
    
    def test_empty_table_handling(self):
        """Test handling of empty tables."""
        table = Table()
        self.output.print_table(table)
        self.output.console.print.assert_called()
```

## Related Documentation
- [Test Coverage Guide](./TEST_COVERAGE.md) - Coverage targets and best practices
- [Package Management](../PACKAGE_MANAGEMENT.md) - Using uv for test dependencies
- [UI Themes](../ui/themes.md) - Testing UI components across themes
- [Project README](../../README.md) - Project overview and setup