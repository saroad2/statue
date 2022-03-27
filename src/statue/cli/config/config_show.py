"""Show configuration CLI."""
from pathlib import Path
from typing import Optional

import click

from statue.cli.common_flags import config_path_option
from statue.cli.config.config_cli import config_cli
from statue.cli.styled_strings import bullet_style, name_style, source_style
from statue.config.configuration_builder import ConfigurationBuilder
from statue.constants import ENCODING


@config_cli.command("show")
@config_path_option
def show_config_cli(config: Optional[Path]):
    """Show configuration file context."""
    if config is None:
        config = ConfigurationBuilder.configuration_path()
    with open(config, mode="r", encoding=ENCODING) as config_file:
        lines = config_file.readlines()
    click.echo_via_pager(lines)


@config_cli.command("show-tree")
@config_path_option
def show_config_tree_cli(config: Optional[Path]):
    """
    Show sources configuration as a tree.

    This method prints the sources' configuration as a tree, including:
    contexts, allow and deny lists and matching commands.
    """
    configuration = ConfigurationBuilder.build_configuration_from_file(config)
    sources_list = configuration.sources_repository.sources_list
    if len(sources_list) == 0:
        click.echo("No sources configuration is specified.")
    for source in sources_list:
        source_commands_filter = configuration.sources_repository[source]
        context_names = [context.name for context in source_commands_filter.contexts]
        click.echo(
            f"{source_style(source)} "
            f"({bullet_style('contexts')}: "
            f"{__join_names(context_names)}, "
            f"{bullet_style('allowed')}: "
            f"{__join_names(source_commands_filter.allowed_commands)}, "
            f"{bullet_style('denied')}: "
            f"{__join_names(source_commands_filter.denied_commands)}):"
        )
        commands = configuration.build_commands(source_commands_filter)
        click.echo(f"\t{__join_names([command.name for command in commands])}")


def __join_names(names_list):
    if names_list is None or len(names_list) == 0:
        return "empty"
    names_list = list(names_list)
    names_list.sort()
    return ", ".join([name_style(name) for name in names_list])
