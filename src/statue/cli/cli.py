"""Main CLI for statue."""
from typing import Optional

import click

from statue import __version__
from statue.configuration import Configuration


@click.group(name="statue", no_args_is_help=True)
@click.version_option(version=__version__)
@click.option(
    "--config",
    envvar="STATUE_CONFIG",
    type=click.Path(exists=True, dir_okay=False),
    help="Statue configuration file.",
)
def statue_cli(config: Optional[str]) -> None:
    """Statue is a static code analysis tools orchestrator."""
    Configuration.load_configuration(config)
