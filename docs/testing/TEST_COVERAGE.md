# Test Coverage Guide

## Overview

Test coverage measures how much of your code is executed during testing. This guide covers coverage measurement, targets, and best practices for the ChukTerm project.

## Coverage Tools

### Installation
```bash
# Install coverage tools using uv (preferred)
uv add --dev pytest-cov

# The tool is already included in pyproject.toml dev dependencies
```

### Running Coverage Reports

```bash
# Basic coverage report
uv run pytest --cov=chuk_term

# Detailed terminal report with missing lines
uv run pytest --cov=chuk_term --cov-report=term-missing

# Generate HTML coverage report
uv run pytest --cov=chuk_term --cov-report=html

# Coverage for specific module
uv run pytest --cov=chuk_term.ui tests/ui/

# Fail tests if coverage drops below threshold
uv run pytest --cov=chuk_term --cov-fail-under=80

# Using Makefile commands
make test          # Run tests with coverage
make check         # Run all checks including coverage
```

## Coverage Targets

### Project Goals
- **Overall Coverage**: ≥ 80%
- **Core Modules**: ≥ 90%
- **New Code**: ≥ 95%
- **Critical Paths**: 100%

### Module-Specific Targets

| Module Category | Target Coverage | Priority | Current |
|----------------|-----------------|----------|----------|
| CLI Interface (`cli.py`) | 95% | Critical | 100% ✅ |
| Output Management (`ui/output.py`) | 90% | Critical | 62% ⚠️ |
| Terminal Management (`ui/terminal.py`) | 95% | High | 97% ✅ |
| Theme System (`ui/theme.py`) | 90% | High | 98% ✅ |
| Prompts (`ui/prompts.py`) | 85% | High | 79% |
| Code Display (`ui/code.py`) | 85% | Medium | 72% |
| Formatters (`ui/formatters.py`) | 80% | Medium | 73% |
| Banners (`ui/banners.py`) | 75% | Low | 20% ⚠️ |
| Example Scripts | 0% | N/A | N/A |

## Understanding Coverage Reports

### Terminal Output
```
Name                            Stmts   Miss  Cover   Missing
----------------------------------------------------------------
chuk_term/__init__.py                3      0   100%
chuk_term/cli.py                    45     12    73%   42-53
chuk_term/ui/__init__.py           15      0   100%
chuk_term/ui/terminal.py          215      2    99%   487-488
chuk_term/ui/output.py            390    122    69%   Various
chuk_term/ui/theme.py             156      3    98%   234-236
chuk_term/ui/prompts.py            89     16    82%   67-82
chuk_term/ui/code.py              112     28    75%   Various
chuk_term/ui/formatters.py        78     15    81%   Various
chuk_term/ui/banners.py           45     12    73%   Various
----------------------------------------------------------------
TOTAL                            1148    210    82%
```

- **Stmts**: Total number of statements
- **Miss**: Number of statements not executed
- **Cover**: Percentage of statements covered
- **Missing**: Line numbers not covered

### HTML Reports
```bash
# Generate HTML report
uv run pytest --cov=chuk_term --cov-report=html

# Using Makefile
make test

# Open report (macOS)
open htmlcov/index.html

# Open report (Linux)
xdg-open htmlcov/index.html

# Open report (Windows)
start htmlcov/index.html

# Report location: htmlcov/index.html
```

HTML reports provide:
- Interactive line-by-line coverage visualization
- Sortable module list
- Coverage trends over time
- Branch coverage details

## Coverage Types

### Line Coverage
Basic metric showing which lines were executed:
```python
def calculate(x, y):
    result = x + y  # ✓ Covered
    if result > 100:
        return 100  # ✗ Not covered if result ≤ 100
    return result   # ✓ Covered
```

### Branch Coverage
Ensures all code paths are tested:
```python
def process(value):
    if value > 0:      # Need tests for both True and False
        return "positive"
    elif value < 0:    # Need tests for both True and False
        return "negative"
    else:
        return "zero"
```

