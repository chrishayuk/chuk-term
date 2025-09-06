"""
Tests for the banners module.
"""

from unittest.mock import patch

from chuk_term.ui.banners import (
    BannerStyle,
    display_chat_banner,
    display_diagnostic_banner,
    display_error_banner,
    display_interactive_banner,
    display_session_banner,
    display_success_banner,
    display_welcome_banner,
)
from chuk_term.ui.output import get_output
from chuk_term.ui.theme import set_theme


class TestBannerStyles:
    """Test BannerStyle configurations."""

    def test_banner_styles_exist(self):
        """Test that all expected banner styles are defined."""
        assert hasattr(BannerStyle, "CHAT")
        assert hasattr(BannerStyle, "INTERACTIVE")
        assert hasattr(BannerStyle, "DIAGNOSTIC")
        assert hasattr(BannerStyle, "ERROR")
        assert hasattr(BannerStyle, "SUCCESS")

    def test_banner_style_structure(self):
        """Test banner style data structure."""
        assert "title" in BannerStyle.CHAT
        assert "style" in BannerStyle.CHAT
        assert "icon" in BannerStyle.CHAT


class TestChatBanner:
    """Test chat banner display."""

    def test_display_chat_banner_default_theme(self):
        """Test chat banner with default theme."""
        set_theme("default")
        output = get_output()

        with patch.object(output, "panel") as mock_panel:
            display_chat_banner("OpenAI", "gpt-4")

            mock_panel.assert_called_once()
            args, kwargs = mock_panel.call_args
            assert "title" in kwargs
            assert kwargs["style"] == "yellow"

    def test_display_chat_banner_with_info(self):
        """Test chat banner with additional info."""
        output = get_output()

        with patch.object(output, "panel") as mock_panel:
            display_chat_banner("OpenAI", "gpt-4", additional_info={"Temperature": "0.7", "Max Tokens": "1000"})

            mock_panel.assert_called_once()

    def test_display_chat_banner_minimal_theme(self):
        """Test chat banner with minimal theme."""
        set_theme("minimal")
        output = get_output()

        with patch.object(output, "print") as mock_print:
            display_chat_banner("OpenAI", "gpt-4")

            mock_print.assert_called()
            calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("Chat Mode" in call for call in calls)
            assert any("OpenAI/gpt-4" in call for call in calls)

        set_theme("default")  # Reset

    def test_display_chat_banner_terminal_theme(self):
        """Test chat banner with terminal theme."""
        set_theme("terminal")
        output = get_output()

        with patch.object(output, "print") as mock_print:
            display_chat_banner("OpenAI", "gpt-4", {"Temp": "0.5"})

            mock_print.assert_called()
            calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("CHAT MODE" in call for call in calls)
            assert any("Temp: 0.5" in call for call in calls)

        set_theme("default")  # Reset

    def test_display_chat_banner_terminal_no_info(self):
        """Test chat banner terminal theme without additional info."""
        set_theme("terminal")
        output = get_output()

        with patch.object(output, "print") as mock_print:
            display_chat_banner("Claude", "claude-3")

            mock_print.assert_called()
            calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("[CHAT MODE]" in call for call in calls)
            assert any("Provider: Claude | Model: claude-3" in call for call in calls)
            assert any("Type 'exit' to quit" in call for call in calls)

        set_theme("default")  # Reset


