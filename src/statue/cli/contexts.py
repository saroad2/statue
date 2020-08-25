"""Contexts CLI."""
from typing import Any, MutableMapping

import click

from statue.cli.cli import statue as statue_cli
from statue.commands_reader import read_commands
from statue.configuration import Configuration
from statue.constants import COMMANDS, CONTEXTS, HELP


@statue_cli.group()
def context() -> None:
    """Contexts related actions such as list, show, etc."""


@context.command("list")
@click.pass_context
def contexts_list(ctx: click.Context) -> None:
    """Print all available contexts."""
    contexts_configuration = Configuration.contexts_configuration
    if contexts_configuration is None:
        click.echo(f"No contexts were found.")
        ctx.exit(1)
    for context_name, context_instance in contexts_configuration.items():
        click.echo(f"{context_name} - {context_instance[HELP]}")


@context.command("show")
@click.pass_context
@click.argument("context_name", type=str)
def show_contexts(ctx: click.Context, context_name: str) -> None:
    """Print all available contexts."""
    contexts_configuration = Configuration.contexts_configuration
    if contexts_configuration is None:
        click.echo(f"No contexts were found.")
        ctx.exit(1)
    context_instance = contexts_configuration.get(context_name, None)
    if context_instance is None:
        click.echo(f'Could not find the context "{context_name}".')
        ctx.exit(1)
    click.echo(f"Name - {context_name}")
    click.echo(f"Description - {context_instance[HELP]}")
    commands = read_commands(contexts=[context_name])
    click.echo(
        f"Matching commands - {', '.join([command.name for command in commands])}"
    )