### Statement Coverage vs Functional Coverage
```python
# High statement coverage but poor functional coverage
async def divide(a, b):
    # Test might cover the line but miss edge cases
    return a / b  # ✓ Line covered, but did we test b=0?
```

## Best Practices

### 1. Focus on Meaningful Coverage
```python
# Good: Test actual functionality
def test_output_theme_adaptation():
    """Test output adapts to theme changes."""
    from chuk_term.ui.output import get_output
    from chuk_term.ui.theme import set_theme
    
    output = get_output()
    
    # Test with different themes
    for theme in ["default", "minimal", "terminal"]:
        set_theme(theme)
        # Verify output behavior changes appropriately
        # Not just that the code runs
```

### 2. Don't Chase 100% Coverage Blindly
```python
# Not worth testing
if __name__ == "__main__":
    # Demo code - low priority for coverage
    demo()

# Platform-specific code
if sys.platform == "win32":
    # Only test on relevant platform
    windows_specific_function()
```

### 3. Prioritize Critical Paths
```python
# High priority - core output management
class Output:
    """Critical singleton - aim for 95%+ coverage."""
    def info(self, message: str):
        # Every output method should be tested
    
# Lower priority - simple utilities
def format_timestamp(dt: datetime):
    """Simple formatting - basic test sufficient."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")
```

### 4. Use Coverage to Find Gaps
```bash
# Identify untested modules
uv run pytest --cov=chuk_term --cov-report=term-missing | grep "0%"

# Find partially tested modules  
uv run pytest --cov=chuk_term --cov-report=term-missing | grep -E "[0-9]{1,2}%"

# Using Makefile
make test | grep "0%"  # Find untested modules
```

## Improving Coverage

### Step-by-Step Approach

1. **Measure Baseline**
   ```bash
   uv run pytest --cov=chuk_term --cov-report=term > coverage_baseline.txt
   
   # Or using Makefile
   make test > coverage_baseline.txt
   ```

2. **Identify Gaps**
   - Sort by coverage percentage
   - Focus on critical modules first
   - Look for easy wins (simple functions)

3. **Write Targeted Tests**
   ```python
   # Use coverage report to identify missing lines
   # Missing: lines 45-52 (error handling)
   @pytest.mark.asyncio
   async def test_error_conditions():
       """Target uncovered error paths."""
       with pytest.raises(ValueError):
           await function_that_needs_coverage(invalid_input)
   ```

4. **Verify Improvement**
   ```bash
   # Run coverage again and compare
   uv run pytest --cov=chuk_term --cov-report=term
   
   # Or using Makefile
   make test
   ```

## Coverage in CI/CD

