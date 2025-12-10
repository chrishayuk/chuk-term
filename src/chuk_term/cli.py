"""CLI interface for ChukTerm."""

import sys
from pathlib import Path

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
from chuk_term.ui.formatters import format_table
from chuk_term.ui.theme import get_available_themes, get_theme, set_theme


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


@cli.command()
@click.option("--side-by-side", "-s", is_flag=True, help="Show themes side by side")
def themes(side_by_side: bool) -> None:
    """Preview all available themes."""
    available_themes = get_available_themes()
    current_theme = get_theme().name

    output.rule("ChukTerm Theme Gallery")
    output.info(f"Current theme: {current_theme}\n")

    if side_by_side:
        # Show a compact preview of all themes
        from rich.columns import Columns
        from rich.panel import Panel

        panels = []
        for theme_name in available_themes:
            set_theme(theme_name)
            content = f"[{get_theme().style('info')}]Info[/]\n"
            content += f"[{get_theme().style('success')}]Success[/]\n"
            content += f"[{get_theme().style('warning')}]Warning[/]\n"
            content += f"[{get_theme().style('error')}]Error[/]"
            panels.append(Panel(content, title=theme_name, border_style=get_theme().style("info")))

        output._console.print(Columns(panels, equal=True, expand=True))
        # Restore original theme
        set_theme(current_theme)
    else:
        # Show detailed preview of each theme
        for theme_name in available_themes:
            set_theme(theme_name)
            output.rule(f"Theme: {theme_name}")
            output.info("This is an info message")
            output.success("This is a success message")
            output.warning("This is a warning message")
            output.error("This is an error message")
            output.debug("This is a debug message")
            output.print("")  # Empty line

        # Restore original theme
        set_theme(current_theme)

    output.rule("Theme Gallery Complete")
    output.tip("Use 'chuk-term themes --side-by-side' for compact view")
    output.hint(f"Current theme restored: {current_theme}")


@cli.command()
@click.option("--run", "-r", "run_example", help="Run a specific example by name")
@click.option("--list-only", "-l", is_flag=True, help="Only list examples without details")
def examples(run_example: str | None, list_only: bool) -> None:
    """List and run available examples."""
    # Find examples directory
    package_dir = Path(__file__).parent
    examples_dir = package_dir.parent.parent / "examples"

    if not examples_dir.exists():
        output.error(f"Examples directory not found at: {examples_dir}")
        return

    example_files = sorted(examples_dir.glob("*.py"))

    if not example_files:
        output.warning("No example files found")
        return

    if run_example:
        # Run specific example
        example_path = examples_dir / f"{run_example}.py"
        if not example_path.exists():
            # Try with ui_ prefix
            example_path = examples_dir / f"ui_{run_example}.py"

        if not example_path.exists():
            output.error(f"Example '{run_example}' not found")
            output.hint("Use 'chuk-term examples' to see available examples")
            return

        output.info(f"Running example: {example_path.name}")
        output.rule(example_path.stem)

        # Execute the example
        import subprocess

        try:
            result = subprocess.run([sys.executable, str(example_path)], check=True)
            if result.returncode == 0:
                output.success(f"Example '{example_path.stem}' completed successfully")
        except subprocess.CalledProcessError as e:
            output.error(f"Example failed with exit code {e.returncode}")
        return

    # List examples
    output.rule("ChukTerm Examples")

    if list_only:
        for example_file in example_files:
            output.print(f"  • {example_file.stem}")
    else:
        table_data = []
        for example_file in example_files:
            # Read first line of docstring for description
            try:
                with open(example_file) as f:
                    lines = f.readlines()
                    description = "No description"
                    for line in lines[:10]:  # Check first 10 lines
                        if '"""' in line or "'''" in line:
                            # Extract description
                            description = line.strip("\"' \n")
                            if description:
                                break
                table_data.append({"Name": example_file.stem, "Description": description[:60]})
            except Exception:
                table_data.append({"Name": example_file.stem, "Description": "Error reading file"})

        table = format_table(table_data, title="Available Examples")
        output.print_table(table)

    output.print("\n")
    output.tip("Run an example: chuk-term examples --run <name>")
    output.hint(f"Found {len(example_files)} example(s)")


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
