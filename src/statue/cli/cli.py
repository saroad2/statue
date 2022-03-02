"""Main CLI for statue."""
from pathlib import Path
from typing import Optional

import click

from statue import __version__
from statue.config.configuration import Configuration
from statue.config.configuration_builder import ConfigurationBuilder
from statue.exceptions import MissingConfiguration

pass_configuration = click.make_pass_decorator(Configuration)


@click.group(name="statue", no_args_is_help=True)
@click.version_option(version=__version__)
@click.option(
    "--config",
    envvar="STATUE_CONFIG",
    type=click.Path(exists=True, dir_okay=False),
    help="Statue configuration file.",
)
@click.pass_context
def statue_cli(ctx, config: Optional[str]) -> None:
    """Statue is a static code analysis tools orchestrator."""
    config_path = Path(config) if config is not None else None
    try:
        ctx.obj = ConfigurationBuilder.build_configuration_from_file(config_path)
    except MissingConfiguration as error:
        click.echo(click.style(error))
        ctx.exit(3)
