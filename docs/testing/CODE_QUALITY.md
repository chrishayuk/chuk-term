# Code Quality Standards

## Overview
This document outlines the code quality standards and tools used in the ChukTerm project. We use automated tools to ensure consistent code style, catch potential bugs, and maintain high code quality across the codebase.

## Tools and Configuration

### 1. Ruff - Fast Python Linter
**Purpose**: Catches code quality issues, potential bugs, and enforces Python best practices.

**Configuration**: `pyproject.toml`
```toml
[tool.ruff]
line-length = 120
target-version = "py310"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "B",    # flake8-bugbear
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "ARG",  # flake8-unused-arguments
    "SIM",  # flake8-simplify
]
ignore = []
```

### 2. Black - Code Formatter
**Purpose**: Automatically formats Python code to ensure consistent style.

**Configuration**: `pyproject.toml`
```toml
[tool.black]
line-length = 120
target-version = ['py310']
```

### 3. MyPy - Type Checker
**Purpose**: Static type checking for Python code to catch type-related bugs before runtime.

**Configuration**: `pyproject.toml`
```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
no_implicit_reexport = true
disallow_untyped_defs = false  # Relaxed for gradual typing
disallow_any_unimported = false
check_untyped_defs = true
strict_equality = true
warn_redundant_casts = true
warn_unused_ignores = false
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "tests.*"
ignore_errors = true

[[tool.mypy.overrides]]
module = "chuk_term.ui.*"
disallow_untyped_defs = false  # UI modules use gradual typing
```

## Running Code Quality Checks

### Quick Commands

```bash
# Check all code quality issues
uv run ruff check src/ tests/

# Auto-fix safe issues
uv run ruff check --fix src/ tests/

# Auto-fix including unsafe fixes (review changes!)
uv run ruff check --fix --unsafe-fixes src/ tests/

# Check formatting
uv run black --check src/ tests/

# Format code
uv run black src/ tests/

# Type checking
uv run mypy src/

# Run all quality checks at once
make check
# Or manually:
uv run ruff check src/ tests/ && \
uv run black --check src/ tests/ && \
uv run mypy src/ && \
uv run pytest
```

### Pre-commit Hooks
For automatic checking before commits:

```bash
# Install pre-commit
uv add --dev pre-commit

# Install hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

## Common Issues and Solutions

### MyPy Errors

#### Missing Type Annotations
```python
# Error: Function is missing a return type annotation
def process(data):
    return data * 2

# Fix: Add type hints
def process(data: int) -> int:
    return data * 2

# Or suppress if intentional
def process(data):  # type: ignore[no-untyped-def]
    return data * 2
```

#### Incompatible Types
```python
# Error: Incompatible return value type
def get_value() -> str:
    return None  # Error!

# Fix: Use Optional
from typing import Optional

def get_value() -> Optional[str]:
    return None

# Or use union syntax (Python 3.10+)
def get_value() -> str | None:
    return None
```

#### Type Ignore Comments
```python
# Ignore specific error
result = complex_function()  # type: ignore[return-value]

# Ignore all errors on a line (use sparingly!)
result = complex_function()  # type: ignore
```

### Ruff Errors

#### F401 - Unused Import
```python
# Bad
import os  # F401: unused import

# Good - remove unused import or use it
import os
print(os.getcwd())

# Or if needed for re-export
import os  # noqa: F401
```

#### ARG001/ARG002 - Unused Function/Method Arguments
```python
# Bad
def process(data, unused_param):  # ARG001
    return data

# Good - use underscore prefix
def process(data, _unused_param):
    return data

# Or add noqa for legitimate cases (e.g., test mocks)
def test_method(self, mock_input):  # noqa: ARG002
    assert something
```

#### SIM117 - Combine Multiple Context Managers
```python
# Bad
with open('file1') as f1:
    with open('file2') as f2:
        process(f1, f2)

# Good
with (
    open('file1') as f1,
    open('file2') as f2
):
    process(f1, f2)
```

#### B007 - Unused Loop Variable
```python
# Bad
for i in range(10):
    print("hello")

# Good
for _ in range(10):
    print("hello")