class TestInteractiveBanner:
    """Test interactive banner display."""

    def test_display_interactive_banner_basic(self):
        """Test basic interactive banner."""
        output = get_output()

        with patch.object(output, "panel") as mock_panel:
            display_interactive_banner("OpenAI", "gpt-4")

            mock_panel.assert_called_once()
            assert mock_panel.call_args[1]["style"] == "cyan"

    def test_display_interactive_banner_with_counts(self):
        """Test interactive banner with tool and server counts."""
        output = get_output()

        with patch.object(output, "panel") as mock_panel:
            display_interactive_banner("OpenAI", "gpt-4", tool_count=10, server_count=2)

            mock_panel.assert_called_once()

    def test_display_interactive_banner_minimal(self):
        """Test interactive banner in minimal theme."""
        set_theme("minimal")
        output = get_output()

        with patch.object(output, "print") as mock_print:
            display_interactive_banner("OpenAI", "gpt-4", tool_count=5)

            calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("Interactive Mode" in call for call in calls)
            assert any("Tools: 5" in call for call in calls)

        set_theme("default")  # Reset

    def test_display_interactive_banner_terminal(self):
        """Test interactive banner in terminal theme."""
        set_theme("terminal")
        output = get_output()

        with patch.object(output, "print") as mock_print:
            display_interactive_banner("Claude", "claude-3", tool_count=10, server_count=3)

            calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("[INTERACTIVE MODE]" in call for call in calls)
            assert any("Provider: Claude | Model: claude-3" in call for call in calls)
            assert any("Tools: 10 | Servers: 3" in call for call in calls)
            assert any("Type 'help' for commands" in call for call in calls)

        set_theme("default")  # Reset

    def test_display_interactive_banner_terminal_no_tools(self):
        """Test interactive banner terminal theme without tools/servers."""
        set_theme("terminal")
        output = get_output()

        with patch.object(output, "print") as mock_print:
            display_interactive_banner("Anthropic", "claude-2")

            calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("[INTERACTIVE MODE]" in call for call in calls)
            assert any("Provider: Anthropic | Model: claude-2" in call for call in calls)
            # Should not have Tools or Servers in output
            assert not any("Tools:" in call for call in calls)
            assert not any("Servers:" in call for call in calls)

        set_theme("default")  # Reset


class TestDiagnosticBanner:
    """Test diagnostic banner display."""

    def test_display_diagnostic_banner_basic(self):
        """Test basic diagnostic banner."""
        output = get_output()

        with patch.object(output, "panel") as mock_panel:
            display_diagnostic_banner("Connection Test", "Testing API connection")

            mock_panel.assert_called_once()
            assert mock_panel.call_args[1]["style"] == "magenta"

    def test_display_diagnostic_banner_with_params(self):
        """Test diagnostic banner with parameters."""
        output = get_output()

        with patch.object(output, "panel") as mock_panel:
            display_diagnostic_banner(
                "Performance Test", "Testing system performance", parameters={"Iterations": 100, "Timeout": "30s"}
            )

            mock_panel.assert_called_once()

    def test_display_diagnostic_banner_minimal(self):
        """Test diagnostic banner in minimal theme."""
        set_theme("minimal")
        output = get_output()

        with patch.object(output, "print") as mock_print:
            display_diagnostic_banner("Test Name", "Test Description", {"param1": "value1"})

            calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("Diagnostic: Test Name" in call for call in calls)
            assert any("Test Description" in call for call in calls)
            assert any("Parameters: param1=value1" in call for call in calls)

        set_theme("default")  # Reset

    def test_display_diagnostic_banner_terminal(self):
        """Test diagnostic banner in terminal theme."""
        set_theme("terminal")
        output = get_output()

        with patch.object(output, "print") as mock_print:
            display_diagnostic_banner("Network Test", "Testing connectivity", {"timeout": "30s", "retries": "3"})

            calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("[DIAGNOSTIC]" in call for call in calls)
            assert any("Test: Network Test" in call for call in calls)
            assert any("Description: Testing connectivity" in call for call in calls)
            assert any("Parameters: timeout=30s, retries=3" in call for call in calls)

        set_theme("default")  # Reset

    def test_display_diagnostic_banner_terminal_no_params(self):
        """Test diagnostic banner terminal theme without parameters."""
        set_theme("terminal")
        output = get_output()

        with patch.object(output, "print") as mock_print:
            display_diagnostic_banner("Simple Test", "Basic diagnostic")

            calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("[DIAGNOSTIC]" in call for call in calls)
            assert any("Test: Simple Test" in call for call in calls)
            assert any("Description: Basic diagnostic" in call for call in calls)
            # Should not have Parameters in output
            assert not any("Parameters:" in call for call in calls)

        set_theme("default")  # Reset


