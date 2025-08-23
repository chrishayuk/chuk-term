# Package Management with uv

## Overview

ChukTerm uses `uv` as the primary package manager for Python dependencies. `uv` is a fast, reliable Python package and project manager written in Rust that provides significant performance improvements over traditional Python package managers.

## Why uv?

- **Speed**: 10-100x faster than pip and pip-tools
- **Reliability**: Built-in resolver prevents dependency conflicts
- **Simplicity**: Single tool for package and project management
- **Compatibility**: Drop-in replacement for pip commands
- **Lock files**: Automatic dependency locking for reproducible builds

## Installation

### Install uv
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Using pip (fallback)
pip install uv

# Verify installation
uv --version
```

## Basic Usage

### Installing Dependencies

```bash
# Install project with all dependencies
uv sync

# Install including dev dependencies (recommended for ChukTerm development)
uv sync --dev

# Install specific package
uv add package-name

# Install dev dependency
uv add --dev pytest-cov

# Install from requirements file
uv pip install -r requirements.txt
```

### Running Commands

```bash
# Run command in project environment
uv run python script.py

# Run pytest
uv run pytest

# Run with coverage for ChukTerm
uv run pytest --cov=chuk_term

# Run any command
uv run make test

# Run ChukTerm CLI
uv run chuk-term info
uv run chuk-term demo

# Run example scripts
uv run python examples/ui_demo.py
```

### Managing Dependencies

```bash
# Add a new dependency
uv add numpy

# Add dev dependency
uv add --dev pytest-benchmark

# Remove dependency
uv remove package-name

# Update dependencies
uv sync --upgrade

# Show installed packages
uv pip list
```

## Project Configuration

### pyproject.toml

ChukTerm uses `pyproject.toml` for dependency management:

```toml
[project]
name = "chuk-term"
requires-python = ">=3.10"
dependencies = [
    "click>=8.0.0",
    "rich>=13.0.0",
]

[dependency-groups]
dev = [
    "black>=25.1.0",
    "mypy>=1.17.1",
    "pytest>=8.4.1",
    "pytest-asyncio>=1.1.0",
    "pytest-cov>=6.2.1",
    "ruff>=0.12.10",
]
```

### Lock File

`uv.lock` ensures reproducible installations:
- Automatically generated and updated
- Should be committed to version control
- Ensures all developers use same dependency versions

## Common Commands Reference

### Development Workflow

```bash
# Initial setup
git clone https://github.com/yourusername/chuk-term.git
cd chuk-term
uv sync --dev

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=chuk_term

# Run linting
uv run ruff check src/ tests/

# Run type checking
uv run mypy src/

# Format code
uv run black src/ tests/

# Run all checks (using Makefile)
make check
```

### Package Management

```bash
# Add production dependency
uv add fastapi

# Add dev dependency
uv add --dev black

# Add with version constraint
uv add "pandas>=2.0.0"

# Remove package
uv remove pandas

# Update all dependencies
uv sync --upgrade

# Update specific package
uv add --upgrade numpy
```

### Environment Management

```bash
# Create virtual environment (automatic with uv sync)
uv venv

# Activate environment (usually not needed with uv run)
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Show environment info
uv pip list
uv pip show package-name
```

## Makefile Integration

ChukTerm's Makefile is configured to use uv:

```makefile
# Install dependencies
install:
	uv sync

# Install with dev dependencies
dev:
	uv sync --dev

# Run tests
test:
	uv run pytest --cov=chuk_term

# Run specific test file
test-file:
	uv run pytest tests/ui/test_output.py -v

# Linting
lint:
	uv run ruff check src/ tests/

# Format code
format:
	uv run black src/ tests/

# Type checking
typecheck:
	uv run mypy src/