```

#### W293 - Blank Line Contains Whitespace
```python
# Bad
def function():
    """Docstring."""
    ····  # Whitespace on blank line
    return None

# Good
def function():
    """Docstring."""
    # No whitespace on blank line
    return None
```

### Black Formatting

Black is opinionated and will automatically format your code. Common changes include:

- **String quotes**: Prefers double quotes
- **Line breaks**: Adds/removes based on line length
- **Trailing commas**: Adds in multi-line structures
- **Parentheses**: Adds for clarity in complex expressions

```python
# Before Black
x = {'a':1,'b':2,'c':3}
very_long_function_name(argument1,argument2,argument3,argument4)

# After Black
x = {"a": 1, "b": 2, "c": 3}
very_long_function_name(
    argument1,
    argument2,
    argument3,
    argument4,
)
```

## Code Quality Standards

### Line Length
- Maximum: 120 characters
- Exceptions: URLs, long strings with no natural break points

### Imports
- Grouped and sorted automatically by Ruff
- Order: standard library, third-party, local
- One import per line for clarity

### Type Hints
- Required for all public functions
- Encouraged for complex internal functions
- Use modern syntax (e.g., `list[str]` not `List[str]`)

```python
# Good
def process_items(items: list[str], count: int) -> dict[str, int]:
    """Process items and return counts."""
    return {item: count for item in items}
```

### Docstrings
- Required for all public modules, classes, and functions
- Use Google or NumPy style consistently
- Include Args, Returns, Raises sections when applicable

```python
def calculate_average(numbers: list[float], weights: list[float] | None = None) -> float:
    """
    Calculate weighted average of numbers.
    
    Args:
        numbers: List of numbers to average
        weights: Optional weights for each number
        
    Returns:
        Weighted average of the numbers
        
    Raises:
        ValueError: If weights don't match numbers length
    """
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install uv
          uv sync --dev
      
      - name: Run Ruff
        run: uv run ruff check src/ tests/
      
      - name: Check Black formatting
        run: uv run black --check src/ tests/
      
      - name: Run MyPy
        run: uv run mypy src/
```

## Suppressing Warnings

Sometimes you need to suppress warnings for legitimate reasons:

### File-level Suppression
```python
# ruff: noqa: ARG002  # Suppress unused argument warnings for entire file
```

### Line-level Suppression
```python
import unused_module  # noqa: F401  # Needed for side effects
```

### Block-level Suppression (Ruff)
```python
# fmt: off
complex_matrix = [
    [1,  2,  3],
    [4,  5,  6],
    [7,  8,  9],
]
# fmt: on
```

## Best Practices

1. **Run checks before committing**: Use pre-commit hooks or run manually
2. **Fix issues immediately**: Don't let quality issues accumulate
3. **Review auto-fixes**: Always review changes made by `--fix` flags
4. **Keep tools updated**: Regular updates via `uv lock --upgrade`
5. **Document exceptions**: If suppressing a warning, add a comment explaining why
6. **Consistent configuration**: Share config via `pyproject.toml`

## Metrics and Goals

### Current Status
- ✅ All files pass Ruff checks
- ✅ All files formatted with Black
- ✅ MyPy type checking passes (with gradual typing)

### Quality Goals
- Zero Ruff errors in production code
- 100% Black formatted
- No suppressed warnings without documentation
- Type hints for all public APIs
- Docstrings for all public functions

## Troubleshooting

### Common Problems

**Problem**: Ruff and Black disagree on formatting
**Solution**: Black takes precedence for formatting; Ruff for linting

**Problem**: Too many errors to fix manually
**Solution**: Use `ruff check --fix --unsafe-fixes` carefully, review all changes

**Problem**: CI fails but local passes
**Solution**: Ensure same tool versions; run `uv lock --upgrade`

**Problem**: Import order keeps changing
**Solution**: Let Ruff handle imports with isort rules

## Resources

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Documentation](https://black.readthedocs.io/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## Conclusion

Maintaining high code quality is essential for the ChukTerm project. These tools and standards help us:
- Write more maintainable code
- Catch bugs early
- Ensure consistency across contributors
- Reduce code review time
- Improve overall code reliability

Remember: **Clean code is a team effort!** 🚀