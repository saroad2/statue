"""Main CLI for statue."""
from pathlib import Path
from typing import Optional, Union

import click

from statue import __version__
from statue.cli.styled_strings import failure_style
from statue.config.configuration import Configuration
from statue.config.configuration_builder import ConfigurationBuilder
from statue.exceptions import StatueConfigurationError

pass_configuration = click.make_pass_decorator(Configuration)


@click.group(name="statue", no_args_is_help=True)
@click.version_option(version=__version__)
@click.option(
    "--config",
    envvar="STATUE_CONFIG",
    type=click.Path(exists=True, dir_okay=False),
    help="Statue configuration file.",
)
@click.option(
    "--cache-dir",
    envvar="STATUE_CACHE_CONFIG",
    type=click.Path(exists=True, file_okay=False),
    help="Statue caching directory path",
)
@click.pass_context
def statue_cli(
    ctx, config: Optional[Union[str, Path]], cache_dir: Optional[Union[str, Path]]
) -> None:
    """Statue is a static code analysis tools orchestrator."""
    config_path = Path(config) if config is not None else None
    cache_dir = Path(cache_dir) if cache_dir is not None else None
    try:
        ctx.obj = ConfigurationBuilder.build_configuration_from_file(
            statue_configuration_path=config_path, cache_dir=cache_dir
        )
    except StatueConfigurationError as error:
        click.echo(failure_style(click.style(error)))
        ctx.exit(3)
