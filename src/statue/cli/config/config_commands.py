"""Commands configuration CLI."""
import sys
from pathlib import Path
from typing import Optional

import click

from statue.cli.common_flags import config_path_option, verbose_option
from statue.cli.config.config_cli import config_cli
from statue.cli.config.interactive_adders.interactive_command_adder import (
    InteractiveCommandAdder,
)
from statue.cli.styled_strings import failure_style, name_style
from statue.config.configuration import Configuration
from statue.exceptions import UnknownCommand


@config_cli.command("add-command")
@config_path_option
def add_command_cli(config):
    """Add new command to configuration."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    InteractiveCommandAdder.add_command(configuration)
    configuration.to_toml(config)
    click.echo("Command was successfully added!")


@config_cli.command("edit-command")
@config_path_option
@click.argument("command_name", type=str)
def edit_command_cli(config, command_name):
    """Edit context from configuration."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    InteractiveCommandAdder.edit_command(name=command_name, configuration=configuration)
    configuration.to_toml(config)
    click.echo(f"{name_style(command_name)} was successfully edited!")


@config_cli.command("remove-command")
@config_path_option
@click.argument("command_name", type=str)
def remove_command_cli(config, command_name):
    """Remove command from configuration."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    try:
        command_builder = configuration.commands_repository[command_name]
    except UnknownCommand as error:
        click.echo(failure_style(str(error)))
        sys.exit(1)
    if not click.confirm(
        f"Are you sure you would like to remove the command {name_style(command_name)} "
        "and all of its references from configuration?",
    ):
        click.echo("Abort!")
        return
    configuration.remove_command(command_builder)
    configuration.to_toml(config)
    click.echo(f"{name_style(command_name)} was successfully removed!")


@config_cli.command(
    "fix-versions", short_help="Fixate the installed version of the commands."
)
@config_path_option
@click.option(
    "-l",
    "--latest",
    is_flag=True,
    default=False,
    help=(
        "Update commands to latest before fixing the version. "
        "If a command is not installed, will install it."
    ),
)
@verbose_option
def fixate_commands_versions_cli(
    config: Optional[Path],
    latest: bool,
    verbosity: str,
):
    """
    Fixate the installed version of the commands.

    This helps you make sure that you use the same checkers in all commands
    across time.
    """
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    if len(configuration.commands_repository) == 0:
        click.echo("No commands to fixate.")
        return
    for command_builder in configuration.commands_repository:
        if latest:
            command_builder.update(verbosity=verbosity)
        if not command_builder.installed():
            continue
        command_builder.set_version_as_installed()
    configuration.to_toml(config)
