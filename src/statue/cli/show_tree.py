"""Show commands map as tree."""
from typing import List, Optional, Sequence

import click

from statue.cli.cli import pass_configuration, statue_cli
from statue.cli.cli_util import list_or_none
from statue.cli.common_flags import allow_option, contexts_option, deny_option
from statue.cli.styled_strings import bullet_style, name_style, source_style
from statue.commands_filter import CommandsFilter
from statue.config.configuration import Configuration


@statue_cli.command("show-tree", short_help="Show sources configuration as a tree.")
@pass_configuration
@contexts_option
@allow_option
@deny_option
def show_tree_cli(
    configuration: Configuration,
    context: Sequence[str],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
):
    """
    Show sources configuration as a tree.

    This method prints the sources' configuration as a tree, including:
    contexts, allow and deny lists and matching commands.
    """
    sources_list = configuration.sources_repository.sources_list
    general_filter = CommandsFilter(
        allowed_commands=list_or_none(allow),
        denied_commands=list_or_none(deny),
        contexts=[
            configuration.contexts_repository[context_name] for context_name in context
        ],
    )
    if len(sources_list) == 0:
        click.echo("No sources configuration is specified.")
    for source in sources_list:
        source_commands_filter = CommandsFilter.merge(
            general_filter, configuration.sources_repository[source]
        )
        context_names = [context.name for context in source_commands_filter.contexts]
        click.echo(
            f"{source_style(str(source))} "
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
