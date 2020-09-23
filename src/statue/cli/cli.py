"""Main CLI for statue."""
from pathlib import Path
from typing import Optional

import click

from statue import __version__
from statue.configuration import Configuration


@click.group(no_args_is_help=True)
@click.version_option(version=__version__)
@click.option(
    "--config",
    envvar="STATUE_CONFIG",
    type=click.Path(exists=True, dir_okay=False),
    help="Statue configuration file.",
)
def statue(config: Optional[str]) -> None:
    """Statue is a static code analysis tools orchestrator."""
    if config is not None:
        Configuration.load_configuration(Path(config))
    else:
        Configuration.load_configuration(Path.cwd() / "statue.toml")
