# pylint: disable=too-many-arguments
"""Config CLI."""
import re
from collections import OrderedDict
from pathlib import Path

import click
import git
import toml

from statue.cli.cli import statue_cli
from statue.cli.common_flags import (
    allow_option,
    contexts_option,
    deny_option,
    verbose_option,
)
from statue.cli.styled_strings import bullet_style, name_style, source_style
from statue.configuration import Configuration
from statue.constants import (
    ALLOW_LIST,
    COMMANDS,
    CONTEXTS,
    DENY_LIST,
    ENCODING,
    SOURCES,
    VERSION,
)
from statue.sources_finder import expend, find_sources

YES = ["y", "yes"]
NO = ["n", "no"]
EXPEND = ["e", "expend"]
DEFAULT_OPTION = "yes"


@statue_cli.group("config")
def config_cli():
    """Configuration related actions."""


@config_cli.command("show-tree")
def show_tree():
    """
    Show sources configuration as a tree.

    This method prints the sources' configuration as a tree, including:
    contexts, allow and deny lists and matching commands.
    """
    sources_list = Configuration.sources_list()
    if len(sources_list) == 0:
        click.echo("No sources configuration is specified.")
    for source in sources_list:
        source_config = Configuration.get_source_configuration(source)
        contexts = source_config.get(CONTEXTS)
        allowed = source_config.get(ALLOW_LIST)
        denied = source_config.get(DENY_LIST)
        click.echo(
            f"{source_style(source)} "
            f"({bullet_style('contexts')}: {__join_names(contexts)}, "
            f"{bullet_style('allowed')}: {__join_names(allowed)}, "
            f"{bullet_style('denied')}: {__join_names(denied)}):"
        )
        commands = Configuration.read_commands(
            contexts=contexts, allow_list=allowed, deny_list=denied
        )
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
        Configuration.configuration_path(directory), mode="w", encoding=ENCODING
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
@contexts_option
@allow_option
@deny_option
@verbose_option
def fixate_commands_versions(
    directory,
    context,
    allow,
    deny,
    latest,
    verbosity,
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
    configuration_path = Configuration.configuration_path(directory)
    Configuration.load_configuration(configuration_path)
    commands_list = Configuration.read_commands(
        contexts=context, allow_list=allow, deny_list=deny
    )
    if len(commands_list) == 0:
        click.echo("No commands to fixate.")
        return
    with open(configuration_path, mode="r", encoding=ENCODING) as config_file:
        raw_config_dict = toml.load(config_file)
    if COMMANDS not in raw_config_dict:
        raw_config_dict[COMMANDS] = {}
    for command in commands_list:
        if latest:
            command.update(verbosity=verbosity)
        if not command.installed():
            continue
        if command.name not in raw_config_dict[COMMANDS]:
            raw_config_dict[COMMANDS][command.name] = {}
        raw_config_dict[COMMANDS][command.name][VERSION] = command.installed_version
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
    return ", ".join([name_style(name) for name in names_list])
