"""Config CLI."""
# pylint: disable=too-many-arguments
import sys
from pathlib import Path
from typing import Optional, Union

import click
import git
import toml

from statue.cli.cli import statue_cli
from statue.cli.common_flags import config_path_option, verbose_option
from statue.cli.interactive_sources_adder import InteractiveSourcesAdder
from statue.cli.styled_strings import (
    bullet_style,
    failure_style,
    name_style,
    source_style,
)
from statue.commands_filter import CommandsFilter
from statue.config.configuration_builder import ConfigurationBuilder
from statue.constants import ENCODING
from statue.exceptions import StatueConfigurationError, UnknownTemplate
from statue.sources_finder import find_sources
from statue.templates.templates_provider import TemplatesProvider


@statue_cli.group("config")
def config_cli():
    """Configuration related actions."""


@config_cli.command("show-tree")
@config_path_option
def show_tree(config: Optional[Union[str, Path]]):
    """
    Show sources configuration as a tree.

    This method prints the sources' configuration as a tree, including:
    contexts, allow and deny lists and matching commands.

    # noqa: DAR101
    """
    config = Path(config) if config is not None else None
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


@config_cli.command("init")
@config_path_option
@click.option(
    "-t",
    "--template",
    type=str,
    default="defaults",
    help="Configuration template name",
)
@click.option("-y", "interactive", flag_value=False, default=True)
@click.option(
    "--git/--no-git",
    "use_git",
    is_flag=True,
    default=True,
    help="Should use git to trace ignored files",
)
@click.option(
    "--fix-versions",
    is_flag=True,
    default=False,
    help="Fix versions in config when running",
)
@click.option(
    "-i",
    "--install",
    is_flag=True,
    default=False,
    help="Install latest version for all commands in configuration",
)
def init_config_cli(
    config: Optional[Union[str, Path]],
    template: str,
    interactive: bool,
    use_git: bool,
    fix_versions: bool,
    install: bool,
):
    """
    Initialize configuration for Statue.

    By default, this command searches for sources files in the given directory (cwd by
     default) and sets them with default contexts.

    You can run this command with the "-i" flag in order to choose interactively which
     source files to track and which contexts to assign to them.
    """
    try:
        configuration = ConfigurationBuilder.build_configuration_from_file(
            TemplatesProvider.get_template_path(template)
        )
    except (UnknownTemplate, StatueConfigurationError) as error:
        click.echo(failure_style(str(error)))
        sys.exit(3)
    output_path = (
        Path(config)
        if config is not None
        else ConfigurationBuilder.configuration_path()
    )
    directory = Path.cwd()
    repo = None
    if use_git:
        try:
            repo = git.Repo(directory)
        except git.InvalidGitRepositoryError:
            pass
    sources = [
        source.relative_to(directory) for source in find_sources(directory, repo=repo)
    ]
    if interactive:
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration,
            sources=sources,
            repo=repo,
        )
    else:
        for source in sources:
            configuration.sources_repository[source] = CommandsFilter()
    if fix_versions or install:
        for command_builder in configuration.commands_repository:
            if install:
                command_builder.update()
            if fix_versions and command_builder.installed():
                command_builder.set_version_as_installed()
    with open(output_path, mode="w", encoding=ENCODING) as config_file:
        toml.dump(configuration.as_dict(), config_file)
    click.echo("Done!")


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
def fixate_commands_versions(
    config: Optional[Union[str, Path]],
    latest: bool,
    verbosity: str,
):
    """
    Fixate the installed version of the commands.

    This helps you make sure that you use the same checkers in all commands
    across time.

    # noqa: DAR101
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


def __join_names(names_list):
    if names_list is None or len(names_list) == 0:
        return "empty"
    names_list = list(names_list)
    names_list.sort()
    return ", ".join([name_style(name) for name in names_list])
