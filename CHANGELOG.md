# Changelog

## [0.1.7] - 2025-12-07

### Added
- **`clear_lines(count)`** function for multi-line clearing
  - Clears N lines starting from current position
  - Returns cursor to first line after clearing
  - Properly handles line counting and cursor positioning
  - Essential for live-updating multi-line displays

### API
New functions in `chuk_term.ui.terminal`:
- `clear_lines(count: int)` - Clear multiple lines and return to first line
- Exposed `clear_line()` in public API
- Exposed `move_cursor_up(lines)` and `move_cursor_down(lines)` in public API

### Tests
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