class TestSessionBanner:
    """Test session banner display."""

    def test_display_session_banner_basic(self):
        """Test basic session banner."""
        output = get_output()

        with patch.object(output, "panel") as mock_panel:
            display_session_banner("Session Info", {"User": "test_user", "Duration": "5m"})

            mock_panel.assert_called_once()
            assert mock_panel.call_args[1]["style"] == "cyan"

    def test_display_session_banner_custom_style(self):
        """Test session banner with custom style."""
        output = get_output()

        with patch.object(output, "panel") as mock_panel:
            display_session_banner("Custom Session", {"ID": "123"}, style_name="green")

            mock_panel.assert_called_once()
            assert mock_panel.call_args[1]["style"] == "green"

    def test_display_session_banner_minimal(self):
        """Test session banner in minimal theme."""
        set_theme("minimal")
        output = get_output()

        with patch.object(output, "print") as mock_print:
            display_session_banner("Session", {"Key1": "Value1", "Key2": "Value2"})

            calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("Session" in call for call in calls)
            assert any("Key1: Value1" in call for call in calls)
            assert any("Key2: Value2" in call for call in calls)

        set_theme("default")  # Reset

    def test_display_session_banner_terminal(self):
        """Test session banner in terminal theme."""
        set_theme("terminal")
        output = get_output()

        with patch.object(output, "print") as mock_print:
            display_session_banner("Debug Session", {"PID": "12345", "Memory": "256MB"})

            calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("[DEBUG SESSION]" in call for call in calls)
            assert any("PID: 12345" in call for call in calls)
            assert any("Memory: 256MB" in call for call in calls)

        set_theme("default")  # Reset


class TestErrorBanner:
    """Test error banner display."""

    def test_display_error_banner_basic(self):
        """Test basic error banner."""
        output = get_output()
        error = ValueError("Test error")

        with patch.object(output, "panel") as mock_panel:
            display_error_banner(error)

            mock_panel.assert_called_once()
            assert mock_panel.call_args[1]["style"] == "red"

    def test_display_error_banner_with_context(self):
        """Test error banner with context."""
        output = get_output()
        error = RuntimeError("Something failed")

        with patch.object(output, "panel") as mock_panel:
            display_error_banner(
                error, context="While processing request", suggestions=["Check input", "Retry operation"]
            )

            mock_panel.assert_called_once()

    def test_display_error_banner_minimal(self):
        """Test error banner in minimal theme."""
        set_theme("minimal")
        output = get_output()
        error = Exception("Test error")

        with patch.object(output, "error") as mock_error, patch.object(output, "print") as mock_print:
            display_error_banner(error, context="Test context", suggestions=["Fix 1", "Fix 2"])

            mock_error.assert_called_once_with("ERROR: Test error")
            # Check that context and suggestions were printed
            print_calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("Context: Test context" in call for call in print_calls)
            assert any("Suggestions:" in call for call in print_calls)
            assert any("1. Fix 1" in call for call in print_calls)
            assert any("2. Fix 2" in call for call in print_calls)

        set_theme("default")  # Reset

    def test_display_error_banner_terminal(self):
        """Test error banner in terminal theme."""
        set_theme("terminal")
        output = get_output()
        error = RuntimeError("Connection failed")

        with patch.object(output, "error") as mock_error, patch.object(output, "print") as mock_print:
            display_error_banner(error, context="During API call", suggestions=["Check network", "Retry"])

            mock_error.assert_called_once_with("Connection failed")
            print_calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("[yellow]Context:[/] During API call" in call for call in print_calls)
            assert any("[cyan]Suggestions:[/]" in call for call in print_calls)
            assert any("1. Check network" in call for call in print_calls)
            assert any("2. Retry" in call for call in print_calls)

        set_theme("default")  # Reset


