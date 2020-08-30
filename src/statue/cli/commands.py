"""Commands CLI."""
from typing import List, Optional

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
from statue.configuration import Configuration
from statue.excptions import InvalidCommand, UnknownCommand


@statue_cli.group("command")
def commands_cli() -> None:
    """Commands related actions such as list, install, show, etc."""


@commands_cli.command("list")
@contexts_option
@allow_option
@deny_option
def list_commands(
    context: Optional[List[str]],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
) -> None:
    """List matching commands to contexts, allow list and deny list."""
    commands = Configuration.read_commands(
        contexts=context,
        allow_list=allow,
        deny_list=deny,
    )
    for command_instance in commands:
        click.echo(f"{command_instance.name} - {command_instance.help}")


@commands_cli.command("install")
@contexts_option
@allow_option
@deny_option
@silent_option
@verbose_option
@verbosity_option
def install_commands(
    context: Optional[List[str]],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
    verbosity: str,
) -> None:
    """Install missing commands."""
    install_commands_if_missing(
        Configuration.read_commands(
            contexts=context,
            allow_list=allow,
            deny_list=deny,
        ),
        verbosity=verbosity,
    )


@commands_cli.command("show")
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
        command_instance = Configuration.read_command(
            command_name=command_name,
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
