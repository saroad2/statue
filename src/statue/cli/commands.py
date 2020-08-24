"""Commands CLI."""
from typing import Any, List, MutableMapping, Optional

import click

from statue.cli.cli import statue as statue_cli
from statue.cli.util import (
    allow_option,
    contexts_option,
    deny_option,
    install_commands_if_missing,
    silent_option,
    verbose_option,
    verbosity_option,
)
from statue.commands_reader import read_command, read_commands
from statue.constants import COMMANDS
from statue.excptions import InvalidCommand, UnknownCommand


@statue_cli.group("command")
def command() -> None:
    """Commands related actions such as list, install, show, etc."""


@command.command("list")
@click.pass_obj
@contexts_option
@allow_option
@deny_option
def list_commands(
    statue_configuration: MutableMapping[str, Any],
    context: Optional[List[str]],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
) -> None:
    """List matching commands to contexts, allow list and deny list."""
    commands = read_commands(
        statue_configuration[COMMANDS],
        contexts=context,
        allow_list=allow,
        deny_list=deny,
    )
    for command_instance in commands:
        click.echo(f"{command_instance.name} - {command_instance.help}")


@command.command("install")
@click.pass_obj
@contexts_option
@allow_option
@deny_option
@verbosity_option
@silent_option
@verbose_option
def install_commands(
    statue_configuration: MutableMapping[str, Any],
    context: Optional[List[str]],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
    verbosity: str,
) -> None:
    """Install missing commands."""
    install_commands_if_missing(
        read_commands(
            statue_configuration[COMMANDS],
            contexts=context,
            allow_list=allow,
            deny_list=deny,
        ),
        verbosity=verbosity,
    )


@command.command("show")
@click.pass_context
@click.argument("command_name", type=str)
@contexts_option
@allow_option
@deny_option
def show_command(
    ctx: click.Context,
    command_name: str,
    context: Optional[List[str]],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
) -> None:
    """Show information about specific command."""
    try:
        command_instance = read_command(
            command_name=command_name,
            commands_configuration=ctx.obj[COMMANDS],
            contexts=context,
            allow_list=allow,
            deny_list=deny,
        )
        click.echo(f"Name - {command_instance.name}")
        click.echo(f"Description - {command_instance.help}")
        click.echo(f"Arguments - {command_instance.args}")
    except (UnknownCommand, InvalidCommand) as error:
        click.echo(str(error))
        ctx.exit(1)
