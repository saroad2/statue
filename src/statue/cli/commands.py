"""Commands CLI."""
from typing import List

import click

from statue.cli.cli import statue_cli
from statue.cli.common_flags import (
    allow_option,
    contexts_option,
    deny_option,
    silent_option,
    verbose_option,
    verbosity_option,
)
from statue.cli.styled_strings import bullet_style, name_style
from statue.commands_filter import CommandsFilter
from statue.configuration import Configuration
from statue.exceptions import UnknownCommand


@statue_cli.group("command")
def commands_cli() -> None:
    """Commands related actions such as list, install, show, etc."""


@commands_cli.command("list")
@contexts_option
@allow_option
@deny_option
def list_commands_cli(
    context: List[str],
    allow: List[str],
    deny: List[str],
) -> None:
    """List matching commands to contexts, allow list and deny list."""
    commands = Configuration.build_commands(
        CommandsFilter(
            contexts=frozenset(
                {
                    Configuration.contexts_repository[context_name]
                    for context_name in context
                }
            ),
            allowed_commands=(frozenset(allow) if len(allow) != 0 else None),
            denied_commands=(frozenset(deny) if len(deny) != 0 else None),
        )
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
    context: List[str], allow: List[str], deny: List[str], verbosity: str
) -> None:
    """Install missing commands."""
    commands_list = Configuration.build_commands(
        CommandsFilter(
            contexts=frozenset(
                {
                    Configuration.contexts_repository[context_name]
                    for context_name in context
                }
            ),
            allowed_commands=(frozenset(allow) if len(allow) != 0 else None),
            denied_commands=(frozenset(deny) if len(deny) != 0 else None),
        )
    )
    for command in commands_list:
        command.install(verbosity=verbosity)


@commands_cli.command("show")
@click.pass_context
@click.argument("command_name", type=str)
def show_command_cli(
    ctx: click.Context,
    command_name: str,
) -> None:
    """Show information about specific command."""
    try:
        command_instance = Configuration.get_command_builder(command_name)
        click.echo(f"{bullet_style('Name')} - {name_style(command_instance.name)}")
        click.echo(f"{bullet_style('Description')} - {command_instance.help}")
        click.echo(
            f"{bullet_style('Default arguments')} - {command_instance.default_args}"
        )
    except UnknownCommand as error:
        click.echo(str(error))
        ctx.exit(1)
