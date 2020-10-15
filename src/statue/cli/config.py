"""Config CLI."""
from collections import OrderedDict
from pathlib import Path

import click
import toml

from statue.cli.cli import statue as statue_cli
from statue.configuration import Configuration
from statue.constants import CONTEXTS, SOURCES
from statue.sources_finder import find_sources


@statue_cli.group("config")
def config_cli():
    """Configuration related actions."""


@config_cli.command("init")
@click.option(
    "-d",
    "--directory",
    type=click.Path(dir_okay=True, file_okay=False, exists=True),
)
def init_config(directory):
    """Initialize configuration path."""
    if directory is None:
        directory = Path.cwd()
    if isinstance(directory, str):
        directory = Path(directory)
    sources = sorted(find_sources(directory))
    config = {SOURCES: OrderedDict()}
    for source in sources:
        contexts = __get_default_contexts(source)
        config[SOURCES][source.relative_to(directory).as_posix()] = {CONTEXTS: contexts}
    with open(Configuration.configuration_path(directory), mode="w") as config_file:
        toml.dump(config, config_file)


def __get_default_contexts(source: Path):
    if "test" in source.name:
        return ["test"]
    if source.name == "setup.py":
        return ["fast"]
    return []
