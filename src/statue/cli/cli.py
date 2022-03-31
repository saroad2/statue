"""Main CLI for statue."""
from pathlib import Path
from typing import Optional

import click

from statue import __version__
from statue.cli.common_flags import config_path_option
from statue.cli.styled_strings import failure_style
from statue.config.configuration import Configuration
from statue.exceptions import StatueConfigurationError

pass_configuration = click.make_pass_decorator(Configuration)


@click.group(name="statue", no_args_is_help=True)
@click.version_option(version=__version__)
@config_path_option
@click.option(
    "--cache-dir",
    envvar="STATUE_CACHE",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Statue caching directory path",
)
@click.pass_context
def statue_cli(
    ctx: click.Context,
    config: Optional[Path],
    cache_dir: Optional[Path],
):
    """Statue is a static code analysis tools orchestrator."""
    if ctx.invoked_subcommand in ["config", "templates"]:
        return
    try:
        ctx.obj = Configuration.from_file(config_path=config, cache_dir=cache_dir)
    except StatueConfigurationError as error:
        click.echo(failure_style(click.style(error)))
        ctx.exit(3)
