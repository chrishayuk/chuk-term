# Changelog

All notable changes to ChukTerm will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Updated pre-commit hooks to latest versions (ruff v0.12.10, black v25.1.0, mypy v1.17.1)
- Fixed package metadata URLs to use correct GitHub repository (chrishayuk/chuk-term)
- Updated Python version compatibility to 3.10+ across all configurations

### Added
- Documentation link in package metadata
- CONTRIBUTING.md with comprehensive contributor guidelines
- Enhanced progress bar features:
  - `progress_bar()` - Detailed progress bar with customizable columns
  - `track()` - Simple iterator tracking with progress display
  - `spinner()` - Spinner alias for better API consistency
- Additional Rich progress imports for better progress visualization
- New CLI commands:
  - `chuk-term themes` - Preview all themes with detailed or side-by-side view
  - `chuk-term examples` - List and run available examples
  - `get_available_themes()` function in theme.py
- Test coverage improvements:
  - Added 13 new tests for CLI commands (themes, examples)
  - Added 10 new tests for progress features (progress_bar, track, spinner)
  - Total test count: 519 (was 506)
  - Overall coverage: 89% (was 86%)

## [0.1.8] - 2025-12-07

### Added
- **`clear_lines(count)`** function for multi-line clearing
  - Clears N lines starting from current position
  - Returns cursor to first line after clearing
  - Properly handles line counting and cursor positioning
  - Essential for live-updating multi-line displays

- **ANSI Escape Code Support** in `Output.print()`
  - Automatically detects ANSI escape sequences (`\033[...`)
  - Writes them directly to stdout without escaping
  - Preserves terminal control codes for cursor movement, clearing, etc.
  - Critical for live-updating displays with multi-line content

### API
New functions in `chuk_term.ui.terminal`:
- `clear_lines(count: int)` - Clear multiple lines and return to first line
- Exposed `clear_line()` in public API
- Exposed `move_cursor_up(lines)` and `move_cursor_down(lines)` in public API

### Tests
- Added 9 comprehensive tests for ANSI escape code handling
  - Tests preservation of escape codes, clearing, cursor movement
  - Tests mixed ANSI and text content, flushing, custom end parameters
- Added 5 comprehensive tests for `clear_lines()` function
  - Tests cover single line, multiple lines, zero, negative, and Windows platform

### Use Case
Enables clean implementation of multi-line live status displays:
```python
from chuk_term.ui.terminal import clear_lines, move_cursor_up

# Update a 3-line display
clear_lines(3)
print("Line 1: Status")
print("Line 2: Progress")
print("Line 3: Details")
# Move cursor back to first line for next update
move_cursor_up(2)
print("\r", end="")
```

## [0.1.6] - Previous version
