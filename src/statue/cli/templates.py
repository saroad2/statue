"""Templates CLI."""
import sys

import click

from statue.cli.cli import statue_cli
from statue.cli.styled_strings import failure_style, name_style
from statue.exceptions import UnknownTemplate
from statue.templates.templates_provider import TemplatesProvider


@statue_cli.group("templates")
def templates_cli() -> None:
    """Template related actions such as list, show, etc."""


@templates_cli.command("list")
def list_templates_cli():
    """List all available templates."""
    for template_file in TemplatesProvider.template_names():
        click.echo(name_style(template_file))


@templates_cli.command("show")
@click.argument("template_name", type=str)
def show_templates_cli(template_name):
    """Show template by name."""
    try:
        template_path = TemplatesProvider.get_template_path(template_name)
    except UnknownTemplate as error:
        click.echo(failure_style(str(error)))
        sys.exit(1)
    with template_path.open(mode="r") as template_file:
        template_lines = template_file.readlines()
    click.echo("".join(template_lines))
