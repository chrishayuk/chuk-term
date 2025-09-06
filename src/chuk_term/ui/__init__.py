"""
User Interface components.

This package provides all UI-related functionality organized into focused modules:
- output: Centralized console output management
- terminal: Terminal state and cleanup
- banners: Welcome banners and headers
- prompts: User input and interaction
- formatters: Content formatting utilities
- code: Code display and syntax highlighting
"""

# Core output management (most commonly used)
# Banner displays
from chuk_term.ui.banners import (
    display_chat_banner,
    display_diagnostic_banner,
    display_error_banner,
    display_interactive_banner,
    display_session_banner,
    display_success_banner,
    display_welcome_banner,  # Legacy compatibility
)

# Code display and formatting
from chuk_term.ui.code import (
    display_code,
    display_code_analysis,
    display_code_review,
    display_diff,
    display_file_tree,
    display_side_by_side,
    format_code_snippet,
)

# Content formatters
from chuk_term.ui.formatters import (
    format_diff,
    format_error,
    format_json,
    format_table,
    format_timestamp,
    format_tool_call,
    format_tool_result,
    format_tree,
)
from chuk_term.ui.output import (
    Output,
    clear,
    command,
    debug,
    error,
    fatal,
    get_output,
    hint,
    info,
    # Direct convenience functions
    print,
    rule,
    status,
    success,
    tip,
    warning,
)

# User prompts and interaction
from chuk_term.ui.prompts import (
    ask,
    ask_number,
    confirm,
    create_menu,
    prompt_for_retry,
    prompt_for_tool_confirmation,
    select_from_list,
    select_multiple,
)

# Streaming support
from chuk_term.ui.streaming import (
    StreamingAssistant,
    StreamingMessage,
)

# Terminal management
from chuk_term.ui.terminal import (
    TerminalManager,
    clear_screen,
    get_terminal_size,
    reset_terminal,
    restore_terminal,
    set_terminal_title,
)

# Singleton output instance for convenient import
output = get_output()

__all__ = [
    # Output management
    "Output",
    "output",
    "get_output",
    "print",
    "debug",
    "info",
    "success",
    "warning",
    "error",
    "fatal",
    "tip",
    "hint",
    "status",
    "command",
    "clear",
    "rule",
    # Terminal
    "TerminalManager",
    "clear_screen",
    "restore_terminal",
    "reset_terminal",
    "get_terminal_size",
    "set_terminal_title",
    # Banners
    "display_chat_banner",
    "display_interactive_banner",
    "display_diagnostic_banner",
    "display_session_banner",
    "display_error_banner",
    "display_success_banner",
    "display_welcome_banner",
    # Prompts
    "ask",
    "confirm",
    "ask_number",
    "select_from_list",
    "select_multiple",
    "prompt_for_tool_confirmation",
    "prompt_for_retry",
    "create_menu",
    # Formatters
    "format_tool_call",
    "format_tool_result",
    "format_error",
    "format_json",
    "format_table",
    "format_tree",
    "format_timestamp",
    "format_diff",
    # Code display
    "display_code",
    "display_diff",
    "display_code_review",
    "display_code_analysis",
    "display_side_by_side",
    "display_file_tree",
    "format_code_snippet",
    # Streaming
    "StreamingMessage",
    "StreamingAssistant",
]
