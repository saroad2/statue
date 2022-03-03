"""Commands CLI."""
from typing import List

import click

from statue.cli.cli import pass_configuration, statue_cli
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
from statue.config.configuration import Configuration
from statue.exceptions import UnknownCommand


@statue_cli.group("command")
def commands_cli() -> None:
    """Commands related actions such as list, install, show, etc."""


@commands_cli.command("list")
@pass_configuration
def list_commands_cli(configuration: Configuration) -> None:
    """List matching commands to contexts, allow list and deny list."""
    for command_builder in configuration.commands_repository:
        click.echo(f"{name_style(command_builder.name)} - {command_builder.help}")


@commands_cli.command("install")
@contexts_option
@allow_option
@deny_option
@silent_option
@verbose_option
@verbosity_option
@pass_configuration
def install_commands_cli(
    configuration: Configuration,
    context: List[str],
    allow: List[str],
    deny: List[str],
    verbosity: str,
) -> None:
    """Install missing commands."""
    commands_list = configuration.build_commands(
        CommandsFilter(
            contexts=frozenset(
                {
                    configuration.contexts_repository[context_name]
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
@click.argument("command_name", type=str)
@click.pass_context
@pass_configuration
def show_command_cli(
    configuration: Configuration,
    ctx: click.Context,
    command_name: str,
) -> None:
    """Show information about specific command."""
    command_builder = None
    try:
        command_builder = configuration.commands_repository[command_name]
    except UnknownCommand as error:
        click.echo(str(error))
        ctx.exit(1)
    click.echo(f"{bullet_style('Name')} - {name_style(command_builder.name)}")
    click.echo(f"{bullet_style('Description')} - {command_builder.help}")
    if len(command_builder.default_args) != 0:
        click.echo(
            f"{bullet_style('Default arguments')} - "
            f"{' '.join(command_builder.default_args)}"
        )
    if len(command_builder.required_contexts) != 0:
        click.echo(
            f"{bullet_style('Required contexts')} - "
            f"{', '.join(command_builder.required_contexts)}"
        )
    if len(command_builder.allowed_contexts) != 0:
        click.echo(
            f"{bullet_style('Allowed contexts')} - "
            f"{', '.join(command_builder.allowed_contexts)}"
        )
    if len(command_builder.specified_contexts) != 0:
        click.echo(
            f"{bullet_style('Specified contexts')} - "
            f"{', '.join(command_builder.specified_contexts)}"
        )
