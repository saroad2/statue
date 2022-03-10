"""Config CLI."""
import re
from collections import OrderedDict
from pathlib import Path
from typing import Union

import click
import git
import toml

from statue.cli.cli import pass_configuration, statue_cli
from statue.cli.common_flags import verbose_option
from statue.cli.styled_strings import bullet_style, name_style, source_style
from statue.config.configuration import Configuration
from statue.config.configuration_builder import ConfigurationBuilder
from statue.constants import COMMANDS, CONTEXTS, ENCODING, SOURCES, VERSION
from statue.sources_finder import expend, find_sources

YES = ["y", "yes"]
NO = ["n", "no"]
EXPEND = ["e", "expend"]
DEFAULT_OPTION = "yes"


@statue_cli.group("config")
def config_cli():
    """Configuration related actions."""


@config_cli.command("show-tree")
@pass_configuration
def show_tree(configuration: Configuration):
    """
    Show sources configuration as a tree.

    This method prints the sources' configuration as a tree, including:
    contexts, allow and deny lists and matching commands.

    # noqa: DAR101
    """
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
@click.option(
    "--directory",
    type=click.Path(dir_okay=True, file_okay=False, exists=True),
    help=(
        "Directory to save configuration in. "
        "Tracked files will be saved relative paths to this directory. "
        "Default directory is current working directory."
    ),
)
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    default=False,
    help="Run interactively in order to determine tracked sources and contexts.",
)
def init_config_cli(directory, interactive):
    """
    Initialize configuration for Statue.

    By default, this command searches for sources files in the given directory (cwd by
     default) and sets them with default contexts.

    You can run this command with the "-i" flag in order to choose interactively which
     source files to track and which contexts to assign to them.
    """
    if directory is None:
        directory = Path.cwd()
    if isinstance(directory, str):
        directory = Path(directory)
    repo = None
    try:
        repo = git.Repo(directory)
    except git.InvalidGitRepositoryError:
        pass
    sources = [
        source.relative_to(directory) for source in find_sources(directory, repo=repo)
    ]
    sources_map = OrderedDict()
    __update_sources_map(
        sources_map,
        sources,
        repo=repo,
        interactive=interactive,
    )
    with open(
        ConfigurationBuilder.configuration_path(directory), mode="w", encoding=ENCODING
    ) as config_file:
        toml.dump({SOURCES: sources_map}, config_file)


@config_cli.command("fix-versions")
@click.option(
    "--directory",
    type=click.Path(dir_okay=True, file_okay=False, exists=True),
    help=(
        "Directory to save configuration in. "
        "Tracked files will be saved relative paths to this directory. "
        "Default directory is current working directory."
    ),
)
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
    directory: Union[str, Path],
    latest: bool,
    verbosity: str,
):
    """
    Fixate the installed version of the commands.

    This helps you make sure that you use the same checkers in all commands
    across time.

    # noqa: DAR101
    """
    if directory is None:
        directory = Path.cwd()
    if isinstance(directory, str):
        directory = Path(directory)
    configuration_path = ConfigurationBuilder.configuration_path(directory)
    configuration = ConfigurationBuilder.build_configuration_from_file(
        configuration_path
    )
    if len(configuration.commands_repository) == 0:
        click.echo("No commands to fixate.")
        return
    with open(configuration_path, mode="r", encoding=ENCODING) as config_file:
        raw_config_dict = toml.load(config_file)
    if COMMANDS not in raw_config_dict:
        raw_config_dict[COMMANDS] = {}
    for command_builder in configuration.commands_repository:
        if latest:
            command_builder.update(verbosity=verbosity)
        if not command_builder.installed():
            continue
        if command_builder.name not in raw_config_dict[COMMANDS]:
            raw_config_dict[COMMANDS][command_builder.name] = {}
        raw_config_dict[COMMANDS][command_builder.name][
            VERSION
        ] = command_builder.installed_version
    with open(configuration_path, mode="w", encoding=ENCODING) as config_file:
        toml.dump(raw_config_dict, config_file)


def __update_sources_map(sources_map, sources, repo=None, interactive=False):
    for source in sources:
        option = "y"
        if interactive:
            choices = YES + NO
            choices_string = "[Y]es, [N]o"
            if source.is_dir():
                choices.extend(EXPEND)
                choices_string += ", [E]xpend"
            option = click.prompt(
                f'Would you like to track "{source}" ({choices_string}. '
                f"default: {DEFAULT_OPTION})",
                type=click.Choice(choices, case_sensitive=False),
                show_choices=False,
                show_default=False,
                default=DEFAULT_OPTION,
            ).lower()
        if option in EXPEND:
            __update_sources_map(
                sources_map,
                expend(source, repo=repo),
                repo=repo,
                interactive=interactive,
            )
        if option not in YES:
            continue
        contexts = __get_default_contexts(source)
        if interactive:
            default_contexts_string = ",".join(contexts)
            contexts_string = click.prompt(
                f'Add contexts to "{source}" (default: [{default_contexts_string}])',
                type=str,
                default=default_contexts_string,
                show_default=False,
            )
            if len(contexts_string) != 0:
                contexts = re.split(r"[ \t]*,[ \t]*", contexts_string)
        sources_map[source.as_posix()] = {}
        if len(contexts) != 0:
            sources_map[source.as_posix()][CONTEXTS] = contexts


def __get_default_contexts(source: Path):
    if "test" in source.as_posix():
        return ["test"]
    if source.name == "setup.py":
        return ["fast"]
    return []


def __join_names(names_list):
    if names_list is None or len(names_list) == 0:
        return "empty"
    names_list = list(names_list)
    names_list.sort()
    return ", ".join([name_style(name) for name in names_list])
