"""Commands configuration CLI."""
from pathlib import Path
from typing import Optional, Union

import click
import toml

from statue.cli.common_flags import config_path_option, verbose_option
from statue.cli.config.config_cli import config_cli
from statue.config.configuration_builder import ConfigurationBuilder
from statue.constants import ENCODING


@config_cli.command("fix-versions")
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
    config: Optional[Union[str, Path]],
    latest: bool,
    verbosity: str,
):
    """
    Fixate the installed version of the commands.

    This helps you make sure that you use the same checkers in all commands
    across time.
    """
    config = (
        Path(config)
        if config is not None
        else ConfigurationBuilder.configuration_path()
    )
    configuration = ConfigurationBuilder.build_configuration_from_file(config)
    if len(configuration.commands_repository) == 0:
        click.echo("No commands to fixate.")
        return
    for command_builder in configuration.commands_repository:
        if latest:
            command_builder.update(verbosity=verbosity)
        if not command_builder.installed():
            continue
        command_builder.set_version_as_installed()
    with open(config, mode="w", encoding=ENCODING) as config_file:
        toml.dump(configuration.as_dict(), config_file)
