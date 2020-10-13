"""Config CLI."""
from pathlib import Path

import click
import toml

from statue.cli.cli import statue as statue_cli
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
    default=Path.cwd,
)
def init_config(directory):
    """Initialize configuration path."""
    sources = find_sources(Path(directory))
    config = {SOURCES: {}}
    for source in sources:
        contexts = __get_default_contexts(source)
        config[SOURCES][str(source.relative_to(directory))] = {CONTEXTS: contexts}
    with open(directory / "statue.toml", mode="w") as config_file:
        toml.dump(config, config_file)


def __get_default_contexts(source: Path):
    if "test" in source.name:
        return ["test"]
    if source.name == "setup.py":
        return ["fast"]
    return []