# Run all checks
check: lint format typecheck test

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info htmlcov/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
```

## CI/CD Integration

### GitHub Actions

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Install uv
      uses: astral-sh/setup-uv@v3
      
    - name: Set up Python
      run: uv python install ${{ matrix.python-version }}
      
    - name: Install dependencies
      run: uv sync --dev
    
    - name: Run linting
      run: uv run ruff check src/ tests/
    
    - name: Run type checking
      run: uv run mypy src/
    
    - name: Run tests with coverage
      run: uv run pytest --cov=chuk_term --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## Migration from pip

### For Developers

Replace pip commands with uv equivalents:

| pip command | uv command |
|------------|------------|
| `pip install package` | `uv add package` |
| `pip install -e .` | `uv sync` |
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| `pip uninstall package` | `uv remove package` |
| `pip list` | `uv pip list` |
| `pip freeze` | `uv pip freeze` |
| `python script.py` | `uv run python script.py` |
| `pytest` | `uv run pytest` |

### For Scripts

Update automation scripts:

```bash
# Old (pip)
pip install -e ".[dev]"
pytest

# New (uv)
uv sync --dev
uv run pytest
```

## Troubleshooting

### Common Issues

**uv command not found**
```bash
# Reinstall uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"
```

**Dependency conflicts**
```bash
# Clear cache and reinstall
uv cache clean
rm -rf .venv uv.lock
uv sync --dev
```

**Wrong Python version**
```bash
# Specify Python version
uv venv --python 3.11
uv sync
```

**Import errors after install**
```bash
# Ensure using uv run
uv run python  # Not just 'python'
uv run pytest  # Not just 'pytest'
```

## Best Practices

### DO's
✅ Always use `uv run` to execute commands  
✅ Commit `uv.lock` to version control  
✅ Use `uv add` instead of editing pyproject.toml manually  
✅ Keep dev dependencies separate with `--dev` flag  
✅ Use `uv sync` after pulling changes  

### DON'Ts
❌ Don't use pip alongside uv in the same project  
❌ Don't manually activate venv when using `uv run`  
❌ Don't ignore uv.lock in git  
❌ Don't edit uv.lock manually  
❌ Don't mix pip and uv commands  

## Advanced Usage

### Custom Package Index
```bash
# Add custom index
uv add --index-url https://custom.pypi.org/simple/ package

# Use extra index
uv add --extra-index-url https://extra.pypi.org/simple/ package
```

### Platform-specific Dependencies
```toml
[tool.uv]
dependencies = [
    "windows-only-package ; sys_platform == 'win32'",
    "unix-only-package ; sys_platform != 'win32'",
]
```

### Workspace Management
```bash
# For monorepo with multiple packages
uv sync --workspace
```

## ChukTerm-Specific Commands

### Running the CLI

```bash
# Show library information
uv run chuk-term info
uv run chuk-term info --verbose

# Run interactive demo
uv run chuk-term demo

# Test with specific theme
uv run chuk-term test --theme monokai
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

# Quick test
uv run python examples/ui_quick_test.py
```

### Development Workflow

```bash
# Start development
uv sync --dev

# Make changes to code
# ...

# Run tests for changed module
uv run pytest tests/ui/test_output.py -v

# Check code quality
make check  # Runs lint, format, typecheck, and tests

# Generate coverage report
uv run pytest --cov=chuk_term --cov-report=html
open htmlcov/index.html  # View coverage in browser
```

## Publishing ChukTerm

### Build Package

```bash
# Build distribution files
uv build

# Check build artifacts
ls dist/
```

### Publish to PyPI

```bash
# Test on TestPyPI first
uv publish --repository testpypi

# Publish to PyPI
uv publish
```

## Related Documentation

- [uv Documentation](https://docs.astral.sh/uv/)
- [pyproject.toml Specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
- [Python Packaging Guide](https://packaging.python.org/)
- [ChukTerm README](../README.md)
- [ChukTerm Testing Guide](./testing/UNIT_TESTING.md)
- [ChukTerm Coverage Requirements](./testing/TEST_COVERAGE.md)