### GitHub Actions
For GitHub Actions workflow configuration, see:
- **Template**: [github-actions-coverage.yaml](https://github.com/chrishayuk/vibe-coding-templates/blob/main/python/templates/cicd/workflows/github-actions-coverage.yaml)
- **Local Implementation**: [github-actions-coverage.yaml](../../templates/cicd/workflows/github-actions-coverage.yaml)

The workflow includes coverage reporting, Codecov integration, and artifact uploading.

### Pre-commit Hooks
For pre-commit hook configuration, see:
- **Template**: [pre-commit-coverage-hook.yaml](https://github.com/chrishayuk/vibe-coding-templates/blob/main/python/templates/cicd/hooks/pre-commit-coverage-hook.yaml)
- **Local Implementation**: [pre-commit-coverage-hook.yaml](../../templates/cicd/hooks/pre-commit-coverage-hook.yaml)

Quick setup:
```bash
# Install pre-commit
uv add --dev pre-commit

# Add hooks to .pre-commit-config.yaml from template

# Install hooks
pre-commit install

# Run coverage check
pre-commit run test-coverage --all-files
```

## Common Coverage Patterns

### UI Component Coverage
```python
def test_theme_switching():
    """Ensure theme switching is properly covered."""
    from chuk_term.ui.theme import set_theme, get_theme
    
    # Test all themes
    themes = ["default", "dark", "light", "minimal", 
              "terminal", "monokai", "dracula", "solarized"]
    
    for theme_name in themes:
        set_theme(theme_name)
        theme = get_theme()
        assert theme.name == theme_name
```

### Error Path Coverage
```python
def test_terminal_error_paths():
    """Cover terminal operation error conditions."""
    from chuk_term.ui.terminal import TerminalManager
    import subprocess
    
    # Mock subprocess to simulate errors
    def mock_run_error(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "cmd")
    
    # Test error handling for clear screen
    with patch('subprocess.run', mock_run_error):
        # Should handle error gracefully
        TerminalManager.clear()
```

### Branch Coverage  
```python
@pytest.mark.parametrize("quiet,verbose,shows_debug", [
    (False, False, False),  # Normal mode
    (True, False, False),   # Quiet mode
    (False, True, True),    # Verbose mode
])
def test_output_modes(quiet, verbose, shows_debug, capsys):
    """Ensure all output modes are covered."""
    from chuk_term.ui.output import get_output
    
    output = get_output()
    output.set_output_mode(quiet=quiet, verbose=verbose)
    
    output.debug("Debug message")
    captured = capsys.readouterr()
    
    if shows_debug:
        assert "Debug" in captured.out
    else:
        assert "Debug" not in captured.out
```

## Troubleshooting

### Coverage Not Detected
```bash
# Ensure test discovery is working
uv run pytest --collect-only

# Check source path is correct
uv run pytest --cov=chuk_term --cov-report=term

# Verify __init__.py files exist
find src/chuk_term -name "*.py" -type f | head
```

### Inconsistent Coverage
```bash
# Clear coverage cache
rm -rf .coverage .pytest_cache htmlcov/

# Run with fresh environment
uv run pytest --cov=chuk_term --no-cov-on-fail
```

### Missing Async Coverage
```python
# Ensure pytest-asyncio is installed
uv add --dev pytest-asyncio

# Use proper async test marking
@pytest.mark.asyncio  # Required for async tests
async def test_async():
    result = await async_function()
```

## Coverage Badges

Add coverage badges to README:
```markdown
![Coverage](https://img.shields.io/badge/coverage-83%25-green)
![Tests](https://img.shields.io/badge/tests-156%20passed-green)
```

Or with dynamic coverage:
```markdown
[![codecov](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/username/repo)
```

## Related Documentation

- [Unit Testing](./UNIT_TESTING.md) - General unit testing practices
- [Package Management](../PACKAGE_MANAGEMENT.md) - Using uv for dependencies
- [UI Themes](../ui/themes.md) - Testing UI components across themes
- [Project README](../../README.md) - Project overview

## Current Coverage Status

### Overall Coverage: 71%

**High Coverage Modules (>95%)**:
- `cli.py`: 100% ✅
- `ui/theme.py`: 98% ✅
- `ui/terminal.py`: 97% ✅
- `__init__.py` files: 100% ✅

**Needs Improvement (<80%)**:
- `ui/output.py`: 62% ⚠️
- `ui/prompts.py`: 79% ⚠️
- `ui/formatters.py`: 73% ⚠️
- `ui/code.py`: 72% ⚠️
- `ui/banners.py`: 20% ⚠️

## Next Steps

1. **Priority 1**: Improve `ui/output.py` coverage to 90%
   - Add tests for all output levels
   - Test quiet/verbose modes
   - Test theme adaptation

2. **Priority 2**: Improve CLI coverage to 95%
   - Test all command options
   - Test error handling
   - Test help output

3. **Priority 3**: Complete UI component tests
   - Finish prompt tests
   - Add code display tests
   - Add formatter tests