"""CLI interface for ChukTerm."""

import sys

import click

from chuk_term import __version__
from chuk_term.ui import (
    ask,
    confirm,
    display_chat_banner,
    display_code,
    display_interactive_banner,
    output,
    select_from_list,
)
from chuk_term.ui.theme import set_theme


@click.group()
@click.version_option(version=__version__, prog_name="chuk-term")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """ChukTerm - A powerful terminal library CLI."""
    ctx.ensure_object(dict)


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def info(verbose: bool) -> None:
    """Display information about ChukTerm."""
    output.info(f"ChukTerm version {__version__}")
    if verbose:
        output.print("\nFeatures:")
        output.print("  • Rich UI components for terminal applications")
        output.print("  • Theme support (monokai, dracula, solarized, etc.)")
        output.print("  • Code display with syntax highlighting")
        output.print("  • Interactive prompts and menus")
        output.print("  • Centralized output management")


@cli.command()
@click.argument("command", required=False)
@click.option("--config", "-c", type=click.Path(exists=True), help="Configuration file path")
def run(command: str | None, config: str | None) -> None:
    """Run a terminal command or start interactive mode."""
    if command:
        output.command(command)
        output.success(f"Command executed: {command}")
    else:
        display_interactive_banner("ChukTerm", "Terminal v1.0")
        output.warning("Interactive mode not yet implemented")
        output.hint("This is where your terminal functionality will go")

    if config:
        output.status(f"Using config: {config}")


@cli.command()
def demo() -> None:
    """Run an interactive demo of ChukTerm features."""
    display_chat_banner("ChukTerm", "Demo v1.0")

    name = ask("What's your name?")
    output.success(f"Hello, {name}!")

    if confirm("Would you like to see the available themes?"):
        themes = ["default", "dark", "light", "minimal", "terminal", "monokai", "dracula"]
        theme = select_from_list("Choose a theme:", themes)
        set_theme(theme)
        output.info(f"Theme changed to: {theme}")

    output.print("\n### Sample Code Display")
    code = """def hello_world():
    print("Hello from ChukTerm!")
    return True"""
    display_code(code, language="python", title="Example Code")

    output.print("\n### Output Examples")
    output.success("This is a success message")
    output.warning("This is a warning message")
    output.error("This is an error message")
    output.info("This is an info message")
    output.tip("This is a helpful tip")
    output.hint("This is a subtle hint")

    output.print("\n### Demo Complete!")
    output.success("Thank you for trying ChukTerm!")


@cli.command()
@click.option(
    "--theme",
    type=click.Choice(["default", "dark", "light", "minimal", "terminal", "monokai", "dracula"]),
    help="Set the theme",
)
def test(theme: str | None) -> None:
    """Run terminal tests."""
    if theme:
        set_theme(theme)

    output.status("Running terminal tests...")
    output.print("Test functionality will be implemented here")


def main() -> int:
    """Main entry point for the CLI."""
    try:
        cli()
        return 0
    except Exception as e:
        output.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