class TestSuccessBanner:
    """Test success banner display."""

    def test_display_success_banner_basic(self):
        """Test basic success banner."""
        output = get_output()

        with patch.object(output, "panel") as mock_panel:
            display_success_banner("Operation completed successfully")

            mock_panel.assert_called_once()
            assert mock_panel.call_args[1]["style"] == "green"

    def test_display_success_banner_with_details(self):
        """Test success banner with details."""
        output = get_output()

        with patch.object(output, "panel") as mock_panel:
            display_success_banner("All tests passed", details={"Tests": 100, "Time": "2.5s"})

            mock_panel.assert_called_once()

    def test_display_success_banner_minimal(self):
        """Test success banner in minimal theme."""
        set_theme("minimal")
        output = get_output()

        with patch.object(output, "success") as mock_success, patch.object(output, "print") as mock_print:
            display_success_banner("Success!", details={"Count": "10", "Time": "1.5s"})

            mock_success.assert_called_once_with("SUCCESS: Success!")
            # Check details were printed
            print_calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("Count: 10" in call for call in print_calls)
            assert any("Time: 1.5s" in call for call in print_calls)

        set_theme("default")  # Reset

    def test_display_success_banner_terminal(self):
        """Test success banner in terminal theme."""
        set_theme("terminal")
        output = get_output()

        with patch.object(output, "success") as mock_success, patch.object(output, "print") as mock_print:
            display_success_banner("All tests passed", details={"Total": "100", "Duration": "5s"})

            mock_success.assert_called_once_with("All tests passed")
            print_calls = [str(call[0][0]) for call in mock_print.call_args_list]
            assert any("Total: 100" in call for call in print_calls)
            assert any("Duration: 5s" in call for call in print_calls)

        set_theme("default")  # Reset


class TestWelcomeBanner:
    """Test welcome banner display."""

    def test_display_welcome_banner(self):
        """Test welcome banner."""
        get_output()
        ctx = {"provider": "OpenAI", "model": "gpt-4", "mode": "chat"}

        # Should delegate to appropriate banner based on mode
        with patch("chuk_term.ui.banners.display_chat_banner") as mock_chat:
            display_welcome_banner(ctx)
            mock_chat.assert_called_once()

    def test_display_welcome_banner_interactive_mode(self):
        """Test welcome banner for interactive mode."""
        ctx = {"provider": "OpenAI", "model": "gpt-4", "mode": "interactive", "tool_count": 5}

        with patch("chuk_term.ui.banners.display_interactive_banner") as mock_interactive:
            display_welcome_banner(ctx)
            mock_interactive.assert_called_once()

    def test_display_welcome_banner_diagnostic_mode(self):
        """Test welcome banner for diagnostic mode."""
        ctx = {"mode": "diagnostic", "test_name": "Test", "description": "Description"}

        with patch("chuk_term.ui.banners.display_diagnostic_banner") as mock_diagnostic:
            display_welcome_banner(ctx)
            mock_diagnostic.assert_called_once()


class TestBannerIntegration:
    """Integration tests for banner functionality."""

    def test_all_themes_chat_banner(self):
        """Test chat banner works with all themes."""
        themes = ["default", "minimal", "terminal", "dark", "light"]

        for theme_name in themes:
            set_theme(theme_name)
            # Should not raise any errors
            display_chat_banner("Provider", "Model")

        set_theme("default")  # Reset

    def test_all_themes_error_banner(self):
        """Test error banner works with all themes."""
        themes = ["default", "minimal", "terminal"]
        error = Exception("Test")

        for theme_name in themes:
            set_theme(theme_name)
            # Should not raise any errors
            display_error_banner(error)

        set_theme("default")  # Reset

    def test_unicode_in_banners(self):
        """Test banners handle Unicode content."""
        display_chat_banner("Provider 🚀", "Model émoji")
        display_success_banner("Success ✨ 完成")
        display_error_banner(Exception("Error ñoño 🚨"))

    def test_empty_data_in_banners(self):
        """Test banners handle empty data gracefully."""
        display_chat_banner("", "", {})
        display_interactive_banner("", "")
        display_diagnostic_banner("", "", {})
        display_session_banner("", {})
        display_error_banner(Exception(""))
        display_success_banner("", {})

    def test_long_content_in_banners(self):
        """Test banners handle long content."""
        long_text = "x" * 1000
        display_chat_banner(long_text, long_text)
        display_success_banner(long_text)
        display_error_banner(Exception(long_text))
