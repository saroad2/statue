"""Contexts CLI."""
from typing import Any, MutableMapping

import click

from statue.cli.cli import statue as statue_cli
from statue.commands_reader import read_commands
from statue.constants import COMMANDS, CONTEXTS, HELP


@statue_cli.group()
def context() -> None:
    """Contexts related actions such as list, show, etc."""


@context.command("list")
@click.pass_obj
def contexts_list(statue_configuration: MutableMapping[str, Any]) -> None:
    """Print all available contexts."""
    for context_name, context_instance in statue_configuration[CONTEXTS].items():
        click.echo(f"{context_name} - {context_instance[HELP]}")


@context.command("show")
@click.pass_context
@click.argument("context_name", type=str)
def show_contexts(ctx: click.Context, context_name: str) -> None:
    """Print all available contexts."""
    statue_configuration = ctx.obj
    context_instance = statue_configuration[CONTEXTS].get(context_name, None)
    if context_instance is None:
        click.echo(f'Could not find the context "{context_name}".')
        ctx.exit(1)
    click.echo(f"Name - {context_name}")
    click.echo(f"Description - {context_instance[HELP]}")
    commands = read_commands(
        commands_configuration=statue_configuration[COMMANDS], contexts=[context_name]
    )
    click.echo(
        f"Matching commands - {', '.join([command.name for command in commands])}"
    )
