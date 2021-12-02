"""Commands CLI."""
from typing import List, Optional

import click

from statue.cli.cli import statue_cli
from statue.cli.util import (
    allow_option,
    bullet_style,
    contexts_option,
    deny_option,
    name_style,
    silent_option,
    verbose_option,
    verbosity_option,
)
from statue.configuration import Configuration
from statue.exceptions import InvalidCommand, UnknownCommand


@statue_cli.group("command")
def commands_cli() -> None:
    """Commands related actions such as list, install, show, etc."""


@commands_cli.command("list")
@contexts_option
@allow_option
@deny_option
def list_commands_cli(
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
        click.echo(f"{name_style(command_instance.name)} - {command_instance.help}")


@commands_cli.command("install")
@contexts_option
@allow_option
@deny_option
@silent_option
@verbose_option
@verbosity_option
def install_commands_cli(
    context: Optional[List[str]],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
    verbosity: str,
) -> None:
    """Install missing commands."""
    commands_list = Configuration.read_commands(
        contexts=context, allow_list=allow, deny_list=deny
    )
    for command in commands_list:
        command.install(verbosity=verbosity)


@commands_cli.command("show")
@click.pass_context
@click.argument("command_name", type=str)
@contexts_option
@allow_option
@deny_option
def show_command_cli(
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
        click.echo(f"{bullet_style('Name')} - {name_style(command_instance.name)}")
        click.echo(f"{bullet_style('Description')} - {command_instance.help}")
        click.echo(f"{bullet_style('Arguments')} - {command_instance.args}")
    except (UnknownCommand, InvalidCommand) as error:
        click.echo(str(error))
        ctx.exit(1)
