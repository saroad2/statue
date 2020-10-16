"""Config CLI."""
import re
from collections import OrderedDict
from pathlib import Path

import click
import git
import toml

from statue.cli.cli import statue as statue_cli
from statue.configuration import Configuration
from statue.constants import CONTEXTS, SOURCES
from statue.sources_finder import expend, find_sources

YES = ["y", "yes"]
NO = ["n", "no"]
EXPEND = ["e", "expend"]
DEFAULT_OPTION = "yes"


@statue_cli.group("config")
def config_cli():
    """Configuration related actions."""


@config_cli.command("init")
@click.option(
    "-d",
    "--directory",
    type=click.Path(dir_okay=True, file_okay=False, exists=True),
    help=(
        "Directory to save configuration in. "
        "Tracked files will be saved relative paths to this directory"
    ),
)
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    default=False,
    help="Run interactively in order to determine tracked sources and contexts.",
)
def init_config(directory, interactive):
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
    with open(Configuration.configuration_path(directory), mode="w") as config_file:
        toml.dump({SOURCES: sources_map}, config_file)


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
            contexts = re.split(r"[ \t]*,[ \t]*", contexts_string)
        sources_map[source.as_posix()] = {CONTEXTS: contexts}


def __get_default_contexts(source: Path):
    if "test" in source.as_posix():
        return ["test"]
    if source.name == "setup.py":
        return ["fast"]
    return ["standard"]
