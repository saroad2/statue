"""Contexts CLI."""

import click

from statue.cli.cli import statue as statue_cli
from statue.configuration import Configuration


@statue_cli.group("context")
def context_cli() -> None:
    """Contexts related actions such as list, show, etc."""


@context_cli.command("list")
@click.pass_context
def contexts_list(ctx: click.Context) -> None:
    """Print all available contexts."""
    contexts_obj_list = Configuration.contexts_list()
    if len(contexts_obj_list) == 0:
        click.echo("No contexts were found.")
        ctx.exit(1)
    for context in contexts_obj_list:
        click.echo(f"{context.name} - {context.help}")


@context_cli.command("show")
@click.pass_context
@click.argument("context_name", type=str)
def show_contexts(ctx: click.Context, context_name: str) -> None:
    """Print all available contexts."""
    context_instance = Configuration.get_context(context_name)
    if context_instance is None:
        click.echo(f'Could not find the context "{context_name}".')
        ctx.exit(1)
    click.echo(f"Name - {context_name}")
    click.echo(f"Description - {context_instance.help}")
    if len(context_instance.aliases) != 0:
        click.echo(f"Aliases - {', '.join(context_instance.aliases)}")
    if context_instance.parent is not None:
        click.echo(f"Parent - {context_instance.parent.name}")
    commands = Configuration.read_commands(contexts=[context_name])
    click.echo(
        f"Matching commands - {', '.join([command.name for command in commands])}"
    )
