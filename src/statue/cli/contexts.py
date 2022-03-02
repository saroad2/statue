"""Contexts CLI."""

import click

from statue.cli.cli import pass_configuration, statue_cli
from statue.cli.styled_strings import bullet_style, name_style
from statue.config.configuration import Configuration
from statue.exceptions import UnknownContext


@statue_cli.group("context")
def context_cli() -> None:
    """Contexts related actions such as list, show, etc."""


@context_cli.command("list")
@click.pass_context
@pass_configuration
def contexts_list_cli(configuration: Configuration, ctx: click.Context) -> None:
    """Print all available contexts."""
    if len(configuration.contexts_repository) == 0:
        click.echo("No contexts were found.")
        ctx.exit(1)
    for context in configuration.contexts_repository:
        click.echo(f"{name_style(context.name)} - {context.help}")


@context_cli.command("show")
@click.argument("context_name", type=str)
@click.pass_context
@pass_configuration
def show_contexts_cli(
    configuration: Configuration, ctx: click.Context, context_name: str
) -> None:
    """Print all available contexts."""
    try:
        context_instance = configuration.contexts_repository[context_name]
        click.echo(f"{bullet_style('Name')} - {name_style(context_instance.name)}")
        click.echo(f"{bullet_style('Description')} - {context_instance.help}")
        if len(context_instance.aliases) != 0:
            click.echo(
                f"{bullet_style('Aliases')} - {', '.join(context_instance.aliases)}"
            )
        if context_instance.parent is not None:
            click.echo(
                f"{bullet_style('Parent')} - {name_style(context_instance.parent.name)}"
            )
    except UnknownContext:
        click.echo(f'Could not find the context "{context_name}".')
        ctx.exit(1)
